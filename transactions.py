"""
Transaction management functionality.
"""

from datetime import datetime
from database import db, cursor
from categories import add_category


def get_date(transaction_type):
    """Get and validate date input from user."""
    while True:
        date_str = input(
            f"Please input a date for this {transaction_type}. Press enter"
            " for today's date, or enter a date in format YYYY-MM-DD: "
        )
        if date_str == "":
            return datetime.today().strftime("%Y-%m-%d")
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date. Please try again (format: YYYY-MM-DD).")


def get_amount(transaction_type):
    """Get and validate amount input from user."""
    while True:
        try:
            amount = float(
                input(
                    f"Please type the amount for the {transaction_type} "
                    "payment here: "
                )
            )
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a valid number.")


def get_note():
    """Get optional note from user."""
    user_optional_note = input(
        "Would you like to write an optional note? y/n: "
    ).lower()
    if user_optional_note == "y":
        return input("Please write your optional note: ")
    elif user_optional_note == "n":
        return ""
    else:
        print("Invalid option, no note will be added.")
        return ""


def fetch_categories():
    """Fetch all categories from the database."""
    cursor.execute("SELECT id, name FROM categories")
    return cursor.fetchall()


def show_categories(category_list):
    """Display the list of categories to the user."""
    print("Select a category (or N to create a new one):\n")
    for cat_id, name in category_list:
        print(f"{cat_id}: {name}")


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


def collect_fields(transaction_type):
    """Collect all transaction details from the user."""
    amount = get_amount(transaction_type)
    date = get_date(transaction_type)
    note = get_note()
    return amount, date, note


def confirm_or_edit(amount, expense_date, note, transaction_type):
    """Show summary and allow user to confirm or edit fields."""
    while True:
        print("Here is your summary:\n")
        print(
            f"1. Amount - ${amount}\n2. Date Added - {expense_date}\n3. "
            f"Note - {note}"
        )
        # COULD IMPLEMENT IT BETTER WITH MULTIPLE DIFFERENT USE CASES
        # FOR OTHER FUNCTIONS
        choice = input(
            "Enter Y to confirm, N to cancel, or 1-3 to edit: "
        ).lower()
        if choice == "y":
            return ("confirm", amount, expense_date, note)
        if choice == "n":
            return ("cancel", amount, expense_date, note)
        if choice == "1":
            amount = get_amount(transaction_type)
        elif choice == "2":
            expense_date = get_date(transaction_type)
        elif choice == "3":
            note = get_note()
        else:
            print("Invalid option. Please try again.")


def insert_transaction(category_id, amount, date, note, transaction_type):
    """Insert transaction into expenses or income table."""
    transaction_config = {
        "expense": {"table": "expenses", "name": "Expense"},
        "income": {"table": "income", "name": "Income"},
    }

    config = transaction_config.get(
        transaction_type, {"table": "expenses", "name": "Transaction"}
    )

    cursor.execute(
        f"""INSERT INTO {config['table']} (amount, date, note, category_id)
           VALUES (?, ?, ?, ?)""",
        (amount, date, note, category_id),
    )
    db.commit()
    print(f"\n${amount:.2f} {config['name'].lower()} added successfully!")


def add_expense():
    """Main function to add a new expense with full user interaction."""
    while True:
        cats = fetch_categories()
        show_categories(cats)

        category_id = choose_category(cats)
        if category_id is None:
            # Either invalid input or user added a new category.
            # Loop refreshes the list and shows menu again.
            continue

        amount, expense_date, note = collect_fields("expense")
        action, amount, expense_date, note = confirm_or_edit(
            amount, expense_date, note, "expense"
        )

        if action == "confirm":
            insert_transaction(
                category_id, amount, expense_date, note, "expense"
            )
        else:
            print("Expense cancelled. Returning to main menu.")
        break


def filter_expenses():
    """Get user's preference for filtering expenses."""
    user_expense = input("Filter by category? y/n: ")
    while True:
        if user_expense.lower() == "y":
            return True
        elif user_expense.lower() == "n":
            print("Here are all the expenses:")
            return False
        else:
            print("Invalid option, please try again.")
            user_expense = input("Would you like to filter expenses? y/n: ")


