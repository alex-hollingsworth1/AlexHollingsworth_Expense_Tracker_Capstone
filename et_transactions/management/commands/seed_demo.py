from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand

from et_transactions.models import Budget, Category, Expense, Goal, Income


class Command(BaseCommand):
    """Load demo data for development/testing."""

    help = "Populate the database with sample categories, expenses, income, budgets, and goals."

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Seeding demo data..."))

        Category.objects.all().delete()
        Expense.objects.all().delete()
        Income.objects.all().delete()
        Budget.objects.all().delete()
        Goal.objects.all().delete()

        categories = [
            Category(
                name="Groceries",
                category_type=Category.CategoryType.EXPENSE,
            ),
            Category(
                name="Entertainment",
                category_type=Category.CategoryType.EXPENSE,
            ),
            Category(
                name="Gas",
                category_type=Category.CategoryType.EXPENSE,
            ),
            Category(
                name="Dining Out",
                category_type=Category.CategoryType.EXPENSE,
            ),
            Category(
                name="Shopping",
                category_type=Category.CategoryType.EXPENSE,
            ),
            Category(
                name="Bills",
                category_type=Category.CategoryType.EXPENSE,
            ),
            Category(
                name="Salary",
                category_type=Category.CategoryType.INCOME,
            ),
            Category(
                name="Freelance",
                category_type=Category.CategoryType.INCOME,
            ),
        ]
        Category.objects.bulk_create(categories)

        category_lookup = {
            category.name: category
            for category in Category.objects.all()
        }

        expenses = [
            Expense(
                category=category_lookup["Groceries"],
                amount=Decimal("125.50"),
                date=date(2024, 12, 1),
                note="Weekly shopping",
            ),
            Expense(
                category=category_lookup["Gas"],
                amount=Decimal("45.00"),
                date=date(2024, 12, 3),
                note="Tank fill",
            ),
            Expense(
                category=category_lookup["Dining Out"],
                amount=Decimal("35.75"),
                date=date(2024, 12, 5),
                note="Lunch with team",
            ),
            Expense(
                category=category_lookup["Entertainment"],
                amount=Decimal("15.99"),
                date=date(2024, 12, 7),
                note="Movie ticket",
            ),
            Expense(
                category=category_lookup["Groceries"],
                amount=Decimal("89.25"),
                date=date(2024, 12, 10),
                note="Groceries top-up",
            ),
            Expense(
                category=category_lookup["Bills"],
                amount=Decimal("120.00"),
                date=date(2024, 12, 15),
                note="Internet bill",
            ),
            Expense(
                category=category_lookup["Shopping"],
                amount=Decimal("67.89"),
                date=date(2024, 12, 18),
                note="Clothes",
            ),
            Expense(
                category=category_lookup["Gas"],
                amount=Decimal("48.50"),
                date=date(2024, 12, 20),
                note="Fuel",
            ),
        ]
        Expense.objects.bulk_create(expenses)

