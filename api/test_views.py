"""Test cases for the api API views."""

from decimal import Decimal
from datetime import date
from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Expense, Income, Budget, Goal

# pylint: disable=no-member
# pylint: disable=missing-function-docstring

# ----------------------API View Tests----------------------


class ExpenseAPITest(TestCase):
    """
    Test cases for the Expense API endpoints.
    Tests authentication, CRUD operations, and user isolation.
    """

    def setUp(self):
        """Set up test data for API tests."""
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Create another user (to test user isolation)
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        # Create a category
        self.category = Category.objects.create(
            name="Groceries", category_type=Category.CategoryType.EXPENSE
        )
        # Create an API client
        self.client = APIClient()
        # Authenticate the client for all tests
        # (can be overridden in individual tests if needed)
        self.client.force_authenticate(user=self.user)

    def test_list_expenses_authenticated(self):
        """Test that authenticated users can list their expenses."""
        # Create some expenses for the test user
        Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("50.00"),
            date=date(2024, 1, 15),
            note="Test expense",
        )

        response = self.client.get("/expenses/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that we got back data (should be a list)
        self.assertIsInstance(response.data, list)

        # Check that we got back 1 expense
        self.assertEqual(len(response.data), 1)

        # Check that the expense data is correct
        expense_data = response.data[0]
        self.assertEqual(expense_data["amount"], "50.00")
        self.assertEqual(expense_data["note"], "Test expense")

    def test_create_expense(self):
        """Test creating an expense via POST request."""
        # Data to send in the POST request
        expense_data = {
            "category_id": self.category.id,
            "amount": "75.50",
            "date": "2024-02-15",
            "note": "New expense via API",
        }

        # Make a POST request to create an expense
        response = self.client.post("/expenses/", expense_data, format="json")

        # Check that the request was successful (status 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the expense was created with correct data
        self.assertEqual(response.data["amount"], "75.50")
        self.assertEqual(response.data["note"], "New expense via API")
        self.assertEqual(response.data["date"], "2024-02-15")
        # Check that user was automatically set (read-only field)
        self.assertEqual(response.data["user"], self.user.id)

        # Verify it exists in the database
        expense = Expense.objects.get(id=response.data["id"])
        self.assertEqual(expense.amount, Decimal("75.50"))
        self.assertEqual(expense.user, self.user)

    def test_get_expense_detail(self):
        """Test retrieving a single expense by ID."""
        # Create an expense first
        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("100.00"),
            date=date(2024, 3, 10),
            note="Detail test expense",
        )

        # Make a GET request to retrieve the expense
        response = self.client.get(f"/expenses/{expense.id}/")

        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the expense data is correct
        self.assertEqual(response.data["amount"], "100.00")
        self.assertEqual(response.data["note"], "Detail test expense")
        self.assertEqual(response.data["id"], expense.id)

    def test_update_expense(self):
        """Test updating an expense via PUT request."""
        # Create an expense first
        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("50.00"),
            date=date(2024, 1, 15),
            note="Original note",
        )

        # Data to send in the PUT request
        updated_data = {
            "category_id": self.category.id,
            "amount": "125.00",
            "date": "2024-04-20",
            "note": "Updated via API",
        }

        # Make a PUT request to update the expense
        response = self.client.put(
            f"/expenses/{expense.id}/", updated_data, format="json"
        )

        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the expense was updated
        self.assertEqual(response.data["amount"], "125.00")
        self.assertEqual(response.data["note"], "Updated via API")
        self.assertEqual(response.data["date"], "2024-04-20")

        # Verify it was updated in the database
        expense.refresh_from_db()
        self.assertEqual(expense.amount, Decimal("125.00"))
        self.assertEqual(expense.note, "Updated via API")

    def test_delete_expense(self):
        """Test deleting an expense via DELETE request."""
        # Create an expense first
        expense = Expense.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("50.00"),
            date=date(2024, 1, 15),
            note="To be deleted",
        )

        # Verify it exists
        self.assertIsNotNone(Expense.objects.get(id=expense.id))

        # Make a DELETE request
        response = self.client.delete(f"/expenses/{expense.id}/")

        # Check that the request was successful (status 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify it no longer exists in the database
        with self.assertRaises(Expense.DoesNotExist):
            Expense.objects.get(id=expense.id)


# ----------------------Income API Tests----------------------