def filter_income():
    """Get user's preference for filtering expenses."""
    user_income = input("Filter by category? y/n: ")
    while True:
        if user_income.lower() == "y":
            return True
        elif user_income.lower() == "n":
            print("Here is your income in one batch:")
            return False
        else:
            print("Invalid option, please try again.")
            user_income = input("Would you like to filter income? y/n: ")


def fetch_raw_expenses():
    """Fetch all expenses from the database."""
    cursor.execute(
        """
        SELECT e.id, e.category_id, c.name as category_name, e.amount,
        e.date, e.note
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
    """
    )
    raw_expenses = cursor.fetchall()
    print(raw_expenses)


def choose_category_for_viewing():
    """Get user's choice of category for viewing expenses."""
    cats = fetch_categories()
    show_categories(cats)
    while True:
        try:
            user_cat = input("Which category would you like to filter by? ")
            cid = int(user_cat)
            if cid in {c[0] for c in cats}:
                return cid
            else:
                print(
                    "Invalid category ID. Please choose from the list above."
                )
        except ValueError:
            print("Invalid entry, please enter a number.")


def fetch_expenses_by_category(category_id):
    """Fetch expenses for a specific category."""
    cursor.execute(
        """SELECT category_id, amount, date, note FROM expenses
           WHERE category_id = ?""",
        (category_id,),
    )
    return cursor.fetchall()


def fetch_income_by_category(category_id):
    """Fetch income for a specific category."""
    cursor.execute(
        """SELECT category_id, amount, date, note FROM income
           WHERE category_id = ?""",
        (category_id,),
    )
    return cursor.fetchall()


def fetch_transaction_by_category(category_id, transaction_type):
    """Fetch transactions from expenses or income tables by category."""
    table_name = "expenses" if transaction_type == "expense" else "income"
    cursor.execute(
        f"""SELECT category_id, amount, date, note FROM {table_name}
           WHERE category_id = ?""",
        (category_id,),
    )
    return cursor.fetchall()


def ask_continue_filtering():
    """Ask user if they want to continue filtering after no results
    found."""
    while True:
        user_continue = input(
            "No expenses found for selected criteria. "
            "Would you like to try filtering another category? y/n: "
        ).lower()
        if user_continue == "y":
            return True
        elif user_continue == "n":
            print("Returning to main menu.")
            return False
        else:
            print("Invalid option. Please try again.")


def view_expenses():
    while True:
        filter_choice = filter_expenses()
        if not filter_choice:
            fetch_raw_expenses()
            break
        else:
            cid = choose_category_for_viewing()
            filtered_category = fetch_transaction_by_category(cid, "expense")
            if filtered_category:
                print(filtered_category)
            else:
                if not ask_continue_filtering():
                    break


def view_expenses_by_category():
    while True:
        cid = choose_category_for_viewing()
        filtered_category = fetch_expenses_by_category(cid)
        if filtered_category:
            print(filtered_category)
            break
        else:
            if not ask_continue_filtering():
                break


def add_income():
    while True:
        cats = fetch_categories()
        show_categories(cats)
        category_id = choose_category(cats)
        if category_id is None:
            # Either invalid input or user added a new category.
            # Loop refreshes the list and shows menu again.
            continue

        amount, income_date, note = collect_fields("income")
        action, amount, income_date, note = confirm_or_edit(
            amount, income_date, note, "income"
        )

        if action == "confirm":
            insert_transaction(
                category_id, amount, income_date, note, "income"
            )
        else:
            print("Income cancelled. Returning to main menu.")
        break


def view_income():
    while True:
        filter_choice = filter_income()
        if not filter_choice:
            fetch_raw_expenses()
            break
        else:
            cid = choose_category_for_viewing()
            filtered_category = fetch_transaction_by_category(cid, "income")
            if filtered_category:
                print(filtered_category)
            else:
                if not ask_continue_filtering():
                    break


def view_income_by_category():
    print("view_income_by_category() function worked")
