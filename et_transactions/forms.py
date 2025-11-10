"""Forms for the et_transactions app."""

from django import forms
from .models import Expense, Income


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
