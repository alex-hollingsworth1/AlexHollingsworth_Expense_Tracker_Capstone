"""Test cases for the et_transactions models."""

from decimal import Decimal
from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Category, Expense, Income, Budget, Goal

# pylint: disable=no-member
# pylint: disable=missing-function-docstring

# ----------------------Category Model Tests----------------------


class CategoryModelTest(TestCase):
    "Note: Category doesn't have a user field, so no user setup needed."

    def test_create_category_expense(self):
        category = Category.objects.create(
            name="Groceries", category_type=Category.CategoryType.EXPENSE
        )

        saved_category = Category.objects.get(id=category.id)

        self.assertEqual(saved_category.name, "Groceries")
        self.assertEqual(
            saved_category.category_type, Category.CategoryType.EXPENSE
        )
        self.assertEqual(str(saved_category), "Groceries")

    def test_create_category_income(self):

        category = Category.objects.create(
            name="Freelance", category_type=Category.CategoryType.INCOME
        )

        saved_category = Category.objects.get(id=category.id)

        self.assertEqual(saved_category.name, "Freelance")
        self.assertEqual(
            saved_category.category_type, Category.CategoryType.INCOME
        )
        self.assertEqual(str(saved_category), "Freelance")

    def test_read_category_expense(self):
        saved_category = Category.objects.create(name="Groceries")

        retrieved_category = Category.objects.get(id=saved_category.id)
        self.assertEqual(retrieved_category.name, "Groceries")

    # Update
    def test_update_category(self):
        """Test updating an existing category."""
        # Create a category first
        category = Category.objects.create(
            name="Groceries", category_type=Category.CategoryType.EXPENSE
        )

        # Update the category
        category.name = "Food & Dining"
        category.category_type = Category.CategoryType.INCOME
        category.save()

        # Retrieve and verify the updated category
        updated_category = Category.objects.get(id=category.id)
        self.assertEqual(updated_category.name, "Food & Dining")
        self.assertEqual(
            updated_category.category_type, Category.CategoryType.INCOME
        )

    # Delete
    def test_delete_category(self):
        """Test deleting an existing category."""
        # Create a category first
        category = Category.objects.create(
            name="Groceries", category_type=Category.CategoryType.EXPENSE
        )

        # Verify it exists
        self.assertIsNotNone(Category.objects.get(id=category.id))

        # Delete the category
        category.delete()

        # Verify it no longer exists
        with self.assertRaises(Category.DoesNotExist):
            Category.objects.get(id=category.id)


# ----------------------Expense Model Tests----------------------


class ExpenseModelTest(TestCase):
    """
    Note: Expense requires a User and Category (ForeignKey
    relationships).
    We use setUp() to create these once for all tests.
    """

    def setUp(self):
        """Set up test data that all Expense tests can use."""
        # Create a user (required for Expense)
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Create a category (required for Expense)
        self.category = Category.objects.create(
            name="Groceries", category_type=Category.CategoryType.EXPENSE
        )

    # Create
    def test_create_expense(self):
        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("50.00"),
            date=date(2024, 1, 15),
            note="Test grocery expense",
        )

        saved_expense = Expense.objects.get(id=expense.id)

        self.assertEqual(saved_expense.user, self.user)
        self.assertEqual(saved_expense.category, self.category)
        self.assertEqual(saved_expense.amount, Decimal("50.00"))
        self.assertEqual(saved_expense.date, date(2024, 1, 15))
        self.assertEqual(saved_expense.note, "Test grocery expense")
        self.assertEqual(
            str(saved_expense), f"{date(2024, 1, 15)} - Groceries - $50.00"
        )

    # Create without note
    def test_create_expense_without_note(self):
        """Test creating an expense without a note (optional field)."""
        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("25.00"),
            date=date(2024, 1, 20),
        )

        saved_expense = Expense.objects.get(id=expense.id)
        self.assertIsNone(saved_expense.note, "")

    # Update
    def test_update_expense(self):
        """Test updating an existing expense."""
        # Create an expense first
        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("50.00"),
            date=date(2024, 1, 15),
            note="Original note",
        )

        # Update the expense
        expense.amount = Decimal("75.00")
        expense.date = date(2024, 1, 20)
        expense.note = "Updated note"
        expense.save()

        # Retrieve and verify the updated expense
        updated_expense = Expense.objects.get(id=expense.id)
        self.assertEqual(updated_expense.amount, Decimal("75.00"))
        self.assertEqual(updated_expense.date, date(2024, 1, 20))
        self.assertEqual(updated_expense.note, "Updated note")
        self.assertEqual(updated_expense.user, self.user)
        self.assertEqual(updated_expense.category, self.category)

    # Delete
    def test_delete_expense(self):
        """Test deleting an existing expense."""
        # Create an expense first
        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("50.00"),
            date=date(2024, 1, 15),
            note="Test expense",
        )

        # Verify it exists
        self.assertIsNotNone(Expense.objects.get(id=expense.id))

        # Delete the expense
        expense.delete()

        # Verify it no longer exists
        with self.assertRaises(Expense.DoesNotExist):
            Expense.objects.get(id=expense.id)


