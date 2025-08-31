"""
Budget management and tracking functionality.
"""

from datetime import datetime
from categories import (
    fetch_categories,
    show_categories,
    choose_category,
    choose_category_for_viewing,
)
from transactions import ask_continue_filtering
from database import db, cursor
from utils import get_amount, get_note


def calculate_overall_budget():
    """Calculate overall budget."""
    cursor.execute("""SELECT SUM(amount) FROM income""")
    result = cursor.fetchone()
    total_income = result[0] if result[0] is not None else 0

    cursor.execute("""SELECT SUM(amount) FROM expenses""")
    result = cursor.fetchone()
    total_expenses = result[0] if result[0] is not None else 0

    total_budget = total_income - total_expenses

    print("\n=== BUDGET CALCULATION ===")
    print(f"Total Income:    ${total_income:.2f}")
    print(f"Total Expenses:  ${total_expenses:.2f}")
    print("-" * 30)
    print(f"Budget Balance:  ${total_budget:.2f}")

    if total_budget > 0:
        print(f"You have ${total_budget:.2f} remaining")
    elif total_budget < 0:
        print(f"You are over budget by ${abs(total_budget):.2f}")
    else:
        print("You've broken even")


def get_current_spending():
    while True:
        try:
            current_spending = float(
                input("How much have you spent from this budget so far? ")
            )
            if current_spending < 0:
                print("Please input only positive numbers.")
            else:
                return current_spending
        except ValueError:
            print("Invalid option. Please try again.")


def calc_percentage(current_spending, total_amount):
    try:
        percentage = (current_spending / total_amount) * 100
        return percentage
    except ZeroDivisionError:
        print("Cannot divide by zero.")


def calc_remaining_amount(target, current_spending):
    remaining_amount = target - current_spending
    return remaining_amount


def fetch_budget_by_category(category_id):
    """Fetch budgets for a specific category."""
    cursor.execute(
        """SELECT b.id, c.name, b.amount, b.period, b.note, b.dates,
        b.remaining_amount, b.percentage
           FROM budgets b
           JOIN categories c ON b.category_id = c.id
           WHERE b.category_id = ?""",
        (category_id,),
    )
    return cursor.fetchall()


def fetch_all_budgets():
    """Fetch all budgets with category names."""
    cursor.execute(
        """SELECT b.id, c.name, b.amount, b.dates, b.period, b.note,
        b.remaining_amount, b.percentage, b.category_id
           FROM budgets b
           JOIN categories c ON b.category_id = c.id
           ORDER BY b.id"""
    )
    return cursor.fetchall()


def choose_budget_to_edit(budget_list):
    """Display budgets and let user choose one to edit."""
    print("\nSelect a budget to edit:")
    print(
        f"{'ID':<4} {'Category':<15} {'Amount':<12} {'Dates':<30} "
        f"{'Notes':<30} {'% Used':<10} {'Status'}"
    )
    print("-" * 120)

    for (
        bid,
        name,
        amount,
        dates,
        period,
        note,
        remaining_amount,
        percentage,
        category_id,
    ) in budget_list:
        # Calculate display_period for each budget
        if "one-off" in period:
            display_period = "One-off"
        else:
            display_period = period.split("(")[1].rstrip(")").title()

        print(
            f"{bid:<4} {name:<15} ${amount:<11.2f} "
            f"{dates or 'No dates':<30} {note or 'No notes':<30} "
            f"{f'{percentage:.2f}%':<10} {display_period}"
        )

    while True:
        choice = input(
            "\nEnter budget ID to edit (or 'N' to cancel): "
        ).strip()
        if choice.upper() == "N":
            return None
        if choice.isdigit():
            bid = int(choice)
            if bid in {b[0] for b in budget_list}:
                return bid
        print("Invalid choice. Enter a valid budget ID or 'N' to cancel.")


