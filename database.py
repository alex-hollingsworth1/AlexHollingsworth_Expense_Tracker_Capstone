"""
Database management and connection functionality.
"""

import sqlite3

db = sqlite3.connect("expenses.db")
cursor = db.cursor()
cursor.execute("PRAGMA foreign_keys = ON")

# Create categories table to store expense/income categories
db.execute(
    """CREATE TABLE IF NOT EXISTS categories(id INTEGER PRIMARY KEY,
    name TEXT, type TEXT)"""
)

# Create expenses table to store expense transactions
db.execute(
    """CREATE TABLE IF NOT EXISTS expenses(id INTEGER PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id), amount REAL,
    date TEXT, note TEXT)"""
)


# Create income table to store income transactions
db.execute(
    """CREATE TABLE IF NOT EXISTS income(id INTEGER PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id), amount REAL,
    date TEXT, note TEXT)"""
)

# Create budgets table to store budget limits for categories
db.execute(
    """CREATE TABLE IF NOT EXISTS budgets(id INTEGER PRIMARY KEY,
    category_id INTEGER REFERENCES categories(id), period TEXT,
    amount REAL, note TEXT, dates TEXT, remaining_amount REAL,
    percentage REAL)"""
)

# Create goals table to store financial goals
db.execute(
    """CREATE TABLE IF NOT EXISTS goals(id INTEGER PRIMARY KEY,
    name TEXT, target REAL, deadline TEXT, notes TEXT, status TEXT)"""
)