class IncomeAPITest(TestCase):
    """
    Test cases for the Income API endpoints.
    Tests authentication, CRUD operations, and user isolation.
    """

    def setUp(self):
        """Set up test data for API tests."""
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Create another user (to test user isolation)
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        # Create a category
        self.category = Category.objects.create(
            name="Salary", category_type=Category.CategoryType.INCOME
        )
        # Create an API client
        self.client = APIClient()
        # Authenticate the client for all tests
        # (can be overridden in individual tests if needed)
        self.client.force_authenticate(user=self.user)

    def test_list_income_authenticated(self):
        """Test that authenticated users can list their income."""
        # Create some income for the test user
        Income.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("2000.00"),
            date=date(2024, 1, 1),
            note="Test income",
        )

        response = self.client.get("/income/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that we got back data (should be a list)
        self.assertIsInstance(response.data, list)

        # Check that we got back 1 income
        self.assertEqual(len(response.data), 1)

        # Check that the income data is correct
        income_data = response.data[0]
        self.assertEqual(income_data["amount"], "2000.00")
        self.assertEqual(income_data["note"], "Test income")

    def test_create_income(self):
        """Test creating an income via POST request."""
        # Data to send in the POST request
        income_data = {
            "category_id": self.category.id,
            "amount": "2500.00",
            "date": "2024-02-01",
            "note": "New income via API",
        }

        # Make a POST request to create an income
        response = self.client.post("/income/", income_data, format="json")

        # Check that the request was successful (status 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the income was created with correct data
        self.assertEqual(response.data["amount"], "2500.00")
        self.assertEqual(response.data["note"], "New income via API")
        self.assertEqual(response.data["date"], "2024-02-01")
        # Check that user was automatically set (read-only field)
        self.assertEqual(response.data["user"], self.user.id)

        # Verify it exists in the database
        income = Income.objects.get(id=response.data["id"])
        self.assertEqual(income.amount, Decimal("2500.00"))
        self.assertEqual(income.user, self.user)

    def test_get_income_detail(self):
        """Test retrieving a single income by ID."""
        # Create an income first
        income = Income.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("3000.00"),
            date=date(2024, 3, 1),
            note="Detail test income",
        )

        # Make a GET request to retrieve the income
        response = self.client.get(f"/income/{income.id}/")

        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the income data is correct
        self.assertEqual(response.data["amount"], "3000.00")
        self.assertEqual(response.data["note"], "Detail test income")
        self.assertEqual(response.data["id"], income.id)

    def test_update_income(self):
        """Test updating an income via PUT request."""
        # Create an income first
        income = Income.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("2000.00"),
            date=date(2024, 1, 1),
            note="Original note",
        )

        # Data to send in the PUT request
        updated_data = {
            "category_id": self.category.id,
            "amount": "3500.00",
            "date": "2024-04-01",
            "note": "Updated via API",
        }

        # Make a PUT request to update the income
        response = self.client.put(
            f"/income/{income.id}/", updated_data, format="json"
        )

        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the income was updated
        self.assertEqual(response.data["amount"], "3500.00")
        self.assertEqual(response.data["note"], "Updated via API")
        self.assertEqual(response.data["date"], "2024-04-01")

        # Verify it was updated in the database
        income.refresh_from_db()
        self.assertEqual(income.amount, Decimal("3500.00"))
        self.assertEqual(income.note, "Updated via API")

    def test_delete_income(self):
        """Test deleting an income via DELETE request."""
        # Create an income first
        income = Income.objects.create(
            user=self.user,
            category=self.category,
            amount=Decimal("2000.00"),
            date=date(2024, 1, 1),
            note="To be deleted",
        )

        # Verify it exists
        self.assertIsNotNone(Income.objects.get(id=income.id))

        # Make a DELETE request
        response = self.client.delete(f"/income/{income.id}/")

        # Check that the request was successful (status 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify it no longer exists in the database
        with self.assertRaises(Income.DoesNotExist):
            Income.objects.get(id=income.id)


# ----------------------Budget API Tests----------------------


