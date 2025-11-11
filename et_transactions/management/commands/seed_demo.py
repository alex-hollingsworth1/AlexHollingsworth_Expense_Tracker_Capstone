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
            category.name: category for category in Category.objects.all()
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

        income_entries = [
            Income(
                category=category_lookup["Salary"],
                amount=Decimal("3500.00"),
                date=date(2024, 12, 1),
                note="Monthly salary",
            ),
            Income(
                category=category_lookup["Freelance"],
                amount=Decimal("500.00"),
                date=date(2024, 12, 15),
                note="Website project",
            ),
        ]
        Income.objects.bulk_create(income_entries)

        budgets = [
            Budget(
                category=category_lookup["Groceries"],
                amount=Decimal("400.00"),
                start_date=date(2024, 12, 1),
                end_date=date(2024, 12, 31),
                dates="2024-12-01,2024-12-31",
                remaining_amount=Decimal("250.00"),
                percentage=Decimal("62.50"),
                note="Monthly grocery budget",
            ),
        ]
        Budget.objects.bulk_create(budgets)

        goals = [
            Goal(
                name="Emergency Fund",
                target=Decimal("5000.00"),
                deadline=date(2025, 6, 1),
                status="On Track",
                note="6 months expenses",
            ),
        ]
        Goal.objects.bulk_create(goals)
