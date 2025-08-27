"""
Category management for financial transactions and budgets.
"""

from database import db, cursor


def add_category():
    while True:
        try:
            category_name = input("What is the name of your new category?")
            cursor.execute(
                '''INSERT INTO categories (name) VALUES (?)''',
                (category_name,)
            )
            db.commit()
            print(f"Category '{category_name}' added successfully!")
            break
        except ValueError:
            print("Invalid name, please try again.")

        print("add_category() function works.")


default_expense_categories = {
    1: "Food",
    2: "Transportation",
    3: "Rent",
    4: "Utilities",
}

cursor.executemany(
    """INSERT OR IGNORE INTO categories(id, name)
               VALUES(?,?)""",
    default_expense_categories.items(),
)
db.commit()

cursor.execute("""SELECT * FROM categories""")
default_expenses = cursor.fetchall()
