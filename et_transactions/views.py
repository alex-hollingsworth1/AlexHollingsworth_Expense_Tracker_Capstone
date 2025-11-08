from django.views.generic import ListView

from .models import Budget, Category, Expense, Goal, Income


class IndexView(ListView):
    """Display the latest expense activity on the home page."""

    template_name = "et_transactions/index.html"
    model = Expense


class CategoryListView(ListView):
    """List all transaction categories."""

    template_name = "et_transactions/category_list.html"
    model = Category


class ExpenseListView(ListView):
    """List recorded expenses."""

    template_name = "et_transactions/expense_list.html"
    model = Expense


class IncomeListView(ListView):
    """List recorded income entries."""

    template_name = "et_transactions/income_list.html"
    model = Income


class BudgetListView(ListView):
    """List budgets for each category."""

    template_name = "et_transactions/budget_list.html"
    model = Budget


class GoalListView(ListView):
    """List financial goals and their status."""

    template_name = "et_transactions/goal_list.html"
    model = Goal

