# Expense & Budget Tracker

A command-line expense tracker application built in **Python** with an **SQLite database** for the **HyperionDev Software Engineering Bootcamp Capstone Project (Option 1)**.

---

## Requirements Met
All 11 requirements from the Capstone PDF successfully implemented:

- Add new expense/income categories to database  
- Track spending and income  
- View expense/income categories  
- View expenses/income by category
- Set budget for a category
- View budget for a category
- Set financial goals  
- View progress towards financial goals  
- SQLite database connection and tables  
- Menu system (extended with 14 options vs 11 required)  
- Calculate user's budget based on income and expenses  

---

## Additional Features (Beyond Requirements)
- Update transaction amounts (Option 7): Modify existing expense/income records  
- Edit/Update budget (Option 13): Change budget amounts, spending, or notes  
- Recurring budgets: Support for daily/weekly/monthly/yearly periods  
- One-off budgets: Time-bound with start/end dates  
- Input validation: Robust error handling across all inputs  
- Test data generator: Quickly populate the database with sample data  
- Delete category function: Admin-only, not exposed in menu, with safeguards  

---

## Installation & Setup

### Prerequisites
- Python 3.x  
- SQLite3 (included with Python)

### Getting Started

```bash
# Clone repository
git clone [your-repo-url]
cd expense-tracker

# (Optional) Populate with test data
python test_data.py

# Start the application
python main.py
```

---

# Usage
The application provides a command-line menu system with 14 available options:

- Add expense  
- View expenses  
- View expenses by category  
- Add income  
- View income  
- View income by category  
- Update transaction  
- Set budget for a category  
- View budget for a category  
- Set financial goals  
- View progress towards financial goals  
- Calculate overall budget  
- Edit/Update budget  
- Quit  

---

## Key Features

### Transaction Management
- Add expenses and income with category, date, and optional note  
- View all transactions or filter by category  
- Update existing transaction amounts  

### Budget System
- Create one-off or recurring budgets (daily/weekly/monthly/yearly)  
- Track spending percentage and remaining amount  
- Edit budget amount, current spending, or notes  

### Goal Tracking
- Set financial goals with target amounts and deadlines  
- View progress, remaining amount, and days remaining  
- Status options: On Track, Not Started, Behind Schedule, Completed  

### Database Schema
- categories - expense/income categories  
- expenses - expense transactions  
- income - income transactions  
- budgets - category budgets with remaining/percentage fields  
- goals - financial goals with deadline and status  
- Foreign key constraints enforced with `PRAGMA foreign_keys = ON` for data integrity  

---

## Testing

```bash
python test_data.py   # Creates sample categories, transactions, budgets, and goals
python main.py        # Start testing with populated data
```

---

## Design Decisions
- Modular architecture: Each feature separated into its own module with relevant imports.  
- Foreign key enforcement: Prevents orphaned records and maintains table relationships  
- Utility functions: Centralised validation reduces duplication  
- Table formatting: Consistent, readable transaction displays  
- Category protection: Cannot delete categories with linked records  

---

## Implementation Notes
- Redundant functions:  
  - view_expenses_by_category and view_income_by_category were implemented to explicitly meet requirements, though filtering is already available in view_expenses and view_income.  

- Admin functions:  
  - delete_category exists but is not exposed in the menu. It prevents deletion of categories with linked transactions.  

- Design choices explained:  
  - .get() used in test_data.py to safely fetch categories with defaults, avoiding KeyError.  
  - Chained commands used in several places for concise calculations and inline updates.  
  - next() in budgets.py quickly finds the first matching budget tuple by ID.  
  - Triple-quoted strings for multi-line SQL queries (better readability); single quotes for short queries.  

- Test data: 
  - The test_data.py file includes automatically generated sample data to ensure the system could be thoroughly tested with varied transactions, dates, and amounts.

---

## Known Limitations
- No data export functionality  
- Single-user system (no multi-user support)  
- Command-line only (no GUI)  
- 30-character limit on notes (for CLI database viewing purposes) 

---

## Author
Alex Hollingsworth  
HyperionDev Software Engineering Bootcamp  
Capstone Project - 1st September 2025
