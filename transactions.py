"""
Transaction management functionality.
"""

from database import db, cursor
from categories import add_category
from utils import get_amount, get_date, get_note


def fetch_categories():
    """Fetch all categories from the database."""
    cursor.execute("SELECT id, name FROM categories")
    return cursor.fetchall()


def show_categories(category_list):
    """Display the list of categories to the user."""
    print("Select a category (or N to create a new one):")
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
            f"1. Amount - ${amount:.2f}\n2. Date Added - {expense_date}\n3. "
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


def update_expense():
    """Update an existing expense amount."""
    # Fetch all expenses with details
    cursor.execute(
        """
        SELECT e.id, c.name, e.amount, e.date, e.note
        FROM expenses e
        JOIN categories c ON e.category_id = c.id
        ORDER BY e.date DESC
    """
    )
    expenses = cursor.fetchall()

    # Check if there are any expenses
    if not expenses:
        print("No expenses found to update.")
        return

    # Show all expenses
    print("\nAll Expenses:")
    print(
        f"{'ID':<5} {'Category':<15} {'Amount':<12} {'Date':<12} {'Note':<25}"
    )
    print("-" * 70)
    for exp_id, category, amount, date, note in expenses:
        print(
            f"{exp_id:<5} {category:<15} ${amount:<11.2f} {date:<12} "
            f"{note or 'No note':<25}"
        )

    # Get expense ID to update
    while True:
        try:
            expense_id = int(input("\nEnter expense ID to update: "))
            # Validate ID exists
            if expense_id not in {e[0] for e in expenses}:
                print(f"Expense ID {expense_id} not found. Please try again.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter a number.")

    # Find the selected expense details
    selected_expense = None
    for expense in expenses:
        if expense[0] == expense_id:
            selected_expense = expense
            break

    # Safety check (should never happen due to validation above)
    if selected_expense is None:
        print("Error: Could not find the selected expense.")
        return

    # Unpack the expense details
    _, category, current_amount, date, note = selected_expense

    # Show current amount
    print(f"\nCurrent amount for {category} expense: ${current_amount:.2f}")

    # Get new amount
    new_amount = get_amount("expense")

    # Confirm update
    confirm = input(
        f"\nUpdate expense from ${current_amount:.2f} to "
        f"${new_amount:.2f}? (y/n): "
    ).lower()
    if confirm != "y":
        print("Update cancelled.")
        return

    # Update the database
    cursor.execute(
        "UPDATE expenses SET amount = ? WHERE id = ?", (new_amount, expense_id)
    )
    db.commit()

    print(f"Expense updated successfully! New amount: ${new_amount:.2f}")


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
    for id, category_id, category_name, amount, date, note in raw_expenses:
        print(f"ID - {id}")
        print(f"Name - {category_name}")
        print(f"Expense Amount - {amount}")
        print(f"Date - {date}")
        print(f"Note - {note}")


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
    for id, category_id, category_name, amount, date, note in raw_income:
        print(f"ID - {id}")
        print(f"Name - {category_name}")
        print(f"Income Amount - {amount}")
        print(f"Date - {date}")
        print(f"Note - {note}")


def choose_category_for_viewing():
    """Get user's choice of category for viewing expenses."""
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
            """SELECT category_id, amount, date, note FROM income
                 WHERE category_id = ?""",
            (category_id,),
        )
    return cursor.fetchall()


def ask_continue_filtering():
    """Ask user if they want to continue filtering after no results
    found."""
    while True:
        user_continue = input(
            "\nNo expenses found for selected criteria. "
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
            else:
                if not ask_continue_filtering():
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
            else:
                if not ask_continue_filtering():
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
            if not ask_continue_filtering():
                break
