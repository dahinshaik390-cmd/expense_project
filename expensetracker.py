"""A beginner-friendly command-line personal expense tracker."""

import json
import math
import sys
from datetime import date
from pathlib import Path


CATEGORIES = ["Food", "Travel", "Shopping", "Education", "Other"]
DATA_FILE = Path(__file__).with_name("expenses.json")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def load_expenses():
    """Load saved expenses, or return an empty list when no data exists."""
    if not DATA_FILE.exists():
        return []

    try:
        file_contents = DATA_FILE.read_text(encoding="utf-8")
        if not file_contents.strip():
            return []
        expenses = json.loads(file_contents)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        print(f"Could not read saved expenses: {error}")
        return []

    if not isinstance(expenses, list):
        print("The expenses file must contain a list. Starting with no expenses.")
        return []

    valid_expenses = []
    for expense in expenses:
        if is_valid_expense(expense):
            valid_expenses.append(expense)
        else:
            print("Skipped an invalid record in the expenses file.")
    return valid_expenses


def is_valid_expense(expense):
    """Check that a saved record has all the fields the app needs."""
    if not isinstance(expense, dict):
        return False

    amount = expense.get("amount")
    if isinstance(amount, bool) or not isinstance(amount, (int, float)):
        return False
    try:
        amount_is_valid = amount > 0 and math.isfinite(amount)
    except (OverflowError, TypeError):
        amount_is_valid = False
    if not amount_is_valid:
        return False

    if expense.get("category") not in CATEGORIES:
        return False
    if not isinstance(expense.get("description"), str):
        return False
    if not expense["description"].strip():
        return False
    try:
        expense_date = date.fromisoformat(expense.get("date", ""))
    except (TypeError, ValueError):
        return False
    if expense_date.isoformat() != expense.get("date"):
        return False
    return True


def save_expenses(expenses):
    """Save all expenses to the JSON file."""
    temporary_file = DATA_FILE.with_name(f".{DATA_FILE.name}.tmp")
    try:
        temporary_file.write_text(
            json.dumps(expenses, indent=4) + "\n",
            encoding="utf-8",
        )
        temporary_file.replace(DATA_FILE)
        return True
    except OSError as error:
        try:
            temporary_file.unlink(missing_ok=True)
        except OSError:
            pass
        print(f"Could not save expenses: {error}")
        return False
#test

def get_positive_amount():
    """Prompt until the user enters a valid positive amount."""
    while True:
        amount_text = input("Amount: ").strip()
        try:
            amount = float(amount_text)
        except ValueError:
            print("Please enter a valid number, such as 12.50.")
            continue

        rounded_amount = round(amount, 2)
        if not math.isfinite(amount) or rounded_amount <= 0:
            print("The amount must be at least ₹0.01.")
            continue
        return rounded_amount


def choose_category():
    """Show the available categories and return a valid selection."""
    print("Categories:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"  {number}. {category}")

    while True:
        choice = input("Choose a category number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(CATEGORIES):
            return CATEGORIES[int(choice) - 1]
        print("Please choose a number from the category list.")


def get_expense_date():
    """Prompt for a date in YYYY-MM-DD format; blank means today."""
    while True:
        date_text = input(
            f"Date (YYYY-MM-DD, press Enter for {date.today().isoformat()}): "
        ).strip()
        if not date_text:
            return date.today().isoformat()
        try:
            parsed_date = date.fromisoformat(date_text)
        except ValueError:
            print("Please enter a real date in YYYY-MM-DD format.")
            continue
        if parsed_date.isoformat() != date_text:
            print("Please use the YYYY-MM-DD date format.")
            continue
        return date_text


def add_expense(expenses):
    """Collect and save a new expense."""
    print("\nAdd an expense")
    amount = get_positive_amount()
    category = choose_category()

    while True:
        description = input("Description: ").strip()
        if description:
            break
        print("Description cannot be empty.")

    expense = {
        "amount": amount,
        "category": category,
        "description": description,
        "date": get_expense_date(),
    }
    expenses.append(expense)
    if save_expenses(expenses):
        print("Expense added and saved.")
    else:
        expenses.pop()
        print("Expense could not be saved. Please try again.")


def display_expenses(expenses):
    """Print expenses in a readable table."""
    if not expenses:
        print("No expenses found. Add an expense to get started.")
        return

    print(f"\n{'#':<4}{'Amount':>12}  {'Category':<12}  {'Date':<10}  Description")
    print("-" * 70)
    for number, expense in enumerate(expenses, start=1):
        print(
            f"{number:<4}₹{expense['amount']:>10.2f}  "
            f"{expense['category']:<12}  {expense['date']:<10}  "
            f"{expense['description']}"
        )


def view_expenses(expenses):
    """Display every saved expense."""
    print("\nYour expenses")
    display_expenses(expenses)


def show_total(expenses):
    """Calculate and display the total amount spent."""
    total = sum(expense["amount"] for expense in expenses)
    print(f"\nTotal expenses: ₹{total:.2f}")


def filter_by_category(expenses):
    """Display expenses and total spending for one category."""
    print("\nFilter by category")
    category = choose_category()
    matching_expenses = [
        expense for expense in expenses if expense["category"] == category
    ]
    print(f"\n{category} expenses")
    display_expenses(matching_expenses)
    category_total = sum(expense["amount"] for expense in matching_expenses)
    print(f"Total for {category}: ₹{category_total:.2f}")


def delete_expense(expenses):
    """Delete an expense only after the user confirms."""
    if not expenses:
        print("There are no expenses to delete.")
        return

    print("\nDelete an expense")
    display_expenses(expenses)
    while True:
        choice = input("Enter the expense number to delete (or 0 to cancel): ").strip()
        if choice.isdigit() and 0 <= int(choice) <= len(expenses):
            expense_number = int(choice)
            break
        print("Please enter a number shown in the list, or 0 to cancel.")

    if expense_number == 0:
        print("Deletion cancelled.")
        return

    expense = expenses[expense_number - 1]
    confirmation = input(
        f"Delete '{expense['description']}' (₹{expense['amount']:.2f})? (y/n): "
    ).strip().lower()
    if confirmation == "y":
        del expenses[expense_number - 1]
        if save_expenses(expenses):
            print("Expense deleted.")
        else:
            expenses.insert(expense_number - 1, expense)
            print("Expense could not be deleted from the saved file.")
    else:
        print("Deletion cancelled.")


def display_menu():
    """Show the main menu."""
    print(
        "\n=== Personal Expense Tracker ===\n"
        "1. Add expense\n"
        "2. View expenses\n"
        "3. Show total expenses\n"
        "4. Filter by category\n"
        "5. Delete expense\n"
        "6. Exit"
    )


def main():
    """Run the application menu until the user chooses to exit."""
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    expenses = load_expenses()
    actions = {
        "1": add_expense,
        "2": view_expenses,
        "3": show_total,
        "4": filter_by_category,
        "5": delete_expense,
    }

    while True:
        display_menu()
        try:
            choice = input("Choose an option (1-6): ").strip()
        except EOFError:
            print("\nInput ended. Goodbye!")
            break
        except KeyboardInterrupt:
            print("\nInput cancelled. Goodbye!")
            break
        if choice == "6":
            print("Goodbye! Your saved expenses will be here next time.")
            break
        action = actions.get(choice)
        if action is None:
            print("Please choose a menu number from 1 to 6.")
        else:
            try:
                action(expenses)
            except EOFError:
                print("\nInput ended. Goodbye!")
                break
            except KeyboardInterrupt:
                print("\nInput cancelled. Goodbye!")
                break


if __name__ == "__main__":
    main()
