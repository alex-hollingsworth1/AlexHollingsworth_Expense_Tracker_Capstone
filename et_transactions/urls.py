"""URLs for the et_transactions app."""

from django.urls import path
from .views import (
    BudgetDeleteView,
    BudgetDetailView,
    BudgetListView,
    BudgetUpdateView,
    CategoryDetailView,
    CategoryListView,
    CategoryTypeListView,
    CreateBudgetView,
    CreateExpenseView,
    CreateGoalView,
    CreateIncomeView,
    DashboardView,
    ExpenseDeleteView,
    ExpenseDetailView,
    ExpenseListView,
    ExpenseUpdateView,
    GoalDeleteView,
    GoalDetailView,
    GoalListView,
    GoalUpdateView,
    IncomeDeleteView,
    IncomeDetailView,
    IncomeListView,
    IncomeUpdateView,
)


urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path(
        "categories/",
        CategoryTypeListView.as_view(),
        name="category-type-list",
    ),
    path("categories/list/", CategoryListView.as_view(), name="categories"),
    path("expenses/", ExpenseListView.as_view(), name="expenses"),
    path(
        "expenses/<int:pk>/",
        ExpenseDetailView.as_view(),
        name="expense-detail",
    ),
    path("income/", IncomeListView.as_view(), name="income"),
    path(
        "income/<int:pk>/",
        IncomeDetailView.as_view(),
        name="income-detail",
    ),
    path("budgets/", BudgetListView.as_view(), name="budgets"),
    path(
        "budgets/<int:pk>/",
        BudgetDetailView.as_view(),
        name="budget-detail",
    ),
    path("goals/", GoalListView.as_view(), name="goals"),
    path(
        "goals/<int:pk>/",
        GoalDetailView.as_view(),
        name="goal-detail",
    ),
    path(
        "categories/<int:pk>/",
        CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path(
        "expenses/create/", CreateExpenseView.as_view(), name="create-expense"
    ),
    path("income/create/", CreateIncomeView.as_view(), name="create-income"),
    path("budgets/create/", CreateBudgetView.as_view(), name="create-budget"),
    path("goals/create/", CreateGoalView.as_view(), name="create-goal"),
    path(
        "expenses/<int:pk>/edit/",
        ExpenseUpdateView.as_view(),
        name="expense-update",
    ),
    path(
        "expenses/<int:pk>/delete/",
        ExpenseDeleteView.as_view(),
        name="expense-delete",
    ),
    path(
        "income/<int:pk>/edit/",
        IncomeUpdateView.as_view(),
        name="income-update",
    ),
    path(
        "income/<int:pk>/delete/",
        IncomeDeleteView.as_view(),
        name="income-delete",
    ),
    path(
        "budgets/<int:pk>/edit/",
        BudgetUpdateView.as_view(),
        name="budget-update",
    ),
    path(
        "budgets/<int:pk>/delete/",
        BudgetDeleteView.as_view(),
        name="budget-delete",
    ),
    path(
        "goals/<int:pk>/edit/",
        GoalUpdateView.as_view(),
        name="goal-update",
    ),
    path(
        "goals/<int:pk>/delete/",
        GoalDeleteView.as_view(),
        name="goal-delete",
    ),
]
