# Personal Expense Tracker

A beginner-friendly command-line application for recording and reviewing
personal expenses. It uses Python and JSON, with no external libraries or
database required.

## Project objectives

- Practice Python variables, conditions, loops, lists, dictionaries, and functions.
- Store expense records on the computer.
- Calculate and compare personal spending.

## Features

- Add an expense with amount, category, description, and date.
- View all saved expenses.
- Calculate total spending.
- Filter expenses by **Food**, **Travel**, **Shopping**, **Education**, or **Other**.
- View the selected category's total.
- Delete an expense after confirmation.
- Automatically load and save records in `expenses.json`.
- Validate numbers, categories, descriptions, dates, and menu selections.
- Handle missing, empty, malformed, or invalid JSON data safely.

## Technologies

- Python 3
- JSON
- Git and GitHub

Only Python's standard library is used.

## Installation

1. Install Python 3.
2. Download or clone this project folder.
3. Open a terminal in the project folder.

No package installation is required.

## Run the application

```powershell
python expensetracker.py
```

If `python` is not recognized, try:

```powershell
py expensetracker.py
```

Choose a menu option from 1 to 6. The application saves changes automatically.

## Example usage

```text
Choose an option (1-6): 1

Add an expense
Amount: 12.50
Categories:
  1. Food
  2. Travel
  3. Shopping
  4. Education
  5. Other
Choose a category number: 1
Description: Lunch
Date (YYYY-MM-DD, press Enter for 2026-11-24): 
Expense added and saved.
```

To view the record, choose menu option 2. To calculate all spending, choose
option 3. To filter by category, choose option 4 and enter a category number.
To delete, choose option 5, enter the displayed expense number, and confirm
with `y`.

## Data format

Expenses are stored in `expenses.json` as a JSON list:

```json
[
  {
    "amount": 12.5,
    "category": "Food",
    "description": "Lunch",
    "date": "2026-11-24"
  }
]
```

When `expenses.json` does not exist or is empty, the application starts with
no expenses. A successful save creates or updates the file. Existing valid
records are kept when new expenses are added.

## Project structure

```text
testprgrm/
├── expensetracker.py  # Main application
├── expenses.json      # Saved expense data
├── README.md          # Project documentation
└── .gitignore         # Git exclusion rules
```

## Future improvements

- Add monthly summaries and spending limits.
- Export reports to CSV.
- Add automated unit tests.
- Add editing of existing expenses.

## GitHub preparation

The project does not push or upload anything automatically. When ready:

```powershell
git add expensetracker.py README.md .gitignore
git commit -m "Complete Personal Expense Tracker"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPOSITORY.git
git push -u origin main
```

Replace `YOUR-USERNAME` and `YOUR-REPOSITORY` with your GitHub details. Avoid
publishing `expenses.json` if it contains private personal spending records.
