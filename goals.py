"""
Financial goal setting and tracking functionality.

PROJECT REQUIREMENTS - Expense & Budget Tracker:
✅ Completed:
- Add new expense/income categories to database
- Track spending and income
- View expense/income categories
- View expenses/income by category
- Set budget for a category
- View budget for a category
- Set financial goals
- View progress towards financial goals (via prompting)
- SQLite database connection and tables
- Menu system (1-11 options)

🔧 To verify/consider:
- Update an expense amount (may need separate function)
- Delete expense/income categories (have add, may need delete)
- Calculate user's budget based on income and expenses

NOTE: For saved_amount in goals - requirements don't explicitly need
database storage. Current prompting approach meets "View progress"
requirement. Could enhance with database storage to show UPDATE skills
if time permits.
"""

from datetime import datetime
from transactions import get_note
from database import db, cursor


def ask_continue_updating():
    """Ask user if they want to continue updating goals."""
    while True:
        user_continue = input(
            "Would you like to update another goal? y/n: "
        ).lower()
        if user_continue == "y":
            return True
        elif user_continue == "n":
            print("Returning to main menu.")
            return False
        else:
            print("Invalid option. Please try again.")


def update_progress(goal_id):
    # Show user the full details of the goal they have selected
    cursor.execute(
        """SELECT id, name, target, deadline, notes, status FROM goals
           WHERE id = ?""",
        (goal_id,)
    )
    goal_details = cursor.fetchone()

    # Print out goal with the ID requested by the user
    print("Here are the details from your goals with this specific ID:")
    show_goals(goal_list=goal_details)
    saved_amount = float(
        input("\nHow much have you saved so far for this goal? ")
    )
    remaining_amount = goal_details[2] - saved_amount
    deadline = datetime.strptime(
        goal_details[3], "%Y-%m-%d"
    )  # Convert string to datetime
    today = datetime.now()
    days_remaining = (
        deadline - today
    ).days  # This gives you the number of days
    show_remaining_amount = input(
        "Would you like a new table showing the remaining amount and how "
        " many days are remaining?"
    ).lower()

    while True:
        if show_remaining_amount == "y":
            print("\nUpdated Goal Progress:")
            print(f"Goal: {goal_details[1]}")
            print(f"Target: ${goal_details[2]:.2f}")
            print(f"Saved: ${saved_amount:.2f}")
            print(f"Remaining: ${remaining_amount:.2f}")
            if days_remaining < 0:
                print(
                    f"Days remaining: OVERDUE by {abs(days_remaining)} days."
                )
            else:
                print(f"Days remaining: {days_remaining} days")
            print(f"Progress: {(saved_amount/goal_details[2]*100):.1f}%")
            # TODO: Could add daily/weekly savings needed:
            # remaining_amount / days_remaining
            break
        elif show_remaining_amount == "n":
            break
        else:
            print("Please enter valid option.")


def fetch_goals():
    """Fetch all goals from the database."""
    cursor.execute(
        "SELECT id, name, target, deadline, notes, status FROM goals"
    )
    return cursor.fetchall()


def show_goals(goal_list):
    """Display the list of goals to the user."""
    print("Your Financial Goals:\n")
    for id, name, target, deadline, notes, status in goal_list:
        print(f"{id}: {name} - ${target:.2f} by {deadline} [{status}]")
        if notes:
            print(f"   Note: {notes}")


def pick_goals(goal_list):
    """Display the list of goals to the user."""
    show_goals(goal_list)
    user_choice = input(
        "Select goal ID to view or update progress or N to return."
    )
    if user_choice.upper() == "N":
        return None
    elif user_choice.isdigit():
        goal_id = int(user_choice)
        if goal_id in {c[0] for c in goal_list}:
            return goal_id


def insert_goal(goal_name, target, deadline_date, notes, status):
    """Insert goal into goals table."""
    cursor.execute(
        """INSERT INTO goals (name, target, deadline, notes, status)
           VALUES (?, ?, ?, ?, ?)""",
        (goal_name, target, deadline_date, notes, status),
    )
    db.commit()
    print(f"\nGoal '{goal_name}' for ${target:.2f} added successfully!")


