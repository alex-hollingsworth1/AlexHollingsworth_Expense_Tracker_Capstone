"""Serializers for the et_transactions app."""

# pylint: disable=no-member

from rest_framework import serializers
from .models import Expense, Category, Income, Budget, Goal, Project, Client


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
        read_only_fields = ["user"]


class ProjectSerializer(serializers.ModelSerializer):
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.none(),  # Placeholder - will be set in __init__
        source="client", 
        write_only=True,
        required=False,
        allow_null=True
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['client_id'].queryset = Client.objects.filter(user=request.user)

    class Meta:
        model = Project
        fields = "__all__"
        read_only_fields = ["user"]


class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.none(),  # Placeholder - will be set in __init__
        source="project", write_only=True, required=False, allow_null=True
    )
    
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.none(),  # Placeholder - will be set in __init__
        source="client", write_only=True, required=False, allow_null=True
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['project_id'].queryset = Project.objects.filter(user=request.user)
            self.fields['client_id'].queryset = Client.objects.filter(user=request.user)

    class Meta:
        model = Expense
        fields = "__all__"
        read_only_fields = ["user"]


class IncomeSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    project = ProjectSerializer(read_only=True)
    project_id = serializers.PrimaryKeyRelatedField(
        queryset=Project.objects.none(),  # Placeholder - will be set in __init__
        source="project", write_only=True, required=False, allow_null=True
    )
    
    client = ClientSerializer(read_only=True)
    client_id = serializers.PrimaryKeyRelatedField(
        queryset=Client.objects.none(),  # Placeholder - will be set in __init__
        source="client", write_only=True, required=False, allow_null=True
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            self.fields['project_id'].queryset = Project.objects.filter(user=request.user)
            self.fields['client_id'].queryset = Client.objects.filter(user=request.user)

    class Meta:
        model = Income
        fields = "__all__"
        read_only_fields = ["user"]


class BudgetSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source="category", write_only=True
    )
    amount = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

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
        model = Budget
        fields = "__all__"
        read_only_fields = ["user"]


class GoalSerializer(serializers.ModelSerializer):
    target = serializers.DecimalField(max_digits=10, decimal_places=2, min_value=0)

    class Meta:
        model = Goal
        fields = "__all__"
        read_only_fields = ["user"]
