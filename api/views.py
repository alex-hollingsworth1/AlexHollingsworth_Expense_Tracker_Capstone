"""Views for the api app."""

# pylint: disable=no-member

from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from api.data.categories import DEFAULT_EXPENSE_CATEGORIES, DEFAULT_INCOME_CATEGORIES
from .serializers import (
    ExpenseSerializer,
    CategorySerializer,
    IncomeSerializer,
    BudgetSerializer,
    GoalSerializer,
    ProjectSerializer,
    ClientSerializer
)
from .models import Budget, Category, Expense, Goal, Income, Project, Client


# ----------------------API Views (DRF)----------------------

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.filter(user=self.request.user).order_by("-date_created")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ClientSerializer

    def get_queryset(self):
        return Client.objects.filter(user=self.request.user).order_by("name")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows expenses to be viewed or edited.
    """

    queryset = Expense.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class IncomeViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows income to be viewed or edited.
    """

    queryset = Income.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = IncomeSerializer

    def get_queryset(self):
        return Income.objects.filter(user=self.request.user).order_by("-date")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BudgetViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows budgets to be viewed or edited.
    """

    queryset = Budget.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = BudgetSerializer

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user).order_by(
            "-start_date"
        )

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class GoalViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows goals to be viewed or edited.
    """

    queryset = Goal.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = GoalSerializer

    def get_queryset(self):
        return Goal.objects.filter(user=self.request.user).order_by("deadline")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    """API endpoint that allows categories to be viewed or edited."""

    queryset = Category.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer

    def get_queryset(self):
        queryset = Category.objects.all()
        category_type = self.request.query_params.get('type')
        
        if category_type:
            if category_type in ['EXPENSE', 'INCOME']:
                queryset = queryset.filter(category_type=category_type)
        
        return queryset


class DashboardAPIView(APIView):
    """
    API endpoint that returns dashboard summary data.
    Combines expenses, income, budgets, and goals with totals.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Get dashboard summary data."""

        user = request.user

        recent_expenses = Expense.objects.filter(user=user).order_by("-date")[
            :3
        ]
        recent_income = Income.objects.filter(user=user).order_by("-date")[:3]
        recent_budgets = Budget.objects.filter(user=user).order_by(
            "-start_date"
        )[:3]
        recent_goals = Goal.objects.filter(user=user).order_by("deadline")[:3]
        income_total = (
            Income.objects.filter(user=user).aggregate(total=Sum("amount"))[
                "total"
            ]
            or 0
        )
        expense_total = (
            Expense.objects.filter(user=user).aggregate(total=Sum("amount"))[
                "total"
            ]
            or 0
        )
        net_total = income_total - expense_total
        number_of_budgets = Budget.objects.filter(user=user).count()
        number_of_goals = Goal.objects.filter(user=user).count()

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