class BudgetAPITest(TestCase):
    """
    Test cases for the Budget API endpoints.
    Tests authentication, CRUD operations, and user isolation.
    """

    def setUp(self):
        """Set up test data for API tests."""
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Create another user (to test user isolation)
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        # Create a category
        self.category = Category.objects.create(
            name="Groceries", category_type=Category.CategoryType.EXPENSE
        )
        # Create an API client
        self.client = APIClient()
        # Authenticate the client for all tests
        # (can be overridden in individual tests if needed)
        self.client.force_authenticate(user=self.user)

    def test_list_budgets_authenticated(self):
        """Test that authenticated users can list their budgets."""
        # Create some budgets for the test user
        Budget.objects.create(
            user=self.user,
            category=self.category,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            amount=Decimal("500.00"),
            note="Test budget",
        )

        response = self.client.get("/budgets/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that we got back data (should be a list)
        self.assertIsInstance(response.data, list)

        # Check that we got back 1 budget
        self.assertEqual(len(response.data), 1)

        # Check that the budget data is correct
        budget_data = response.data[0]
        self.assertEqual(budget_data["amount"], "500.00")
        self.assertEqual(budget_data["note"], "Test budget")

    def test_create_budget(self):
        """Test creating a budget via POST request."""
        # Data to send in the POST request
        budget_data = {
            "category_id": self.category.id,
            "start_date": "2024-02-01",
            "end_date": "2024-02-28",
            "amount": "600.00",
            "note": "New budget via API",
        }

        # Make a POST request to create a budget
        response = self.client.post("/budgets/", budget_data, format="json")

        # Check that the request was successful (status 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the budget was created with correct data
        self.assertEqual(response.data["amount"], "600.00")
        self.assertEqual(response.data["note"], "New budget via API")
        self.assertEqual(response.data["start_date"], "2024-02-01")
        self.assertEqual(response.data["end_date"], "2024-02-28")
        # Check that user was automatically set (read-only field)
        self.assertEqual(response.data["user"], self.user.id)

        # Verify it exists in the database
        budget = Budget.objects.get(id=response.data["id"])
        self.assertEqual(budget.amount, Decimal("600.00"))
        self.assertEqual(budget.user, self.user)

    def test_get_budget_detail(self):
        """Test retrieving a single budget by ID."""
        # Create a budget first
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            start_date=date(2024, 3, 1),
            end_date=date(2024, 3, 31),
            amount=Decimal("700.00"),
            note="Detail test budget",
        )

        # Make a GET request to retrieve the budget
        response = self.client.get(f"/budgets/{budget.id}/")

        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the budget data is correct
        self.assertEqual(response.data["amount"], "700.00")
        self.assertEqual(response.data["note"], "Detail test budget")
        self.assertEqual(response.data["id"], budget.id)

    def test_update_budget(self):
        """Test updating a budget via PUT request."""
        # Create a budget first
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            amount=Decimal("500.00"),
            note="Original note",
        )

        # Data to send in the PUT request
        updated_data = {
            "category_id": self.category.id,
            "start_date": "2024-04-01",
            "end_date": "2024-04-30",
            "amount": "800.00",
            "note": "Updated via API",
        }

        # Make a PUT request to update the budget
        response = self.client.put(
            f"/budgets/{budget.id}/", updated_data, format="json"
        )

        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the budget was updated
        self.assertEqual(response.data["amount"], "800.00")
        self.assertEqual(response.data["note"], "Updated via API")
        self.assertEqual(response.data["start_date"], "2024-04-01")
        self.assertEqual(response.data["end_date"], "2024-04-30")

        # Verify it was updated in the database
        budget.refresh_from_db()
        self.assertEqual(budget.amount, Decimal("800.00"))
        self.assertEqual(budget.note, "Updated via API")

    def test_delete_budget(self):
        """Test deleting a budget via DELETE request."""
        # Create a budget first
        budget = Budget.objects.create(
            user=self.user,
            category=self.category,
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 31),
            amount=Decimal("500.00"),
            note="To be deleted",
        )

        # Verify it exists
        self.assertIsNotNone(Budget.objects.get(id=budget.id))

        # Make a DELETE request
        response = self.client.delete(f"/budgets/{budget.id}/")

        # Check that the request was successful (status 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify it no longer exists in the database
        with self.assertRaises(Budget.DoesNotExist):
            Budget.objects.get(id=budget.id)


# ----------------------Goal API Tests----------------------


