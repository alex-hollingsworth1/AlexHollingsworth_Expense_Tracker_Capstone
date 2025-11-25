"""Serializers for the et_transactions app."""

from rest_framework import serializers
from .models import Expense, Category, Income, Budget, Goal


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""
    class Meta:
        """Meta class for the CategorySerializer."""
        model = Category
        fields = "__all__"


class ExpenseSerializer(serializers.ModelSerializer):
    """Serializer for the Expense model."""
    category = CategorySerializer(read_only=True)

    class Meta:
        """Meta class for the ExpenseSerializer."""
        model = Expense
        fields = "__all__"


class IncomeSerializer(serializers.ModelSerializer):
    """Serializer for the Income model."""
    category = CategorySerializer(read_only=True)

    class Meta:
        """Meta class for the IncomeSerializer."""
        model = Income
        fields = "__all__"


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for the Budget model."""
    category = CategorySerializer(read_only=True)

    class Meta:
        """Meta class for the BudgetSerializer."""
        model = Budget
        fields = "__all__"


class GoalSerializer(serializers.ModelSerializer):
    """Serializer for the Goal model."""
    category = CategorySerializer(read_only=True)

    class Meta:
        """Meta class for the GoalSerializer."""
        model = Goal
        fields = "__all__"
