from django.urls import path
from .views import (
    BudgetListView,
    CategoryListView,
    ExpenseListView,
    GoalListView,
    IncomeListView,
    IndexView,
)


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("categories/", CategoryListView.as_view(), name="categories"),
    path("expenses/", ExpenseListView.as_view(), name="expenses"),
    path("income/", IncomeListView.as_view(), name="income"),
    path("budgets/", BudgetListView.as_view(), name="budgets"),
    path("goals/", GoalListView.as_view(), name="goals"),
]
