"""
Utility functions and helper methods.
"""

from datetime import datetime


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
            user_input = input(
                f"Please type the amount for the {transaction_type} "
                "payment here (in dollars): "
            )
            # Clean the input first (remove $, commas, spaces)
            cleaned_input = (
                user_input.replace("$", "").replace(",", "").strip()
            )
            amount = float(cleaned_input)
            if amount <= 0:
                print("Amount must be greater than 0.")
                continue
            return amount
        except ValueError:
            print("Invalid amount. Please enter a valid number.")


def get_note():
    """Get optional note from user."""
    while True:
        user_optional_note = input(
            "Would you like to write an optional note? y/n: "
        ).lower()
        if user_optional_note == "y":
            while True:
                user_note = input("Please write your optional note: ")
                if len(user_note) > 30:
                    print("Notes must be 30 characters max.")
                else:
                    return user_note
        elif user_optional_note == "n":
            return ""
        else:
            print("Invalid option. Please enter 'y' or 'n'.")
