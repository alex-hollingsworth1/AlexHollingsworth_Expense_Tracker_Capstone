"""Views for the et_transactions app."""

# pylint: disable=no-member

# from django.contrib import messages
from django.db.models import Sum

# from django.urls import reverse, reverse_lazy
# from django.views.generic import ListView, TemplateView
# from django.views.generic.detail import DetailView
# from django.views.generic.edit import CreateView, DeleteView, UpdateView
from rest_framework import viewsets
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import (
    ExpenseSerializer,
    CategorySerializer,
    IncomeSerializer,
    BudgetSerializer,
    GoalSerializer,
)

# from .forms import (
#     CreateExpenseForm,
#     CreateIncomeForm,
#     CreateBudgetForm,
#     CreateGoalForm,
# )
from .models import Budget, Category, Expense, Goal, Income


# ----------------------API Views (DRF)----------------------


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows expenses to be viewed or edited.
    """

    queryset = Expense.objects.all().order_by("-date")
    serializer_class = ExpenseSerializer


class IncomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows income to be viewed or edited.
    """

    queryset = Income.objects.all().order_by("-date")
    serializer_class = IncomeSerializer


class BudgetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows budgets to be viewed or edited.
    """

    queryset = Budget.objects.all().order_by("-start_date")
    serializer_class = BudgetSerializer


class GoalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows goals to be viewed or edited.
    """

    queryset = Goal.objects.all().order_by("deadline")
    serializer_class = GoalSerializer


class DashboardAPIView(APIView):
    """
    API endpoint that returns dashboard summary data.
    Combines expenses, income, budgets, and goals with totals.
    """

    permission_classes = [AllowAny]

    def get(self, request):

        # Query-set for recent expenses, income, budgets, and goals
        recent_expenses = Expense.objects.order_by("-date")[:3]
        recent_income = Income.objects.order_by("-date")[:3]
        recent_budgets = Budget.objects.order_by("-start_date")[:3]
        recent_goals = Goal.objects.order_by("deadline")[:3]
        income_total = (
            Income.objects.aggregate(total=Sum("amount"))["total"] or 0
        )
        expense_total = (
            Expense.objects.aggregate(total=Sum("amount"))["total"] or 0
        )
        net_total = income_total - expense_total
        number_of_budgets = Budget.objects.count()
        number_of_goals = Goal.objects.count()

        # Serialize the data
        recent_expenses_serializer = ExpenseSerializer(
            recent_expenses, many=True
        )
        recent_income_serializer = IncomeSerializer(recent_income, many=True)
        recent_budgets_serializer = BudgetSerializer(recent_budgets, many=True)
        recent_goals_serializer = GoalSerializer(recent_goals, many=True)

        # Numbers don't need serialization - use them directly
        data = {
            "recent_expenses": recent_expenses_serializer.data,
            "recent_income": recent_income_serializer.data,
            "recent_budgets": recent_budgets_serializer.data,
            "recent_goals": recent_goals_serializer.data,
            "income_total": income_total,
            "expense_total": expense_total,
            "net_total": net_total,
            "number_of_budgets": number_of_budgets,
            "number_of_goals": number_of_goals,
        }

        return Response(data)