# ----------------------Income Model Tests----------------------


class IncomeModelTest(TestCase):
    """
    Note: Income requires a User and Category (ForeignKey
    relationships).
    We use setUp() to create these once for all tests.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.category = Category.objects.create(
            name="Salary", category_type=Category.CategoryType.INCOME
        )

    def test_create_income(self):
        income = Income.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("2000.00"),
            date=date(2024, 1, 1),
            note="Monthly salary",
        )

        saved_income = Income.objects.get(id=income.id)

        self.assertEqual(saved_income.user, self.user)
        self.assertEqual(saved_income.category, self.category)
        self.assertEqual(saved_income.amount, Decimal("2000.00"))
        self.assertEqual(saved_income.date, date(2024, 1, 1))
        self.assertEqual(saved_income.note, "Monthly salary")
        self.assertEqual(
            str(saved_income), f"{date(2024, 1, 1)} - Salary - $2000.00"
        )

    # Update
    def test_update_income(self):
        """Test updating an existing income."""
        # Create an income first
        income = Income.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("2000.00"),
            date=date(2024, 1, 1),
            note="Original salary",
        )

        # Update the income
        income.amount = Decimal("2500.00")
        income.date = date(2024, 2, 1)
        income.note = "Updated salary with bonus"
        income.save()

        # Retrieve and verify the updated income
        updated_income = Income.objects.get(id=income.id)
        self.assertEqual(updated_income.amount, Decimal("2500.00"))
        self.assertEqual(updated_income.date, date(2024, 2, 1))
        self.assertEqual(updated_income.note, "Updated salary with bonus")
        self.assertEqual(updated_income.user, self.user)
        self.assertEqual(updated_income.category, self.category)

    # Delete
    def test_delete_income(self):
        """Test deleting an existing income."""
        # Create an income first
        income = Income.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("2000.00"),
            date=date(2024, 1, 1),
            note="Monthly salary",
        )

        # Verify it exists
        self.assertIsNotNone(Income.objects.get(id=income.id))

        # Delete the income
        income.delete()

        # Verify it no longer exists
        with self.assertRaises(Income.DoesNotExist):
            Income.objects.get(id=income.id)


# ----------------------Budget Model Tests----------------------


class BudgetModelTest(TestCase):
    """
    Note: Budget requires a User and Category (ForeignKey
    relationships).
    """

    def setUp(self):
        """Set up test data that all Budget tests can use."""
        # Create a user (required for Budget)
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Create a category (required for Budget)
        self.category = Category.objects.create(
            name="Groceries", category_type=Category.CategoryType.EXPENSE
        )

    # Create
    def test_create_budget(self):
        """Test that we can create a budget with user and category."""
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            amount=Decimal("500.00"),
            note="Monthly grocery budget",
        )

        saved_budget = Budget.objects.get(id=budget.id)

        self.assertEqual(saved_budget.user, self.user)
        self.assertEqual(saved_budget.category, self.category)
        self.assertEqual(saved_budget.start_date, date(2024, 1, 1))
        self.assertEqual(saved_budget.end_date, date(2024, 1, 31))
        self.assertEqual(saved_budget.amount, Decimal("500.00"))
        self.assertEqual(saved_budget.note, "Monthly grocery budget")

        self.assertIsNotNone(saved_budget.remaining_amount)
        self.assertIsNotNone(saved_budget.percentage)

    # Update
    def test_update_budget(self):
        """Test updating an existing budget."""
        # Create a budget first
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            amount=Decimal("500.00"),
            note="Original budget",
        )

        # Update the budget
        budget.start_date = date(2024, 2, 1)
        budget.end_date = date(2024, 2, 28)
        budget.amount = Decimal("600.00")
        budget.note = "Updated budget amount"
        budget.save()

        # Retrieve and verify the updated budget
        updated_budget = Budget.objects.get(id=budget.id)
        self.assertEqual(updated_budget.start_date, date(2024, 2, 1))
        self.assertEqual(updated_budget.end_date, date(2024, 2, 28))
        self.assertEqual(updated_budget.amount, Decimal("600.00"))
        self.assertEqual(updated_budget.note, "Updated budget amount")
        self.assertEqual(updated_budget.user, self.user)
        self.assertEqual(updated_budget.category, self.category)

    # Delete
    def test_delete_budget(self):
        """Test deleting an existing budget."""
        # Create a budget first
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            amount=Decimal("500.00"),
            note="Monthly grocery budget",
        )

        # Verify it exists
        self.assertIsNotNone(Budget.objects.get(id=budget.id))

        # Delete the budget
        budget.delete()

        # Verify it no longer exists
        with self.assertRaises(Budget.DoesNotExist):
            Budget.objects.get(id=budget.id)


# ----------------------Goal Model Tests----------------------


class GoalModelTest(TestCase):
    """
    Note: Goal requires a User (ForeignKey relationship).
    We use setUp() to create this once for all tests.
    """

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )

    # Create

    def test_create_goal(self):
        goal = Goal.objects.create(
            user=self.user,
            name="Save for Vacation",
            target=Decimal("5000.00"),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note="Saving for summer vacation",
        )

        saved_goal = Goal.objects.get(id=goal.id)

        self.assertEqual(saved_goal.user, self.user)
        self.assertEqual(saved_goal.name, "Save for Vacation")
        self.assertEqual(saved_goal.target, Decimal("5000.00"))
        self.assertEqual(saved_goal.deadline, date(2024, 12, 31))
        self.assertEqual(saved_goal.status, "In Progress")
        self.assertEqual(saved_goal.note, "Saving for summer vacation")
        self.assertEqual(
            str(saved_goal), "Save for Vacation - $5000.00 (In Progress)"
        )

    # Update
    def test_update_goal(self):
        """Test updating an existing goal."""
        # Create a goal first
        goal = Goal.objects.create(
            user=self.user,
            name="Save for Vacation",
            target=Decimal("5000.00"),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note="Original goal note",
        )

        # Update the goal
        goal.name = "Save for House Down Payment"
        goal.target = Decimal("10000.00")
        goal.deadline = date(2025, 6, 30)
        goal.status = "Completed"
        goal.note = "Updated goal - achieved early"
        goal.save()

        # Retrieve and verify the updated goal
        updated_goal = Goal.objects.get(id=goal.id)
        self.assertEqual(updated_goal.name, "Save for House Down Payment")
        self.assertEqual(updated_goal.target, Decimal("10000.00"))
        self.assertEqual(updated_goal.deadline, date(2025, 6, 30))
        self.assertEqual(updated_goal.status, "Completed")
        self.assertEqual(updated_goal.note, "Updated goal - achieved early")
        self.assertEqual(updated_goal.user, self.user)

    # Delete
    def test_delete_goal(self):
        """Test deleting an existing goal."""
        # Create a goal first
        goal = Goal.objects.create(
            user=self.user,
            name="Save for Vacation",
            target=Decimal("5000.00"),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note="Saving for summer vacation",
        )

        # Verify it exists
        self.assertIsNotNone(Goal.objects.get(id=goal.id))

        # Delete the goal
        goal.delete()

        # Verify it no longer exists
        with self.assertRaises(Goal.DoesNotExist):
            Goal.objects.get(id=goal.id)
