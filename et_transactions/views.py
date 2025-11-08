from django.views.generic import ListView
from django.views.generic.detail import DetailView

from .models import Budget, Category, Expense, Goal, Income


class IndexView(ListView):
    """Display the latest expense activity on the home page."""

    template_name = "et_transactions/index.html"
    model = Expense


class CategoryListView(ListView):
    """List all transaction categories."""

    template_name = "et_transactions/category_list.html"
    model = Category
    ordering = ["name"]
    context_object_name = "categories"


class CategoryDetailView(DetailView):
    """Display a single transaction category with all associated
    expenses."""

    template_name = "et_transactions/category_detail.html"
    model = Category
    context_object_name = "category"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["expenses"] = self.object.expenses.order_by("-date")
        return context


class ExpenseListView(ListView):
    """List recorded expenses."""

    template_name = "et_transactions/expense_list.html"
    model = Expense
    ordering = ["-date"]
    context_object_name = "expenses"


class ExpenseDetailView(DetailView):
    """Display a single transaction expense."""

    template_name = "et_transactions/expense_detail.html"
    model = Expense
    context_object_name = "expense"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.object.category
        return context


class IncomeListView(ListView):
    """List recorded income entries."""

    template_name = "et_transactions/income_list.html"
    model = Income


class IncomeDetailView(DetailView):
    """Display a single transaction income."""

    template_name = "et_transactions/income_detail.html"
    model = Income
    context_object_name = "income"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.object.category
        return context


class BudgetListView(ListView):
    """List budgets for each category."""

    template_name = "et_transactions/budget_list.html"
    model = Budget


class BudgetDetailView(DetailView):
    """Display a single transaction budget."""

    template_name = "et_transactions/budget_detail.html"
    model = Budget
    context_object_name = "budget"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["category"] = self.object.category
        return context


class GoalListView(ListView):
    """List financial goals and their status."""

    template_name = "et_transactions/goal_list.html"
    model = Goal
