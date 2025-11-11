"""Forms for the et_transactions app."""

from django import forms
from .models import Expense, Income, Budget, Goal


class CreateExpenseForm(forms.ModelForm):
    """Form for creating a new expense."""

    class Meta:
        """Meta class for CreateExpenseForm."""

        model = Expense
        fields = ["category", "amount", "date", "note"]
        labels = {"amount": "Amount", "date": "Date", "note": "Note"}
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.TextInput(attrs={"placeholder": "Optional note"}),
        }


class CreateIncomeForm(forms.ModelForm):
    """Form for creating a new income."""

    class Meta:
        """Meta class for CreateIncomeForm."""

        model = Income
        fields = ["category", "amount", "date", "note"]
        labels = {"amount": "Amount", "date": "Date", "note": "Note"}
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.TextInput(attrs={"placeholder": "Optional note"}),
        }


class CreateBudgetForm(forms.ModelForm):
    """Form for creating a new budget."""

    class Meta:
        """Meta class for CreateBudgetForm."""

        model = Budget
        fields = [
            "category",
            "start_date",
            "end_date",
            "amount",
            "note",
            "dates",
        ]
        labels = {
            "start_date": "Start date",
            "end_date": "End date",
            "amount": "Budget amount",
            "note": "Note",
            "dates": "Checkpoints",
            "remaining_amount": "Remaining amount",
            "percentage": "Progress (%)",
        }
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
            "note": forms.TextInput(attrs={"placeholder": "Optional note"}),
            "dates": forms.TextInput(
                attrs={
                    "placeholder": "Comma-separated checkpoints, e.g. 2024-12-01,2024-12-31"
                }
            ),
        }


class CreateGoalForm(forms.ModelForm):
    """Form for creating a new goal."""

    class Meta:
        """Meta class for CreateGoalForm."""

        model = Goal
        fields = ["name", "target", "deadline", "note", "status"]
        labels = {
            "name": "Goal name",
            "target": "Target amount",
            "deadline": "Deadline",
            "note": "Note",
            "status": "Status",
        }
        widgets = {
            "deadline": forms.DateInput(attrs={"type": "date"}),
            "note": forms.TextInput(attrs={"placeholder": "Optional note"}),
        }