class GoalAPITest(TestCase):
    """
    Test cases for the Goal API endpoints.
    Tests authentication, CRUD operations, and user isolation.
    """

    def setUp(self):
        """Set up test data for API tests."""
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Create another user (to test user isolation)
        self.other_user = User.objects.create_user(
            username="otheruser", password="otherpass123"
        )
        # Create an API client
        self.client = APIClient()
        # Authenticate the client for all tests
        # (can be overridden in individual tests if needed)
        self.client.force_authenticate(user=self.user)

    def test_list_goals_authenticated(self):
        """Test that authenticated users can list their goals."""
        # Create some goals for the test user
        Goal.objects.create(
            user=self.user,
            name="Save for Vacation",
            target=Decimal("5000.00"),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note="Test goal",
        )

        response = self.client.get("/goals/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that we got back data (should be a list)
        self.assertIsInstance(response.data, list)

        # Check that we got back 1 goal
        self.assertEqual(len(response.data), 1)

        # Check that the goal data is correct
        goal_data = response.data[0]
        self.assertEqual(goal_data["target"], "5000.00")
        self.assertEqual(goal_data["note"], "Test goal")

    def test_create_goal(self):
        """Test creating a goal via POST request."""
        # Data to send in the POST request
        goal_data = {
            "name": "Save for House",
            "target": "10000.00",
            "deadline": "2025-06-30",
            "status": "Not Started",
            "note": "New goal via API",
        }

        # Make a POST request to create a goal
        response = self.client.post("/goals/", goal_data, format="json")

        # Check that the request was successful (status 201 Created)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check that the goal was created with correct data
        self.assertEqual(response.data["name"], "Save for House")
        self.assertEqual(response.data["target"], "10000.00")
        self.assertEqual(response.data["note"], "New goal via API")
        self.assertEqual(response.data["deadline"], "2025-06-30")
        self.assertEqual(response.data["status"], "Not Started")
        # Check that user was automatically set (read-only field)
        self.assertEqual(response.data["user"], self.user.id)

        # Verify it exists in the database
        goal = Goal.objects.get(id=response.data["id"])
        self.assertEqual(goal.target, Decimal("10000.00"))
        self.assertEqual(goal.user, self.user)

    def test_get_goal_detail(self):
        """Test retrieving a single goal by ID."""
        # Create a goal first
        goal = Goal.objects.create(
            user=self.user,
            name="Save for Car",
            target=Decimal("15000.00"),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note="Detail test goal",
        )

        # Make a GET request to retrieve the goal
        response = self.client.get(f"/goals/{goal.id}/")

        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the goal data is correct
        self.assertEqual(response.data["target"], "15000.00")
        self.assertEqual(response.data["note"], "Detail test goal")
        self.assertEqual(response.data["id"], goal.id)

    def test_update_goal(self):
        """Test updating a goal via PUT request."""
        # Create a goal first
        goal = Goal.objects.create(
            user=self.user,
            name="Save for Vacation",
            target=Decimal("5000.00"),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note="Original note",
        )

        # Data to send in the PUT request
        updated_data = {
            "name": "Save for House Down Payment",
            "target": "20000.00",
            "deadline": "2025-12-31",
            "status": "Completed",
            "note": "Updated via API",
        }

        # Make a PUT request to update the goal
        response = self.client.put(
            f"/goals/{goal.id}/", updated_data, format="json"
        )

        # Check that the request was successful
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check that the goal was updated
        self.assertEqual(response.data["name"], "Save for House Down Payment")
        self.assertEqual(response.data["target"], "20000.00")
        self.assertEqual(response.data["note"], "Updated via API")
        self.assertEqual(response.data["status"], "Completed")

        # Verify it was updated in the database
        goal.refresh_from_db()
        self.assertEqual(goal.target, Decimal("20000.00"))
        self.assertEqual(goal.note, "Updated via API")

    def test_delete_goal(self):
        """Test deleting a goal via DELETE request."""
        # Create a goal first
        goal = Goal.objects.create(
            user=self.user,
            name="Save for Vacation",
            target=Decimal("5000.00"),
            deadline=date(2024, 12, 31),
            status="In Progress",
            note="To be deleted",
        )

        # Verify it exists
        self.assertIsNotNone(Goal.objects.get(id=goal.id))

        # Make a DELETE request
        response = self.client.delete(f"/goals/{goal.id}/")

        # Check that the request was successful (status 204 No Content)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # Verify it no longer exists in the database
        with self.assertRaises(Goal.DoesNotExist):
            Goal.objects.get(id=goal.id)
