"""
Category management for financial transactions and budgets.
"""

from database import db, cursor


def choose_category(category_list):
    """Get user's category choice and validate it."""
    user_input = input("Please type your choice: ").strip()
    if user_input.upper() == "N":
        add_category()
        return None  # signal: categories changed, reshow menu
    if user_input.isdigit():
        cid = int(user_input)
        if cid in {c[0] for c in category_list}:
            return cid
    print("Invalid input. Enter a valid category number or 'N'.")
    return None


def choose_category_for_viewing():
    """Get user's choice of category for viewing transactions."""
    cats = fetch_categories()
    show_categories(cats)
    while True:
        try:
            user_cat = input("\nWhich category would you like to filter by? ")
            cid = int(user_cat)
            if cid in {c[0] for c in cats}:
                return cid
            else:
                print(
                    "Invalid category ID. Please choose from the list above."
                )
        except ValueError:
            print("Invalid entry, please enter a number.")


def show_categories(category_list):
    """Display the list of categories to the user."""
    print("Select a category (or N to create a new one):")
    for cat_id, name in category_list:
        print(f"{cat_id}: {name}")


def fetch_categories():
    """Fetch all categories from the database."""
    cursor.execute("SELECT id, name FROM categories")
    return cursor.fetchall()


def delete_category():
    """Delete a category from the database."""
    # Step 1: Fetch and show all categories
    cats = fetch_categories()
    if not cats:
        print("No categories found.")
        return

    show_categories(cats)

    # Step 2: Ask if they want to delete
    choice = input("\nDo you want to delete a category? (y/n): ").lower()
    if choice != "y":
        print("Deletion cancelled.")
        return

    # Step 3: Get category ID with validation
    while True:
        try:
            cat_id = int(input("Enter the ID of the category to delete: "))

            # Validate: no negative or zero
            if cat_id <= 0:
                print("Please enter a positive number.")
                continue

            # Validate: ID exists in list
            if cat_id not in {c[0] for c in cats}:
                print(f"Category ID {cat_id} not found. Please try again.")
                continue

            break  # Valid ID entered

        except ValueError:
            print("Invalid input. Please enter a number.")

    # Step 4: Show category details and confirm
    cursor.execute("SELECT name FROM categories WHERE id = ?", (cat_id,))
    category_name = cursor.fetchone()[0]

    print(f"\nYou selected: {category_name} (ID: {cat_id})")
    confirm = input(
        "Are you sure you want to delete this category? (y/n): "
    ).lower()

    if confirm != "y":
        print("Deletion cancelled.")
        return

    # Step 5: Check for existing transactions (important!)
    cursor.execute(
        "SELECT COUNT(*) FROM expenses WHERE category_id = ?", (cat_id,)
    )
    expense_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM income WHERE category_id = ?", (cat_id,)
    )
    income_count = cursor.fetchone()[0]

    if expense_count > 0 or income_count > 0:
        print(
            f"\nError: Cannot delete '{category_name}' - it has "
            f"{expense_count} expenses and {income_count} income records."
        )
        print("Please delete or reassign these transactions first.")
        return  # Exit without deleting

    # Step 6: Delete the category
    cursor.execute("DELETE FROM categories WHERE id = ?", (cat_id,))
    db.commit()

    print(f"Category '{category_name}' deleted successfully!")


def add_category():
    while True:
        try:
            category_name = input("What is the name of your new category?\n")
            cursor.execute(
                """INSERT INTO categories (name) VALUES (?)""",
                (category_name,),
            )
            db.commit()
            print(f"Category '{category_name}' added successfully!")
            break
        except ValueError:
            print("Invalid name, please try again.")


default_categories = {
    1: "Food",
    2: "Transportation",
    3: "Rent",
    4: "Utilities",
}

cursor.executemany(
    """INSERT OR IGNORE INTO categories(id, name)
               VALUES(?,?)""",
    default_categories.items(),
)
db.commit()

cursor.execute("""SELECT * FROM categories""")
default_expenses = cursor.fetchall()
