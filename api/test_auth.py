"""Test cases for authentication and authorization (security tests)."""

from decimal import Decimal
from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Expense, Income, Budget, Goal

# pylint: disable=no-member
# pylint: disable=missing-function-docstring

# ----------------------Authentication & Authorization Tests-----------


class ExpenseAuthTest(TestCase):
    """
    Test cases for Expense API authentication and authorization.
    Tests unauthenticated access, user isolation, access control.
    """

    def setUp(self):
        """Set up test data for auth tests."""
        # Create two users
        self.user1 = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        # Create a category
        self.category = Category.objects.create(
            name="Groceries", category_type=Category.CategoryType.EXPENSE
        )
        # Create an API client (not authenticated by default)
        self.client = APIClient()

    def test_list_expenses_unauthenticated(self):
        """Test that unauthenticated users cannot list expenses."""
        # Don't authenticate - client is not authenticated
        response = self.client.get("/expenses/")

        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_expense_unauthenticated(self):
        """Test that unauthenticated users cannot create expenses."""
        expense_data = {
            "category_id": self.category.id,
            "amount": "50.00",
            "date": "2024-01-15",
            "note": "Unauthorized attempt",
        }

        # Don't authenticate - try to create expense
        response = self.client.post("/expenses/", expense_data, format="json")

        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_see_other_users_expenses(self):
        """Test that users can only see their own expenses."""
        # Create an expense for user2
        Expense.objects.create(
            user=self.user2,
            category=self.category,
            amount=Decimal("100.00"),
            date=date(2024, 1, 15),
            note="User2's expense",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to list expenses
        response = self.client.get("/expenses/")

        # Should be successful, but should see 0 expenses
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_cannot_access_other_users_expense_detail(self):
        """Test users cannot access another user's expense by ID."""
        # Create an expense for user2
        expense = Expense.objects.create(
            user=self.user2,
            category=self.category,
            amount=Decimal("100.00"),
            date=date(2024, 1, 15),
            note="User2's expense",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to access user2's expense
        response = self.client.get(f"/expenses/{expense.id}/")

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_update_other_users_expense(self):
        """Test that users cannot update another user's expense."""
        # Create an expense for user2
        expense = Expense.objects.create(
            user=self.user2,
            category=self.category,
            amount=Decimal("100.00"),
            date=date(2024, 1, 15),
            note="User2's expense",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to update user2's expense
        updated_data = {
            "category_id": self.category.id,
            "amount": "200.00",
            "date": "2024-01-15",
            "note": "Hacked!",
        }
        response = self.client.put(
            f"/expenses/{expense.id}/", updated_data, format="json"
        )

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the expense wasn't changed
        expense.refresh_from_db()
        self.assertEqual(expense.amount, Decimal("100.00"))
        self.assertEqual(expense.note, "User2's expense")

    def test_user_cannot_delete_other_users_expense(self):
        """Test that users cannot delete another user's expense."""
        # Create an expense for user2
        expense = Expense.objects.create(
            user=self.user2,
            category=self.category,
            amount=Decimal("100.00"),
            date=date(2024, 1, 15),
            note="User2's expense",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to delete user2's expense
        response = self.client.delete(f"/expenses/{expense.id}/")

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the expense still exists
        self.assertIsNotNone(Expense.objects.get(id=expense.id))


# ----------------------Income Auth Tests----------------------


class IncomeAuthTest(TestCase):
    """
    Test cases for Income API authentication and authorization.
    Tests unauthenticated access, user isolation, access control.
    """

    def setUp(self):
        """Set up test data for auth tests."""
        # Create two users
        self.user1 = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        # Create a category (INCOME type for income)
        self.category = Category.objects.create(
            name="Salary", category_type=Category.CategoryType.INCOME
        )
        # Create an API client (not authenticated by default)
        self.client = APIClient()

    def test_list_income_unauthenticated(self):
        """Test that unauthenticated users cannot list income."""
        # Don't authenticate - client is not authenticated
        response = self.client.get("/income/")

        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_income_unauthenticated(self):
        """Test that unauthenticated users cannot create income."""
        income_data = {
            "category_id": self.category.id,
            "amount": "2000.00",
            "date": "2024-01-01",
            "note": "Unauthorized attempt",
        }

        # Don't authenticate - try to create income
        response = self.client.post("/income/", income_data, format="json")

        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_see_other_users_income(self):
        """Test that users can only see their own income."""
        # Create an income for user2
        Income.objects.create(
            user=self.user2,
            category=self.category,
            amount=Decimal("3000.00"),
            date=date(2024, 1, 1),
            note="User2's income",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to list income
        response = self.client.get("/income/")

        # Should be successful, but should see 0 income
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_cannot_access_other_users_income_detail(self):
        """Test users cannot access another user's income by ID."""
        # Create an income for user2
        income = Income.objects.create(
            user=self.user2,
            category=self.category,
            amount=Decimal("3000.00"),
            date=date(2024, 1, 1),
            note="User2's income",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to access user2's income
        response = self.client.get(f"/income/{income.id}/")

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_update_other_users_income(self):
        """Test that users cannot update another user's income."""
        # Create an income for user2
        income = Income.objects.create(
            user=self.user2,
            category=self.category,
            amount=Decimal("3000.00"),
            date=date(2024, 1, 1),
            note="User2's income",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to update user2's income
        updated_data = {
            "category_id": self.category.id,
            "amount": "5000.00",
            "date": "2024-01-01",
            "note": "Hacked!",
        }
        response = self.client.put(
            f"/income/{income.id}/", updated_data, format="json"
        )

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the income wasn't changed
        income.refresh_from_db()
        self.assertEqual(income.amount, Decimal("3000.00"))
        self.assertEqual(income.note, "User2's income")

    def test_user_cannot_delete_other_users_income(self):
        """Test that users cannot delete another user's income."""
        # Create an income for user2
        income = Income.objects.create(
            user=self.user2,
            category=self.category,
            amount=Decimal("3000.00"),
            date=date(2024, 1, 1),
            note="User2's income",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to delete user2's income
        response = self.client.delete(f"/income/{income.id}/")

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the income still exists
        self.assertIsNotNone(Income.objects.get(id=income.id))


# ----------------------Budget Auth Tests----------------------


class BudgetAuthTest(TestCase):
    """
    Test cases for Budget API authentication and authorization.
    Tests unauthenticated access, user isolation, access control.
    """

    def setUp(self):
        """Set up test data for auth tests."""
        # Create two users
        self.user1 = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        # Create a category (EXPENSE type for budget)
        self.category = Category.objects.create(
            name="Salary", category_type=Category.CategoryType.EXPENSE
        )
        # Create an API client (not authenticated by default)
        self.client = APIClient()

    def test_list_budgets_unauthenticated(self):
        """Test that unauthenticated users cannot list budgets."""
        # Don't authenticate - client is not authenticated
        response = self.client.get("/budgets/")

        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_budget_unauthenticated(self):
        """Test that unauthenticated users cannot create budgets."""
        budget_data = {
            "category_id": self.category.id,
            "start_date": "2024-01-01",
            "end_date": "2024-02-02",
            "amount": "2000.00",
            "note": "Unauthorized attempt",
            "dates": "2024-01-01, 2024-02-02",
        }

        # Don't authenticate - try to create income
        response = self.client.post("/budgets/", budget_data, format="json")

        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_see_other_users_budgets(self):
        """Test that users can only see their own income."""
        # Create a budget for user2
        Budget.objects.create(
            user=self.user2,
            category=self.category,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 2, 2),
            amount=Decimal("2000.00"),
            note="User2's budget",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to list income
        response = self.client.get("/budgets/")

        # Should be successful, but should see 0 income
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_cannot_access_other_users_budget_detail(self):
        """Test users cannot access another user's income by ID."""
        # Create a budget for user2
        budget = Budget.objects.create(
            user=self.user2,
            category=self.category,
            start_date="2024-01-01",
            end_date="2024-02-02",
            amount=Decimal("2000.00"),
            note="User2's budget",
            dates="2024-01-01, 2024-02-02",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to access user2's income
        response = self.client.get(f"/budgets/{budget.id}/")

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_update_other_users_budget(self):
        """Test that users cannot update another user's income."""
        # Create a budget for user2
        budget = Budget.objects.create(
            user=self.user2,
            category=self.category,
            start_date="2024-01-01",
            end_date="2024-02-02",
            amount=Decimal("2000.00"),
            note="User2's budget",
            dates="2024-01-01, 2024-02-02",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to update user2's income
        updated_data = {
            "category_id": self.category.id,
            "start_date": "2024-01-01",
            "end_date": "2024-02-02",
            "amount": "5000.00",
            "note": "Hacked!",
        }
        response = self.client.put(
            f"/budgets/{budget.id}/", updated_data, format="json"
        )

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the budget wasn't changed
        budget.refresh_from_db()
        self.assertEqual(budget.amount, Decimal("2000.00"))
        self.assertEqual(budget.note, "User2's budget")

    def test_user_cannot_delete_other_users_budget(self):
        """Test that users cannot delete another user's income."""
        # Create a budget for user2
        budget = Budget.objects.create(
            user=self.user2,
            category=self.category,
            start_date="2024-01-01",
            end_date="2024-02-02",
            amount=Decimal("2000.00"),
            note="User2's budget",
            dates="2024-01-01, 2024-02-02",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to delete user2's income
        response = self.client.delete(f"/budgets/{budget.id}/")

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the budget still exists
        self.assertIsNotNone(Budget.objects.get(id=budget.id))


# ----------------------Goal Auth Tests----------------------


class GoalAuthTest(TestCase):
    """
    Test cases for Goal API authentication and authorization.
    Tests unauthenticated access, user isolation, access control.
    """

    def setUp(self):
        """Set up test data for auth tests."""
        # Create two users
        self.user1 = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        self.user2 = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        # Create an API client (not authenticated by default)
        # Note: Goal doesn't require a category
        self.client = APIClient()

    def test_list_goals_unauthenticated(self):
        """Test that unauthenticated users cannot list goals."""
        # Don't authenticate - client is not authenticated
        response = self.client.get("/goals/")

        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_goal_unauthenticated(self):
        """Test that unauthenticated users cannot create goals."""
        goal_data = {
            "name": "Save for Vacation",
            "target": "5000.00",
            "deadline": "2024-12-31",
            "status": "In Progress",
            "note": "Unauthorized attempt",
        }

        # Don't authenticate - try to create goal
        response = self.client.post("/goals/", goal_data, format="json")

        # Should return 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_see_other_users_goals(self):
        """Test that users can only see their own goals."""
        # Create a goal for user2
        Goal.objects.create(
            user=self.user2,
            name="Save for House",
            target=Decimal("10000.00"),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note="User2's goal",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to list goals
        response = self.client.get("/goals/")

        # Should be successful, but should see 0 goals
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 0)

    def test_user_cannot_access_other_users_goal_detail(self):
        """Test users cannot access another user's goal by ID."""
        # Create a goal for user2
        goal = Goal.objects.create(
            user=self.user2,
            name="Save for House",
            target=Decimal("10000.00"),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note="User2's goal",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to access user2's goal
        response = self.client.get(f"/goals/{goal.id}/")

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_user_cannot_update_other_users_goal(self):
        """Test that users cannot update another user's goal."""
        # Create a goal for user2
        goal = Goal.objects.create(
            user=self.user2,
            name="Save for House",
            target=Decimal("10000.00"),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note="User2's goal",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to update user2's goal
        updated_data = {
            "name": "Save for Car",
            "target": "20000.00",
            "deadline": "2025-06-30",
            "status": "Completed",
            "note": "Hacked!",
        }
        response = self.client.put(
            f"/goals/{goal.id}/", updated_data, format="json"
        )

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the goal wasn't changed
        goal.refresh_from_db()
        self.assertEqual(goal.target, Decimal("10000.00"))
        self.assertEqual(goal.note, "User2's goal")
        self.assertEqual(goal.name, "Save for House")

    def test_user_cannot_delete_other_users_goal(self):
        """Test that users cannot delete another user's goal."""
        # Create a goal for user2
        goal = Goal.objects.create(
            user=self.user2,
            name="Save for House",
            target=Decimal("10000.00"),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note="User2's goal",
        )

        # Authenticate as self.user1
        self.client.force_authenticate(user=self.user1)

        # Try to delete user2's goal
        response = self.client.delete(f"/goals/{goal.id}/")

        # Should return 404 Not Found (user isolation)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # Verify the goal still exists
        self.assertIsNotNone(Goal.objects.get(id=goal.id))
