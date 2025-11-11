from django.urls import path
from .views import (
    BudgetDetailView,
    BudgetListView,
    CategoryDetailView,
    CategoryListView,
    CategoryTypeListView,
    CreateExpenseView,
    CreateIncomeView,
    ExpenseDetailView,
    ExpenseListView,
    GoalListView,
    IncomeDetailView,
    IncomeListView,
    IndexView,
    CreateBudgetView,
    CreateGoalView,
)


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
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
]
