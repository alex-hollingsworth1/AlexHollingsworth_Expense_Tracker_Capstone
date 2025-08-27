"""This is a program to track expenses. Functionality includes the
ability to add, delete, and view expenses, as well as adding and viewing
income, setting and viewing a budget, setting financial goals and
viewing progress towards them.
"""

from transactions import (
    add_expense,
    view_expenses,
    view_expenses_by_category,
    add_income,
    view_income,
    view_income_by_category,
)
from budgets import set_budget, view_budget
from goals import set_financial_goals, progress_towards_goals


def view_menu(user_menu):
    """Display the menu of options to the user."""
    for key, value in user_menu.items():
        print(f"{key}. {value}")


def quit_and_exit():
    print("quit_and_exit() function worked")


menu_dict = {
    1: "Add expense",
    2: "View expenses",
    3: "View expenses by category",
    4: "Add income",
    5: "View income",
    6: "View income by category",
    7: "Set budget for a category",
    8: "View budget for a category",
    9: "Set financial goals",
    10: "View progress towards financial goals",
    11: "Quit",
}

menu_functions = {
    1: add_expense,
    2: view_expenses,
    3: view_expenses_by_category,
    4: add_income,
    5: view_income,
    6: view_income_by_category,
    7: set_budget,
    8: view_budget,
    9: set_financial_goals,
    10: progress_towards_goals,
    11: quit_and_exit,
}


def view_menu_again():
    main_menu = input(
        "Would you like to view the main menu again? y/n: "
    ).lower()
    while True:
        if main_menu == "y":
            return True
        elif main_menu == "n":
            return False
        else:
            print("Invalid option. Please try again.")
            main_menu = input(
                "Would you like to view the main menu again? y/n: "
            ).lower()


def main():
    """Main function to run the expense tracker program."""
    user_continue = True

    while user_continue:
        view_menu(menu_dict)
        try:
            user_select = int(
                input(
                    "Please select a number from the list to perform"
                    " the relevant function: "
                )
            )
            if user_select in menu_functions:
                if user_select == 11:  # Quit option
                    user_continue = False
                else:
                    menu_functions[user_select]()
                    user_continue = view_menu_again()
            else:
                print("Value not in the menu. Please try again.")
        except ValueError:
            print("Error. Please enter a valid number and try again.")


if __name__ == "__main__":
    main()
