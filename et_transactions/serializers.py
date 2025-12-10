"""Serializers for the et_transactions app."""

# pylint: disable=no-member

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
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=0
    )

    class Meta:
        """Meta class for the ExpenseSerializer."""

        model = Expense
        fields = "__all__"
        read_only_fields = ["user"]


class IncomeSerializer(serializers.ModelSerializer):
    """Serializer for the Income model."""

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=0
    )

    class Meta:
        """Meta class for the IncomeSerializer."""

        model = Income
        fields = "__all__"
        read_only_fields = ["user"]


class BudgetSerializer(serializers.ModelSerializer):
    """Serializer for the Budget model."""

    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=0
    )

    # pylint: disable=arguments-renamed
    def validate(self, data):
        """Validate that end_date is after start_date."""

        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date and end_date:
            if end_date <= start_date:
                raise serializers.ValidationError(
                    {"end_date": "End date must be after start date."}
                )

        return data

    class Meta:
        """Meta class for the BudgetSerializer."""

        model = Budget
        fields = "__all__"
        read_only_fields = ["user"]


class GoalSerializer(serializers.ModelSerializer):
    """Serializer for the Goal model."""

    target = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=0
    )

    class Meta:
        """Meta class for the GoalSerializer."""

        model = Goal
        fields = "__all__"
        read_only_fields = ["user"]
