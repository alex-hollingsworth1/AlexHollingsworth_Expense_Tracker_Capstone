"""
Financial goal setting and tracking functionality.
"""

from datetime import datetime
from utils import get_note
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
        (goal_id,),
    )
    goal_details = cursor.fetchone()

    # Print out goal with the ID requested by the user
    print("\nHere are the details from your goals with this specific ID:\n")
    show_goals([goal_details])
    try:
        saved_amount = float(
            input(
                "\nHow much have you saved so far for this goal (in dollars)? "
            )
        )
        if saved_amount < 0:
            print("Amount cannot be negative. Setting to 0.")
            saved_amount = 0
    except ValueError:
        print("Invalid amount. Setting to 0.")
        saved_amount = 0
    remaining_amount = goal_details[2] - saved_amount
    deadline = datetime.strptime(
        goal_details[3], "%Y-%m-%d"
    )  # Convert string to datetime
    today = datetime.now()
    days_remaining = (
        deadline - today
    ).days  # This gives you the number of days

    # After getting saved_amount, calculate display status
    if saved_amount == 0:
        display_status = "Not Started"
    elif saved_amount >= goal_details[2]:  # goal_details[2] is target
        display_status = "Completed"
    elif days_remaining < 0:
        display_status = "Behind Schedule"
    else:
        display_status = "On Track"

    while True:
        show_remaining_amount = input(
            "Would you like a new table showing the remaining amount and how "
            " many days are remaining? (y/n): "
        ).lower()
        if show_remaining_amount == "y":
            print("\nUpdated Goal Progress:\n")
            print(
                f"{'Goal':<40} {'Target':<11} {'Saved':<11} {'Remaining':<11} "
                f"{'Status':<15}"
            )
            print("-" * 120)
            print(
                f"{goal_details[1]:<40} ${goal_details[2]:<10.2f} "
                f"${saved_amount:<10.2f} ${remaining_amount:<10.2f} "
                f"{display_status:<15}"
            )
            print("\nDays until deadline: ", end="")
            if days_remaining < 0:
                print(
                    f"\nDays remaining: OVERDUE by {abs(days_remaining)} days."
                )
            else:
                print(f"{days_remaining} days")
            if goal_details[2] > 0:
                print(f"Progress: {(saved_amount/goal_details[2]*100):.2f}%")
            else:
                print("Progress: N/A (no target set)")
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
    print(
        f"{'ID':<3} {'Goal':<30} {'Target':<11} {'Deadline':<12} "
        f"{'Notes':<30} {'Status':<12}"
    )
    print("-" * 120)
    for id, name, target, deadline, notes, status in goal_list:
        print(
            f"{id:<3} {name:30} ${target:<10.2f} {deadline:<12} "
            f"{notes or 'No notes':<30} {status:<12}"
        )


def pick_goals(goal_list):
    """Display the list of goals to the user."""
    show_goals(goal_list)
    user_choice = input(
        "\nSelect goal ID to view or update progress or N to return: "
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
            f"{'Goal':<40} {'Target':<7} {'Deadline':<12} {'Notes':<30} "
            f"{'Status':<12}"
        )
        print("-" * 120)
        print(
            f"{goal_name:<40} ${goal_amount:<6.2f} {goal_deadline:<12} "
            f"{goal_notes or 'No notes':<30} {goal_status:<12}"
        )
        print("\nEdit options:")
        print("1. Goal name")
        print("2. Target amount")
        print("3. Deadline")
        print("4. Notes")
        print("5. Status")
        choice = input(
            "\nEnter Y to confirm, N to cancel, or 1-5 to edit: "
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
            amount = float(
                input("Please type the goal amount here (in dollars): ")
            )
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
                "Invalid choice. Please select 1-4 or press Enter for "
                "default. "
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
    # confirm_or_edit_goals() returns potentially edited values if user
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
        print("Goal creation cancelled.")


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
