#!/usr/bin/env python
"""
test_data.py - Populate the expense tracker database with test data
"""

import sqlite3
from datetime import datetime, timedelta
import random

# Connect to database
db = sqlite3.connect("expenses.db")
cursor = db.cursor()

# Clear existing test data (optional - comment out to keep existing data)
print("Clearing existing data...")
cursor.execute("DELETE FROM expenses")
cursor.execute("DELETE FROM income")
cursor.execute("DELETE FROM budgets")
cursor.execute("DELETE FROM goals")
db.commit()

# Add test categories if they don't exist
test_categories = [
    "Groceries",
    "Entertainment",
    "Gas",
    "Salary",
    "Freelance",
    "Dining Out",
    "Shopping",
    "Bills",
]

for cat in test_categories:
    cursor.execute(
        "INSERT OR IGNORE INTO categories (name) VALUES (?)", (cat,)
    )
db.commit()

# Get category IDs
cursor.execute("SELECT id, name FROM categories")
categories = {name: id for id, name in cursor.fetchall()}

# Add test expenses
print("Adding test expenses...")
expense_data = [
    (categories.get("Groceries", 1), 125.50, "2024-12-01", "Weekly shopping"),
    (categories.get("Gas", 2), 45.00, "2024-12-03", "Tank fill"),
    (categories.get("Dining Out", 1), 35.75, "2024-12-05", "Lunch with team"),
    (categories.get("Entertainment", 2), 15.99, "2024-12-07", "Movie ticket"),
    (categories.get("Groceries", 1), 89.25, "2024-12-10", "Groceries"),
    (categories.get("Bills", 4), 120.00, "2024-12-15", "Internet"),
    (categories.get("Shopping", 1), 67.89, "2024-12-18", "Clothes"),
    (categories.get("Gas", 2), 48.50, "2024-12-20", "Gas"),
]

for cat_id, amount, date, note in expense_data:
    cursor.execute(
        "INSERT INTO expenses (category_id, amount, date, note) VALUES (?, ?, ?, ?)",
        (cat_id, amount, date, note),
    )

# Add test income
print("Adding test income...")
income_data = [
    (categories.get("Salary", 1), 3500.00, "2024-12-01", "Monthly salary"),
    (categories.get("Freelance", 2), 500.00, "2024-12-15", "Website project"),
]

for cat_id, amount, date, note in income_data:
    cursor.execute(
        "INSERT INTO income (category_id, amount, date, note) VALUES (?, ?, ?, ?)",
        (cat_id, amount, date, note),
    )

# Add test budgets
print("Adding test budgets...")
budget_data = [
    (
        categories.get("Groceries", 1),
        400.00,
        "30 days (monthly)",
        "Monthly grocery budget",
        "2024-12-01 - Indefinitely",
        250.00,
        62.5,
    ),
    (
        categories.get("Entertainment", 2),
        100.00,
        "30 days (monthly)",
        "Fun money",
        "2024-12-01 - Indefinitely",
        84.01,
        15.99,
    ),
]

for cat_id, amount, period, note, dates, remaining, percentage in budget_data:
    cursor.execute(
        """INSERT INTO budgets (category_id, amount, period, note, dates, 
           remaining_amount, percentage) VALUES (?, ?, ?, ?, ?, ?, ?)""",
        (cat_id, amount, period, note, dates, remaining, percentage),
    )

# Add test goals
print("Adding test financial goals...")
goals_data = [
    ("Emergency Fund", 5000.00, "2025-06-01", "6 months expenses", "On Track"),
    ("Vacation", 2000.00, "2025-08-01", "Summer trip", "Not Started"),
    ("New Laptop", 1500.00, "2025-03-01", "For work", "Behind Schedule"),
]

for name, target, deadline, notes, status in goals_data:
    cursor.execute(
        """INSERT INTO goals (name, target, deadline, notes, status) 
           VALUES (?, ?, ?, ?, ?)""",
        (name, target, deadline, notes, status),
    )

db.commit()

# Display summary
print("\nTest data added successfully!")
print("=" * 40)

cursor.execute("SELECT COUNT(*) FROM categories")
print(f"Categories: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM expenses")
print(f"Expenses: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM income")
print(f"Income records: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM budgets")
print(f"Budgets: {cursor.fetchone()[0]}")

cursor.execute("SELECT COUNT(*) FROM goals")
print(f"Goals: {cursor.fetchone()[0]}")

# Calculate totals
cursor.execute("SELECT SUM(amount) FROM expenses")
total_expenses = cursor.fetchone()[0] or 0

cursor.execute("SELECT SUM(amount) FROM income")
total_income = cursor.fetchone()[0] or 0

print("\nFinancial Summary:")
print(f"Total Income: ${total_income:.2f}")
print(f"Total Expenses: ${total_expenses:.2f}")
print(f"Balance: ${total_income - total_expenses:.2f}")

db.close()
print("\nDatabase connection closed.")
