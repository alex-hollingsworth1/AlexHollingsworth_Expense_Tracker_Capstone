"""Views for the et_transactions app."""

from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.contrib import messages

from .forms import (
    CreateExpenseForm,
    CreateIncomeForm,
    CreateBudgetForm,
    CreateGoalForm,
)
from .models import Budget, Category, Expense, Goal, Income

# ----------------------Index View----------------------


class IndexView(ListView):
    """Display the latest expense activity on the home page."""

    template_name = "et_transactions/index.html"
    model = Expense


# ----------------------Category Views----------------------


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


# ----------------------Expense Views----------------------


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


class CreateExpenseView(CreateView):
    """View for creating a new expense."""

    template_name = "et_transactions/create-expense.html"
    form_class = CreateExpenseForm
    success_url = reverse_lazy("expenses")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Expense created successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Unable to create expense. Please fix the errors below.")
        return super().form_invalid(form)

class ExpenseUpdateView(UpdateView):
    """View for updating an existing expense."""

    model = Expense
    form_class = CreateExpenseForm
    template_name = "et_transactions/update-expense.html"
    success_url = reverse_lazy("expenses")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Expense updated successfully.")
        return response


class ExpenseDeleteView(DeleteView):
    """View for deleting an existing expense."""

    model = Expense
    template_name = "et_transactions/confirm-delete-expense.html"
    success_url = reverse_lazy("expenses")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Expense deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ----------------------Income Views----------------------


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


class CreateIncomeView(CreateView):
    """View for creating a new income."""

    template_name = "et_transactions/create-income.html"
    form_class = CreateIncomeForm
    success_url = reverse_lazy("income")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Income recorded successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Unable to record income. Please fix the errors below.")
        return super().form_invalid(form)

class IncomeUpdateView(UpdateView):
    """View for updating an existing income."""

    model = Income
    form_class = CreateIncomeForm
    template_name = "et_transactions/update-income.html"
    success_url = reverse_lazy("income")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Income updated successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Unable to update income. Please fix the errors below.")
        return super().form_invalid(form)


class IncomeDeleteView(DeleteView):
    """View for deleting an existing income."""

    model = Income
    template_name = "et_transactions/confirm-delete-income.html"
    success_url = reverse_lazy("income")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Income deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ----------------------Budget Views----------------------


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


class CreateBudgetView(CreateView):
    """View for creating a new budget."""

    template_name = "et_transactions/create-budget.html"
    form_class = CreateBudgetForm
    success_url = reverse_lazy("budgets")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Budget created successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Unable to create budget. Please fix the errors below.")
        return super().form_invalid(form)


class BudgetUpdateView(UpdateView):
    """View for updating an existing budget."""

    model = Budget
    form_class = CreateBudgetForm
    template_name = "et_transactions/update-budget.html"
    success_url = reverse_lazy("budgets")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Budget updated successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Unable to update budget. Please fix the errors below.")
        return super().form_invalid(form)


class BudgetDeleteView(DeleteView):
    """View for deleting an existing budget."""

    model = Budget
    template_name = "et_transactions/confirm-delete-budget.html"
    success_url = reverse_lazy("budgets")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Budget deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ----------------------Goal Views----------------------


class GoalListView(ListView):
    """List financial goals and their status."""

    template_name = "et_transactions/goal_list.html"
    model = Goal
    ordering = ["deadline"]
    context_object_name = "goals"


class GoalDetailView(DetailView):
    """Display a single financial goal."""

    template_name = "et_transactions/goal-detail.html"
    model = Goal
    context_object_name = "goal"


class CreateGoalView(CreateView):
    """View for creating a new goal."""

    template_name = "et_transactions/create-goal.html"
    form_class = CreateGoalForm
    success_url = reverse_lazy("goals")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Goal created successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Unable to create goal. Please fix the errors below.")
        return super().form_invalid(form)


class GoalUpdateView(UpdateView):
    """View for updating an existing goal."""

    model = Goal
    form_class = CreateGoalForm
    template_name = "et_transactions/update-goal.html"
    success_url = reverse_lazy("goals")

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Goal updated successfully.")
        return response

    def form_invalid(self, form):
        messages.error(self.request, "Unable to update goal. Please fix the errors below.")
        return super().form_invalid(form)


class GoalDeleteView(DeleteView):
    """View for deleting an existing goal."""

    model = Goal
    template_name = "et_transactions/confirm-delete-goal.html"
    success_url = reverse_lazy("goals")

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Goal deleted successfully.")
        return super().delete(request, *args, **kwargs)