def confirm_or_edit_goals(
    goal_name, goal_amount, goal_deadline, goal_notes, goal_status
):
    """Show summary and allow user to confirm or edit fields."""
    while True:
        print("Here is your summary:\n")
        print(
            f"1. Goal name - ${goal_name}\n2. Target - {goal_amount:.2f}\n "
            f"3. Deadline Date - {goal_deadline}\n4. "
            f"Notes - {goal_notes}\n5. Status - {goal_status}"
        )
        choice = input(
            "Enter Y to confirm, N to cancel, or 1-5 to edit: "
        ).lower()
        if choice == "y":
            return (
                "confirm",
                goal_name,
                goal_amount,
                goal_deadline,
                goal_notes,
                goal_status,
            )
        if choice == "n":
            return (
                "cancel",
                goal_name,
                goal_amount,
                goal_deadline,
                goal_notes,
                goal_status,
            )
        if choice == "1":
            goal_name = get_goal_name()
        elif choice == "2":
            goal_amount = get_goal_amount()
        elif choice == "3":
            goal_deadline = get_goal_date()
        elif choice == "4":
            goal_notes = get_note()
        elif choice == "5":
            goal_status = get_status()
        else:
            print("Invalid option. Please try again.")


def get_goal_date():
    """Get and validate goal date input from user."""
    while True:
        date_str = input(
            "Please input a deadline for this goal. Enter a date in "
            "format YYYY-MM-DD: "
        )
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return date_str
        except ValueError:
            print("Invalid date. Please try again (format: YYYY-MM-DD).")


def get_goal_name():
    while True:
        name = input("Please enter a name for your goal: ")
        if not name.strip():
            print("Goal name cannot be empty. Please try again.")
            continue
        return name


def get_goal_amount():
    """Get and validate amount input from user."""
    while True:
        try:
            amount = float(input("Please type the goal amount here: "))
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a valid number.")


def get_status():
    """Get goal status from user (defaults to On Track)."""
    status_options = {
        "1": "On Track",
        "2": "Not Started",
        "3": "Behind Schedule",
        "4": "Completed",
    }

    while True:
        print("\nGoal Status:")
        print("1. On Track (default)")
        print("2. Not Started")
        print("3. Behind Schedule")
        print("4. Completed")
        choice = input(
            "Select status (1-4) or press Enter for default: "
        ).strip()

        if choice == "":
            return "On Track"

        status = status_options.get(choice)
        if status:
            return status
        else:
            print(
                "Invalid choice. Please select 1-4 or press Enter for default."
            )


def collect_goal_fields():
    goal_name = get_goal_name()
    goal_amount = get_goal_amount()
    goal_deadline = get_goal_date()
    goal_notes = get_note()
    goal_status = get_status()
    return goal_name, goal_amount, goal_deadline, goal_notes, goal_status


def set_financial_goals():
    goal_name, goal_amount, goal_deadline, goal_notes, goal_status = (
        collect_goal_fields()
    )
    # IMPORTANT: We intentionally reuse the same variable names here.
    # confirm_or_edit_goals() returns potentially EDITED values if user
    # chose to modify. By reassigning to the same variables, we ensure
    # the final (edited) values are what gets saved to the database, not
    # the original collected values.
    action, goal_name, goal_amount, goal_deadline, goal_notes, goal_status = (
        confirm_or_edit_goals(
            goal_name, goal_amount, goal_deadline, goal_notes, goal_status
        )
    )

    if action == "confirm":
        insert_goal(
            goal_name,
            goal_amount,
            goal_deadline,
            goal_notes,
            goal_status,
        )
    else:
        print("Goal creation cancelled. Returning to main menu.")


def progress_towards_goals():
    while True:
        all_goals = fetch_goals()
        goal_id = pick_goals(all_goals)
        if not goal_id:
            return
        else:
            update_progress(goal_id)
        if not ask_continue_updating():
            break
