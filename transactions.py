"""
Transaction management functionality.
"""

from database import db, cursor
from categories import (
    fetch_categories,
    show_categories,
    choose_category,
    choose_category_for_viewing,
)
from utils import get_amount, get_date, get_note, print_raw_transactions_table


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
            f"1. Amount - ${amount:.2f}\n2. Date Added - {expense_date}\n3. "
            f"Note - {note}"
        )
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
    """Insert transaction into expenses, income, or budgets table."""
    transaction_config = {
        "expense": {"table": "expenses", "name": "Expense"},
        "income": {"table": "income", "name": "Income"},
        "budget": {"table": "budgets", "name": "Budget"},
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


def update_transaction(transaction_type):
    """Update an existing expense amount."""
    # Map transaction type to table and display name
    type_config = {
        "expense": {"table": "expenses", "name": "Expense"},
        "income": {"table": "income", "name": "Income"},
    }

    if transaction_type not in type_config:
        print("Invalid transaction type.")
        return

    config = type_config[transaction_type]

    # Fetch all transactions - note the table name is hardcoded in each
    # query
    if transaction_type == "expense":
        cursor.execute(
            """
            SELECT e.id, c.name, e.amount, e.date, e.note
            FROM expenses e
            JOIN categories c ON e.category_id = c.id
            ORDER BY e.id
        """
        )
    else:  # income
        cursor.execute(
            """
            SELECT i.id, c.name, i.amount, i.date, i.note
            FROM income i
            JOIN categories c ON i.category_id = c.id
            ORDER BY i.id
        """
        )
    transactions = cursor.fetchall()

    # Check if there are any transactions
    if not transactions:
        print(f"No {config['name'].lower()} found to update.")
        return

    print(
        f"{'ID':<5} {'Category':<15} {'Amount':<12} {'Date':<12} {'Note':<25}"
    )
    print("-" * 70)
    for id, category, amount, date, note in transactions:
        print(
            f"{id:<5} {category:<15} ${amount:<11.2f} {date:<12} "
            f"{note or 'No note':<25}"
        )

    # Get transaction ID to update
    while True:
        try:
            transaction_id = int(input("\nEnter ID to update: "))
            # Validate ID exists
            if transaction_id not in {e[0] for e in transactions}:
                print(
                    f"{config['name']} ID {transaction_id} not found. "
                    "Please try again."
                )
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Find the selected transaction details
    selected_expense = None
    for transaction in transactions:
        if transaction[0] == transaction_id:
            selected_expense = transaction
            break

    # Validation above ensures this exists, but linter needs this check
    if selected_expense is None:
        print(f"Error: Could not find the selected {config['name'].lower()}.")
        return

    # Unpack the expense details
    _, category, current_amount, date, note = selected_expense

    # Show current amount
    print(
        f"\nCurrent amount for {category} {config['name'].lower()}: "
        f"${current_amount:.2f}"
    )

    # Get new amount
    new_amount = get_amount(config["name"].lower())

    # Confirm update
    confirm = input(
        f"\nUpdate {config['name'].lower()} from ${current_amount:.2f} to "
        f"${new_amount:.2f}? (y/n): "
    ).lower()
    if confirm != "y":
        print("Update cancelled.")
        return

    if transaction_type == "expense":
        cursor.execute(
            "UPDATE expenses SET amount = ? WHERE id = ?",
            (new_amount, transaction_id),
        )
    else:
        cursor.execute(
            "UPDATE income SET amount = ? WHERE id = ?",
            (new_amount, transaction_id),
        )
    db.commit()

    print(
        f"{config['name']} updated successfully! New amount: ${new_amount:.2f}"
    )


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
            print("\nHere are all the expenses:")
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
    print_raw_transactions_table(raw_expenses, "expense")


def fetch_raw_income():
    """Fetch all income from the database."""
    cursor.execute(
        """
        SELECT i.id, i.category_id, c.name as category_name, i.amount,
        i.date, i.note
        FROM income i
        JOIN categories c ON i.category_id = c.id
    """
    )
    raw_income = cursor.fetchall()
    print_raw_transactions_table(raw_income, "income")


def fetch_expenses_by_category(category_id):
    """Fetch expenses for a specific category."""
    cursor.execute(
        """SELECT e.id, c.name, e.amount, e.date, e.note
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        WHERE e.category_id = ?""",
        (category_id,),
    )
    return cursor.fetchall()


def fetch_income_by_category(category_id):
    """Fetch income for a specific category."""
    cursor.execute(
        """SELECT i.id, c.name, i.amount, i.date, i.note
           FROM income i
           JOIN categories c ON i.category_id = c.id
           WHERE i.category_id = ?""",
        (category_id,),
    )
    return cursor.fetchall()


def fetch_transaction_by_category(category_id, transaction_type):
    """Fetch transactions from expenses or income tables by category."""
    if transaction_type == "expense":
        cursor.execute(
            """SELECT e.id, c.name, e.amount, e.date, e.note
                 FROM expenses e
                 JOIN categories c ON e.category_id = c.id
                 WHERE e.category_id = ?""",
            (category_id,),
        )
    else:  # income
        cursor.execute(
            """SELECT i.id, c.name, i.amount, i.date, i.note
                FROM income i
                JOIN categories c ON i.category_id = c.id
                WHERE i.category_id = ?""",
            (category_id,),
        )
    return cursor.fetchall()


def ask_continue_filtering(transaction_type):
    """Ask user if they want to continue filtering after no results
    found."""
    while True:
        user_continue = input(
            f"\nNo {transaction_type} found for selected criteria. "
            f"Would you like to try viewing {transaction_type} again? y/n: "
        ).lower()
        if user_continue == "y":
            return True
        elif user_continue == "n":
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
                print("\n")
                print(
                    f"{'ID':<5} {'Name':<15} {'Amount':<12} {'Date':<14} "
                    f"{'Note':<25}"
                )
                print("-" * 75)
                for (
                    expense_id,
                    name,
                    amount,
                    date,
                    note,
                ) in filtered_category:
                    print(
                        f"{expense_id:<5} {name:<15} ${amount:<11.2f} "
                        f"{date:<14} {note or 'No note':<25}"
                    )
                print("\n")
                break
            else:
                if not ask_continue_filtering("expenses"):
                    break


def view_expenses_by_category():
    while True:
        cid = choose_category_for_viewing()
        filtered_category = fetch_expenses_by_category(cid)
        if filtered_category:
            print("\n")
            print(
                f"{'ID':<5} {'Name':<15} {'Amount':<12} {'Date':<14} "
                f"{'Note':<25}"
            )
            print("-" * 75)
            for (
                expense_id,
                name,
                amount,
                date,
                note,
            ) in filtered_category:
                print(
                    f"{expense_id:<5} {name:<15} ${amount:<11.2f} {date:<14} "
                    f"{note or 'No note':<25}"
                )
            print("\n")
            break
        else:
            if not ask_continue_filtering("expenses"):
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
            fetch_raw_income()
            break
        else:
            cid = choose_category_for_viewing()
            filtered_category = fetch_transaction_by_category(cid, "income")
            if filtered_category:
                print("\n")
                print(
                    f"{'ID':<5} {'Name':<15} {'Amount':<12} {'Date':<14} "
                    f"{'Note':<25}"
                )
                print("-" * 75)
                for (
                    expense_id,
                    name,
                    amount,
                    date,
                    note,
                ) in filtered_category:
                    print(
                        f"{expense_id:<5} {name:<15} ${amount:<11.2f} "
                        f"{date:<14} {note or 'No note':<25}"
                    )
                print("\n")
                break
            else:
                if not ask_continue_filtering("income"):
                    break


def view_income_by_category():
    while True:
        cid = choose_category_for_viewing()
        filtered_category = fetch_income_by_category(cid)
        if filtered_category:
            print("\n")
            print(
                f"{'ID':<5} {'Name':<15} {'Amount':<12} {'Date':<14} "
                f"{'Note':<25}"
            )
            print("-" * 75)
            for (
                expense_id,
                name,
                amount,
                date,
                note,
            ) in filtered_category:
                print(
                    f"{expense_id:<5} {name:<15} ${amount:<11.2f} {date:<14} "
                    f"{note or 'No note':<25}"
                )
            print("\n")
            break
        else:
            if not ask_continue_filtering("income"):
                break
