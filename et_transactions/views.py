from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView

from .forms import (
    CreateExpenseForm,
    CreateIncomeForm,
    CreateBudgetForm,
    CreateGoalForm,
)
from .models import Budget, Category, Expense, Goal, Income


class IndexView(ListView):
    """Display the latest expense activity on the home page."""

    template_name = "et_transactions/index.html"
    model = Expense


class CategoryTypeListView(TemplateView):
    """Display available category types before drilling into
    categories."""

    template_name = "et_transactions/category_type_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["action_links"] = [
            {"label": "Add Expense", "url": reverse("create-expense")},
            {"label": "Add Income", "url": reverse("create-income")},
            {"label": "Add Budget", "url": reverse("create-budget")},
            {"label": "Add Goal", "url": reverse("create-goal")},
        ]
        return context


class CategoryListView(ListView):
    """List all transaction categories."""

    template_name = "et_transactions/category_list.html"
    model = Category
    ordering = ["name"]
    context_object_name = "categories"

    def get_queryset(self):
        queryset = super().get_queryset()
        selected_type = self.request.GET.get("type")
        if selected_type:
            queryset = queryset.filter(category_type=selected_type)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        selected_type = self.request.GET.get("type")
        context["selected_type"] = selected_type
        if selected_type:
            type_map = dict(Category.CategoryType.choices)
            context["selected_type_label"] = type_map.get(
                selected_type, selected_type.title()
            )
        return context


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
    ordering = ["-date"]
    context_object_name = "incomes"


class IncomeDetailView(DetailView):
    """Display a single transaction income."""

    template_name = "et_transactions/income-detail.html"
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
    ordering = ["start_date"]
    context_object_name = "budgets"


class BudgetDetailView(DetailView):
    """Display a single transaction budget."""

    template_name = "et_transactions/budget-detail.html"
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
    ordering = ["deadline"]
    context_object_name = "goals"


class CreateExpenseView(CreateView):
    """View for creating a new expense."""

    template_name = "et_transactions/create-expense.html"
    form_class = CreateExpenseForm
    success_url = reverse_lazy("expenses")


class CreateIncomeView(CreateView):
    """View for creating a new income."""

    template_name = "et_transactions/create-income.html"
    form_class = CreateIncomeForm
    success_url = reverse_lazy("income")


class CreateBudgetView(CreateView):
    """View for creating a new budget."""

    template_name = "et_transactions/create-budget.html"
    form_class = CreateBudgetForm
    success_url = reverse_lazy("budgets")


class CreateGoalView(CreateView):
    """View for creating a new goal."""

    template_name = "et_transactions/create-goal.html"
    form_class = CreateGoalForm
    success_url = reverse_lazy("goals")
