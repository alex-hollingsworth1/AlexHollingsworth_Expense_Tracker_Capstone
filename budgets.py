"""
Budget management and tracking functionality.
"""

from datetime import datetime

from transactions import (
    fetch_categories,
    show_categories,
    choose_category,
    get_amount,
    get_note,
    choose_category_for_viewing,
    ask_continue_filtering,
)
from database import db, cursor


def fetch_budget_by_category(category_id):
    """Fetch budgets for a specific category."""
    cursor.execute(
        """SELECT b.id, c.name, b.amount, b.period, b.note
           FROM budgets b
           JOIN categories c ON b.category_id = c.id
           WHERE b.category_id = ?""",
        (category_id,),
    )
    return cursor.fetchall()


def insert_budget(category_id, amount, period, deadline_date, note, frequency):
    """Insert budget into budgets table."""
    cursor.execute(
        """INSERT INTO budgets (category_id, amount, period, note)
           VALUES (?, ?, ?, ?)""",
        (category_id, amount, f"{period} days ({frequency})", note),
    )
    db.commit()
    print(f"\n${amount:.2f} budget added successfully!")


def get_budget_end_date():
    """Get budget end date from user (no default to today)."""
    while True:
        date_str = input(
            "Please input the ending date for this budget (YYYY-MM-DD): "
        )
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date. Please try again (format: YYYY-MM-DD).")


def collect_budget_fields(transaction_type):
    """Collect all transaction details from the user."""
    amount = get_amount(transaction_type)
    note = get_note()
    return amount, note


def confirm_or_edit_budget(
    amount, frequency, deadline_date, note, transaction_type
):
    """Show summary and allow user to confirm or edit fields."""
    while True:
        print("Here is your summary:\n")
        print(
            f"1. Amount - ${amount}\n2. Frequency - {frequency}\n"
            f"3. Deadline Date - {deadline_date}\n4. "
            f"Note - {note}"
        )
        choice = input(
            "Enter Y to confirm, N to cancel, or 1-4 to edit: "
        ).lower()
        if choice == "y":
            return ("confirm", amount, frequency, deadline_date, note)
        if choice == "n":
            return ("cancel", amount, frequency, deadline_date, note)
        if choice == "1":
            amount = get_amount(transaction_type)
        elif choice == "2":
            # Add function to edit frequency here
            print("Frequency editing not implemented yet")
        elif choice == "3":
            deadline_date = get_budget_end_date()
        elif choice == "4":
            note = get_note()
        else:
            print("Invalid option. Please try again.")


def one_off_or_recurring(category_id):
    while True:
        user_choice = input(
            "Would you like to make this a one-off or recurring budget? "
        ).lower()
        if user_choice == "one-off" or user_choice == "one off":
            return "one-off"
        elif user_choice == "recurring":
            return "recurring"
        else:
            print("Invalid choice, please try again.")


def one_off_budget():
    start_date, end_date = get_start_and_end_date()
    period = (end_date - start_date).days
    print(f"Budget period: {period} days")
    return period


def recurring_budget():
    recurring_options = ["daily", "weekly", "monthly", "yearly"]
    final_user_choice = ""
    for i, option in enumerate(recurring_options, 1):
        print(f"{i} - {option}")
    user_choice = input(
        "Which of the above options would you like to choose? "
        " Press 'Enter' to choose our default option of monthly or the "
        "number for a specific option."
    )
    if user_choice == "":
        final_user_choice = "monthly"
        return final_user_choice

    while True:
        if user_choice.isdigit() and int(user_choice) in range(
            1, len(recurring_options) + 1
        ):
            final_user_choice = recurring_options[int(user_choice) - 1]
            return final_user_choice
        else:
            print("Invalid input. Please try again")
            user_choice = input("Which option would you like to choose? ")


def get_start_and_end_date():
    while True:
        start_date_str = input(
            "Please input the starting date in YYYY-MM-DD, or press Enter "
            " for today's date: "
        )
        if start_date_str == "":
            start_date = datetime.today()
            break
        try:
            start_date = datetime.strptime(start_date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date. Please try again (format: YYYY-MM-DD).")

    while True:
        end_date_str = input("Please input the ending date in YYYY-MM-DD: ")
        try:
            end_date = datetime.strptime(end_date_str, "%Y-%m-%d")
            break
        except ValueError:
            print("Invalid date. Please try again (format: YYYY-MM-DD).")

    return start_date, end_date


def set_budget():
    while True:
        cats = fetch_categories()
        show_categories(cats)

        category_id = choose_category(cats)
        if category_id is None:
            # Either invalid input or user added a new category.
            # Loop refreshes the list and shows menu again.
            continue

        budget_type = one_off_or_recurring(category_id)

        if budget_type == "one-off":
            start_date, end_date = get_start_and_end_date()
            period = (end_date - start_date).days
            deadline_date = end_date.strftime("%Y-%m-%d")
            # deadline_date = get_budget_end_date()
            frequency = "one-off"
        elif budget_type == "recurring":
            frequency = recurring_budget()
            deadline_date = "Indefinitely"
            period = 0  # No specific period for recurring
            print(
                "You have created a recurring budget from today, "
                f"paying {frequency}, indefinitely until you cancel."
            )

        amount, note = collect_budget_fields(budget_type)
        action, amount, frequency, deadline_date, note = (
            confirm_or_edit_budget(
                amount, frequency, deadline_date, note, budget_type
            )
        )

        if action == "confirm":
            insert_budget(
                category_id, amount, period, deadline_date, note, frequency
            )
        else:
            print("Income cancelled. Returning to main menu.")
        break


def view_budget_for_category():
    while True:
        cid = choose_category_for_viewing()
        filtered_category = fetch_budget_by_category(cid)
        if filtered_category:
            print("\n")
            print(
                f"{'ID':<5} {'Name':<15} {'Amount':<12} {'Period':<18} "
                f"{'Note':<25}"
            )
            print("-" * 75)
            for (
                budget_id,
                name,
                amount,
                period,
                note,
            ) in filtered_category:
                print(
                    f"{budget_id:<5} {name:<15} ${amount:<11.2f} {period:<21} "
                    f"{note or 'No note':<25}"
                )
            print("\n")
            break
            # TODO: Format output display:
            # - For recurring budgets: show period as 'weekly',
            # 'monthly', etc.
            #   and calculate expenses from current period start
            # - For one-off budgets: show actual start/end dates
            #   and calculate expenses within that date range
            # - Display: budget amount, period type, total expenses
            # in period,
            #   remaining amount, and percentage used
            break
        else:
            if not ask_continue_filtering():
                break
