"""Test cases for the et_transactions models."""

from decimal import Decimal
from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Expense, Income, Budget, Goal

# pylint: disable=no-member


class CategoryModelTest(TestCase):
    """Test cases for the Category model.

    Note: Category doesn't have a user field, so no user setup needed.
    """

    def test_create_category_expense(self):
        """
        Test that we can create an expense category.

        This is a simple test that:
        1. Creates a category
        2. Checks it was saved to the database
        3. Verifies its properties are correct
        """

        category = Category.objects.create(
            name="Groceries", category_type=Category.CategoryType.EXPENSE
        )

        saved_category = Category.objects.get(id=category.id)

        # Assert: Check that it has the correct values
        self.assertEqual(saved_category.name, "Groceries")
        self.assertEqual(
            saved_category.category_type, Category.CategoryType.EXPENSE
        )
        self.assertEqual(
            str(saved_category), "Groceries"
        )  # Test __str__ method

    def test_create_category_income(self):
        """
        Test that we can create an income category.
        """

        category = Category.objects.create(
            name="Freelance", category_type=Category.CategoryType.INCOME
        )

        saved_category = Category.objects.get(id=category.id)

        # Assert: Check that it has the correct values
        self.assertEqual(saved_category.name, "Freelance")
        self.assertEqual(
            saved_category.category_type, Category.CategoryType.INCOME
        )
        self.assertEqual(str(saved_category), "Freelance")


class ExpenseModelTest(TestCase):
    """Test cases for the Expense model.

    Note: Expense requires a User and Category (ForeignKey relationships).
    We use setUp() to create these once for all tests.
    """

    def setUp(self):
        """Set up test data that all Expense tests can use."""
        # Create a user (required for Expense)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Create a category (required for Expense)
        self.category = Category.objects.create(
            name="Groceries",
            category_type=Category.CategoryType.EXPENSE
        )

    def test_create_expense(self):
        """Test that we can create an expense with user and category."""
        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('50.00'),
            date=date(2024, 1, 15),
            note='Test grocery expense'
        )

        saved_expense = Expense.objects.get(id=expense.id)

        # Assert: Check all the values
        self.assertEqual(saved_expense.user, self.user)
        self.assertEqual(saved_expense.category, self.category)
        self.assertEqual(saved_expense.amount, Decimal('50.00'))
        self.assertEqual(saved_expense.date, date(2024, 1, 15))
        self.assertEqual(saved_expense.note, 'Test grocery expense')
        self.assertEqual(
            str(saved_expense),
            f"{date(2024, 1, 15)} - Groceries - $50.00"
        )

    def test_create_expense_without_note(self):
        """Test creating an expense without a note (optional field)."""
        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('25.00'),
            date=date(2024, 1, 20)
            # note is optional, so we don't include it
        )

        saved_expense = Expense.objects.get(id=expense.id)
        self.assertIsNone(saved_expense.note)


class IncomeModelTest(TestCase):
    """Test cases for the Income model.

    Note: Income requires a User and Category (ForeignKey relationships).
    We use setUp() to create these once for all tests.
    """

    def setUp(self):
        """Set up test data that all Income tests can use."""
        # Create a user (required for Income)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Create a category (required for Income)
        self.category = Category.objects.create(
            name="Salary",
            category_type=Category.CategoryType.INCOME
        )

    def test_create_income(self):
        """Test that we can create an income with user and category."""
        income = Income.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal('2000.00'),
            date=date(2024, 1, 1),
            note='Monthly salary'
        )

        saved_income = Income.objects.get(id=income.id)

        # Assert: Check all the values
        self.assertEqual(saved_income.user, self.user)
        self.assertEqual(saved_income.category, self.category)
        self.assertEqual(saved_income.amount, Decimal('2000.00'))
        self.assertEqual(saved_income.date, date(2024, 1, 1))
        self.assertEqual(saved_income.note, 'Monthly salary')
        self.assertEqual(
            str(saved_income),
            f"{date(2024, 1, 1)} - Salary - $2000.00"
        )


class BudgetModelTest(TestCase):
    """Test cases for the Budget model.

    Note: Budget requires a User and Category (ForeignKey relationships).
    We use setUp() to create these once for all tests.
    """

    def setUp(self):
        """Set up test data that all Budget tests can use."""
        # Create a user (required for Budget)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        # Create a category (required for Budget)
        self.category = Category.objects.create(
            name="Groceries",
            category_type=Category.CategoryType.EXPENSE
        )

    def test_create_budget(self):
        """Test that we can create a budget with user and category."""
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            amount=Decimal('500.00'),
            note='Monthly grocery budget'
        )

        saved_budget = Budget.objects.get(id=budget.id)

        # Assert: Check all the values
        self.assertEqual(saved_budget.user, self.user)
        self.assertEqual(saved_budget.category, self.category)
        self.assertEqual(saved_budget.start_date, date(2024, 1, 1))
        self.assertEqual(saved_budget.end_date, date(2024, 1, 31))
        self.assertEqual(saved_budget.amount, Decimal('500.00'))
        self.assertEqual(saved_budget.note, 'Monthly grocery budget')
        # Check that remaining_amount and percentage were calculated
        self.assertIsNotNone(saved_budget.remaining_amount)
        self.assertIsNotNone(saved_budget.percentage)


class GoalModelTest(TestCase):
    """Test cases for the Goal model.

    Note: Goal requires a User (ForeignKey relationship).
    We use setUp() to create this once for all tests.
    """

    def setUp(self):
        """Set up test data that all Goal tests can use."""
        # Create a user (required for Goal)
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )

    def test_create_goal(self):
        """Test that we can create a goal with user."""
        goal = Goal.objects.create(
            user=self.user,
            name="Save for Vacation",
            target=Decimal('5000.00'),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note='Saving for summer vacation'
        )

        saved_goal = Goal.objects.get(id=goal.id)

        # Assert: Check all the values
        self.assertEqual(saved_goal.user, self.user)
        self.assertEqual(saved_goal.name, "Save for Vacation")
        self.assertEqual(saved_goal.target, Decimal('5000.00'))
        self.assertEqual(saved_goal.deadline, date(2024, 12, 31))
        self.assertEqual(saved_goal.status, "In Progress")
        self.assertEqual(saved_goal.note, 'Saving for summer vacation')
        self.assertEqual(
            str(saved_goal),
            "Save for Vacation - $5000.00 (In Progress)"
        )
