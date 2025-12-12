# from datetime import date
# from decimal import Decimal

# pylint: disable=no-member

from django.core.management.base import BaseCommand

from et_transactions.models import Budget, Category, Expense, Goal, Income
from et_transactions.data.categories import (
    DEFAULT_EXPENSE_CATEGORIES,
    DEFAULT_INCOME_CATEGORIES,
)


class Command(BaseCommand):
    """Load demo data for development/testing."""

    help = "Populate the database with sample categories, expenses, income, "
    "budgets, and goals."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Seeding demo data..."))

        Expense.objects.all().delete()
        Income.objects.all().delete()
        Budget.objects.all().delete()
        Goal.objects.all().delete()

        categories = []

    for name in DEFAULT_EXPENSE_CATEGORIES:
        Category.objects.get_or_create(
            name=name, defaults={"category_type": Category.CategoryType.EXPENSE}
        )

    for name in DEFAULT_INCOME_CATEGORIES:
        Category.objects.get_or_create(
            name=name, defaults={"category_type": Category.CategoryType.INCOME}
        )

        category_lookup = {
            category.name: category for category in Category.objects.all()
        }