def choose_field_to_edit():
    """Let user choose which field to edit."""
    edit_options = {
        1: "Budget amount",
        2: "Current spending",
        3: "Notes",
        4: "Cancel",
    }

    print("\nWhat would you like to edit?")
    for key, value in edit_options.items():
        print(f"{key}. {value}")

    while True:
        try:
            choice = int(input("\nEnter your choice (1-4): "))
            if choice in edit_options:
                return choice
            else:
                print("Invalid choice. Please select 1-4.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def edit_budget_field(current_budget, field_choice):
    """Edit specific field based on user choice."""
    # current_budget tuple structure:
    # (id, name, amount, dates, period, note, remaining_amount,
    # percentage, category_id)
    (
        budget_id,
        name,
        amount,
        dates,
        period,
        note,
        remaining_amount,
        percentage,
        category_id,
    ) = current_budget

    if field_choice == 1:  # Budget amount
        print(f"\nCurrent budget amount: ${amount:.2f}")
        new_amount = get_amount("budget")
        # Calculate current spending from existing data
        current_spending = amount - remaining_amount
        # Recalculate with new amount
        new_remaining = new_amount - current_spending
        new_percentage = calc_percentage(current_spending, new_amount) or 0
        return (
            budget_id,
            name,
            new_amount,
            dates,
            period,
            note,
            new_remaining,
            new_percentage,
            category_id,
        )

    elif field_choice == 2:  # Current spending
        print(f"\nCurrent spending: ${amount - remaining_amount:.2f}")
        new_spending = get_current_spending()
        # Recalculate remaining and percentage with new spending
        new_remaining = amount - new_spending
        new_percentage = calc_percentage(new_spending, amount) or 0
        return (
            budget_id,
            name,
            amount,
            dates,
            period,
            note,
            new_remaining,
            new_percentage,
            category_id,
        )

    elif field_choice == 3:  # Notes
        print(f"\nCurrent note: {note or 'No note'}")
        new_note = get_note()
        return (
            budget_id,
            name,
            amount,
            dates,
            period,
            new_note,
            remaining_amount,
            percentage,
            category_id,
        )

    elif field_choice == 4:  # Cancel
        return None

    return current_budget


def update_budget_in_database(budget_data):
    """Update budget record in database."""
    # budget_data tuple structure:
    # (id, name, amount, dates, period, note, remaining_amount,
    # percentage, category_id)
    (
        budget_id,
        name,
        amount,
        dates,
        period,
        note,
        remaining_amount,
        percentage,
        category_id,
    ) = budget_data

    cursor.execute(
        """UPDATE budgets
           SET amount = ?, note = ?, remaining_amount = ?, percentage = ?
           WHERE id = ?""",
        (amount, note, remaining_amount, percentage, budget_id),
    )
    db.commit()
    print(f"\nBudget for {name} updated successfully!")
    print(f"New amount: ${amount:.2f}")
    print(f"Remaining: ${remaining_amount:.2f}")
    print(f"Percentage used: {percentage:.2f}%")


def insert_budget(
    category_id,
    amount,
    period,
    start_date,
    end_date,
    note,
    frequency,
    remaining_amount,
    percentage,
):
    """Insert budget into budgets table."""
    if frequency != "one-off":
        dates = f"{start_date.strftime('%Y-%m-%d')} - Indefinitely"
        cursor.execute(
            """INSERT INTO budgets (category_id, amount, period, note, dates,
            remaining_amount, percentage )
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                category_id,
                amount,
                f"{period} days ({frequency})",
                note,
                dates,
                remaining_amount,
                percentage,
            ),
        )
        db.commit()
    else:
        dates = (
            f"{start_date.strftime('%Y-%m-%d')} - "
            f"{end_date.strftime('%Y-%m-%d')}"
        )
        cursor.execute(
            """INSERT INTO budgets (category_id, amount, period, note,
            dates, remaining_amount, percentage)
            VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (
                category_id,
                amount,
                f"{period} days ({frequency})",
                note,
                dates,
                remaining_amount,
                percentage,
            ),
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
    current_spending = get_current_spending()
    remaining_amount = calc_remaining_amount(
        target=amount, current_spending=current_spending
    )
    percentage = calc_percentage(
        current_spending=current_spending, total_amount=amount
    )
    return amount, note, remaining_amount, percentage


def confirm_or_edit_budget(
    amount, frequency, deadline_date, note, transaction_type
):
    """Show summary and allow user to confirm or edit fields."""
    while True:
        print("\nHere is your summary:\n")
        print(
            f"1. Amount - ${amount:.2f}\n2. Frequency - {frequency}\n"
            f"3. Deadline Date - {deadline_date}\n4. "
            f"Note - {note}\n"
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


def recurring_budget():
    recurring_options = ["daily", "weekly", "monthly", "yearly"]
    final_user_choice = ""
    for i, option in enumerate(recurring_options, 1):
        print(f"{i} - {option}")
    user_choice = input(
        "Which of the above options would you like to choose? "
        " Press 'Enter' to choose our default option of monthly or the "
        "number for a specific option: "
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


def get_start_date_only():
    """Get start date for recurring budget."""
    while True:
        start_date_str = input(
            "When should this recurring budget start? Press Enter for today, "
            "or enter date in YYYY-MM-DD format: "
        )
        if start_date_str == "":
            return datetime.today()
        try:
            return datetime.strptime(start_date_str, "%Y-%m-%d")
        except ValueError:
            print("Invalid date. Please try again (format: YYYY-MM-DD).")


def get_start_and_end_date():
    while True:
        start_date_str = input(
            "Please input the starting date in YYYY-MM-DD, or press Enter "
            "for today's date: "
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
            frequency = "one-off"
        elif budget_type == "recurring":
            frequency = recurring_budget()
            deadline_date = "Indefinitely"
            period = 0  # No specific period for recurring
            start_date = get_start_date_only()
            end_date = None  # No end date for recurring budgets
        else:
            # This should never happen as one_off_or_recurring only
            # returns "one-off" or "recurring", but this satisfies the
            # linter
            print(f"Error: Invalid budget type '{budget_type}'")
            continue

        amount, note, remaining_amount, percentage = collect_budget_fields(
            budget_type
        )

        if budget_type == "recurring":
            print(
                "You have created a recurring budget from today, "
                f"paying {frequency}, indefinitely until you cancel."
            )
        action, amount, frequency, deadline_date, note = (
            confirm_or_edit_budget(
                amount, frequency, deadline_date, note, budget_type
            )
        )

        if action == "confirm":
            insert_budget(
                category_id,
                amount,
                period,
                start_date,
                end_date,
                note,
                frequency,
                remaining_amount,
                percentage,
            )
        else:
            print("Budget cancelled. Returning to main menu.")
        break


def view_budget_for_category():
    while True:
        cid = choose_category_for_viewing()
        filtered_category = fetch_budget_by_category(cid)
        if filtered_category:
            print("\n")
            print(
                f"{'ID':<5} {'Name':<15} {'Amount':<12} {'Dates':<30} "
                f"{'Period':<14} {'Note':<25} {'Remaining Amount':<20} "
                f"{'Percentage':<10}"
            )
            print("-" * 150)

            for (
                budget_id,
                name,
                amount,
                period,
                note,
                dates,
                remaining_amount,
                percentage,
            ) in filtered_category:
                # Calculate display_period for each budget
                if "one-off" in period:
                    display_period = period.split("(")[0].strip()
                else:
                    display_period = period.split("(")[1].rstrip(")").title()
                print(
                    f"{budget_id:<5} {name:<15} ${amount:<11.2f} "
                    f"{dates or 'No dates':<30} {display_period:<14} "
                    f"{note or 'No note':<25} {f'{remaining_amount:.2f}':<20} "
                    f"{f'{percentage:.2f}%':<10}"
                )
            break
        else:
            if not ask_continue_filtering():
                break


def edit_budget():
    """Allow user to edit existing budget."""
    while True:
        # Step 1: Get all budgets
        all_budgets = fetch_all_budgets()
        if not all_budgets:
            print("No budgets found to edit.")
            return

        # Step 2: Let user choose which budget to edit
        budget_id = choose_budget_to_edit(all_budgets)
        if budget_id is None:
            return

        # Step 3: Get current budget data
        current_budget = next(b for b in all_budgets if b[0] == budget_id)

        # Step 4: Let user choose what field to edit
        field_choice = choose_field_to_edit()
        if field_choice == 4:  # Cancel
            return

        # Step 5: Edit the chosen field
        updated_budget = edit_budget_field(current_budget, field_choice)
        if updated_budget is None:
            continue

        # Step 6: Update database
        update_budget_in_database(updated_budget)

        # Step 7: Ask if they want to edit another budget
        continue_editing = input(
            "\nWould you like to edit another budget? (y/n): "
        ).lower()
        if continue_editing != "y":
            break
