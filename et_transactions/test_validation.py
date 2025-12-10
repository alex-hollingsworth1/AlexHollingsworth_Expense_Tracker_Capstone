"""Test cases for validation and error handling."""

from django.test import TestCase
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status
from .models import Category, Expense, Income, Budget, Goal

# pylint: disable=no-member
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring

# ----------------------Validation & Error Tests----------------------


class ExpenseValidationTest(TestCase):

    def setUp(self):
        """Set up test data for validation tests."""
        # Create a user
        self.user1 = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Create a category
        self.category = Category.objects.create(
            name="Groceries", category_type=Category.CategoryType.EXPENSE
        )
        # Create an API client
        self.client = APIClient()
        # Authenticate the client
        self.client.force_authenticate(user=self.user1)

    def test_create_expense_missing_amount(self):
        """Test that creating an expense without amount fails."""
        # Create expense data without 'amount' field
        expense_data = {
            "category_id": self.category.id,
            "date": "2024-01-15",
            "note": "Test expense",
        }

        response = self.client.post("/expenses/", expense_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'amount' is required
        self.assertIn("amount", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["amount"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_expense_missing_date(self):
        """Test that creating an expense without date fails."""
        # Create expense data without 'date' field
        expense_data = {
            "category_id": self.category.id,
            "amount": "200.00",
            "note": "Test expense",
        }

        response = self.client.post("/expenses/", expense_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'date' is required
        self.assertIn("date", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["date"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_expense_negative_amount(self):
        """Test that creating an expense with negative amount fails."""
        # Create expense data with negative amount
        expense_data = {
            "category_id": self.category.id,
            "amount": "-10.00",
            "date": "2024-01-15",
            "note": "Test expense",
        }

        response = self.client.post("/expenses/", expense_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'amount' is invalid
        self.assertIn("amount", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["amount"][0]).lower()
        # Check for common validation messages about negative values
        self.assertTrue(
            "greater" in error_message
            or "positive" in error_message
            or "invalid" in error_message
        )

    def test_create_expense_no_category_id(self):
        """Test that creating an expense with no category ID fails."""
        # Create expense data without 'category_id' field
        expense_data = {
            "amount": "50.00",
            "date": "2024-01-15",
            "note": "Test expense",
        }

        response = self.client.post("/expenses/", expense_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'category_id' is required
        # Note: The serializer uses 'category_id' for write operations
        self.assertIn("category_id", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["category_id"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_expense_invalid_amount_type(self):
        """Test that creating an expense with invalid amount type
        fails."""
        # Create expense data with amount as string instead of number
        expense_data = {
            "category_id": self.category.id,
            "amount": "not a number",
            "date": "2024-01-15",
            "note": "Test expense",
        }

        response = self.client.post("/expenses/", expense_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'amount' is invalid
        self.assertIn("amount", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["amount"][0]).lower()
        # Check for common validation messages about invalid number
        # åformat
        self.assertTrue(
            "number" in error_message
            or "decimal" in error_message
            or "invalid" in error_message
        )

    def test_create_expense_invalid_date_format(self):
        """Test that creating an expense with invalid date format
        fails."""

        expense_data = {
            "category_id": self.category.id,
            "amount": "50.00",
            "date": "not-a-date",
            "note": "Test expense",
        }

        response = self.client.post("/expenses/", expense_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("date", response.data)

        error_message = str(response.data["date"][0]).lower()

        self.assertTrue("date" in error_message or "invalid" in error_message)

    def test_create_expense_invalid_category_id_type(self):
        """Test that creating an expense with invalid category ID
        fails."""

        expense_data = {
            "category_id": "not a number",
            "amount": "50.00",
            "date": "2024-01-15",
            "note": "Test expense",
        }

        response = self.client.post("/expenses/", expense_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("category_id", response.data)

        error_message = str(response.data["category_id"][0]).lower()

        # Check for common validation messages about invalid type
        # PrimaryKeyRelatedField might return "incorrect type" or "invalid"
        self.assertTrue(
            "number" in error_message
            or "decimal" in error_message
            or "invalid" in error_message
            or "incorrect" in error_message
            or "type" in error_message
        )

    def test_create_expense_note_too_long(self):
        """Test that creating an expense with a note that is too long
        fails."""

        expense_data = {
            "category_id": self.category.id,
            "amount": "50.00",
            "date": "2024-01-15",
            "note": ("x" * 251),
        }

        response = self.client.post("/expenses/", expense_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("note", response.data)

        error_message = str(response.data["note"][0]).lower()

        self.assertTrue(
            "length" in error_message
            or "characters" in error_message
            or "250" in error_message
        )


class IncomeValidationTest(TestCase):

    def setUp(self):
        """Set up test data for validation tests."""
        # Create a user
        self.user1 = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Create a category
        self.category = Category.objects.create(
            name="Salary", category_type=Category.CategoryType.INCOME
        )
        # Create an API client
        self.client = APIClient()
        # Authenticate the client
        self.client.force_authenticate(user=self.user1)

    def test_create_income_missing_amount(self):
        """Test that creating an income without amount fails."""
        # Create income data without 'amount' field
        income_data = {
            "category_id": self.category.id,
            "date": "2024-01-15",
            "note": "Test income",
        }

        response = self.client.post("/income/", income_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'amount' is required
        self.assertIn("amount", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["amount"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_income_missing_date(self):
        """Test that creating an income without date fails."""
        # Create income data without 'date' field
        income_data = {
            "category_id": self.category.id,
            "amount": "200.00",
            "note": "Test income",
        }

        response = self.client.post("/income/", income_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'date' is required
        self.assertIn("date", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["date"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_income_negative_amount(self):
        """Test that creating an income with negative amount fails."""
        # Create income data with negative amount
        income_data = {
            "category_id": self.category.id,
            "amount": "-10.00",
            "date": "2024-01-15",
            "note": "Test income",
        }

        response = self.client.post("/income/", income_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'amount' is invalid
        self.assertIn("amount", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["amount"][0]).lower()
        # Check for common validation messages about negative values
        self.assertTrue(
            "greater" in error_message
            or "positive" in error_message
            or "invalid" in error_message
        )

    def test_create_income_no_category_id(self):
        """Test that creating an income with no category ID fails."""
        # Create income data without 'category_id' field
        income_data = {
            "amount": "50.00",
            "date": "2024-01-15",
            "note": "Test income",
        }

        response = self.client.post("/income/", income_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'category_id' is required
        # Note: The serializer uses 'category_id' for write operations
        self.assertIn("category_id", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["category_id"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_income_invalid_amount_type(self):
        """Test that creating an income with invalid amount type fails."""
        # Create income data with amount as string instead of number
        income_data = {
            "category_id": self.category.id,
            "amount": "not a number",
            "date": "2024-01-15",
            "note": "Test income",
        }

        response = self.client.post("/income/", income_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'amount' is invalid
        self.assertIn("amount", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["amount"][0]).lower()
        # Check for common validation messages about invalid number format
        self.assertTrue(
            "number" in error_message
            or "decimal" in error_message
            or "invalid" in error_message
        )

    def test_create_income_invalid_date_format(self):
        """Test that creating an income with invalid date format fails."""

        income_data = {
            "category_id": self.category.id,
            "amount": "50.00",
            "date": "not-a-date",
            "note": "Test income",
        }

        response = self.client.post("/income/", income_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("date", response.data)

        error_message = str(response.data["date"][0]).lower()

        self.assertTrue("date" in error_message or "invalid" in error_message)

    def test_create_income_invalid_category_id_type(self):
        """Test that creating an income with invalid category ID fails."""

        income_data = {
            "category_id": "not a number",
            "amount": "50.00",
            "date": "2024-01-15",
            "note": "Test income",
        }

        response = self.client.post("/income/", income_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("category_id", response.data)

        error_message = str(response.data["category_id"][0]).lower()

        # Check for common validation messages about invalid type
        # PrimaryKeyRelatedField might return "incorrect type" or "invalid"
        self.assertTrue(
            "number" in error_message
            or "decimal" in error_message
            or "invalid" in error_message
            or "incorrect" in error_message
            or "type" in error_message
        )

    def test_create_income_note_too_long(self):
        """Test that creating an income with a note that is too long
        fails."""

        income_data = {
            "category_id": self.category.id,
            "amount": "50.00",
            "date": "2024-01-15",
            "note": ("x" * 251),
        }

        response = self.client.post("/income/", income_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("note", response.data)

        error_message = str(response.data["note"][0]).lower()

        self.assertTrue(
            "length" in error_message
            or "characters" in error_message
            or "250" in error_message
        )


class BudgetValidationTest(TestCase):

    def setUp(self):
        """Set up test data for validation tests."""
        # Create a user
        self.user1 = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Create a category
        self.category = Category.objects.create(
            name="Groceries", category_type=Category.CategoryType.EXPENSE
        )
        # Create an API client
        self.client = APIClient()
        # Authenticate the client
        self.client.force_authenticate(user=self.user1)

    def test_create_budget_end_date_before_start_date(self):
        """Test that creating a budget with an end date before start
        date."""

        budget_data = {
            "category_id": self.category.id,
            "start_date": "2024-02-01",
            "end_date": "2024-01-31",
            "amount": "500.00",
            "note": "Test budget",
        }

        response = self.client.post("/budgets/", budget_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # The error might be on end_date field or as a non-field error
        has_date_error = (
            "end_date" in response.data
            or "start_date" in response.data
            or "non_field_errors" in response.data
        )
        self.assertTrue(has_date_error)

        # Get the error message from whichever field has it
        if "end_date" in response.data:
            error_message = str(response.data["end_date"][0]).lower()
        elif "start_date" in response.data:
            error_message = str(response.data["start_date"][0]).lower()
        elif "non_field_errors" in response.data:
            error_message = str(response.data["non_field_errors"][0]).lower()
        else:
            error_message = ""

        # Check for date validation messages
        self.assertTrue(
            "date" in error_message
            or "before" in error_message
            or "after" in error_message
            or "invalid" in error_message
            or "greater" in error_message
            or "less" in error_message
        )

    def test_create_budget_missing_amount(self):
        """Test that creating a budget without amount fails."""
        # Create budget data without 'amount' field
        budget_data = {
            "category_id": self.category.id,
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "note": "Test budget",
        }

        response = self.client.post("/budgets/", budget_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'amount' is required
        self.assertIn("amount", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["amount"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_budget_missing_start_date(self):
        """Test that creating a budget without start_date fails."""
        # Create budget data without 'start_date' field
        budget_data = {
            "category_id": self.category.id,
            "end_date": "2024-01-31",
            "amount": "500.00",
            "note": "Test budget",
        }

        response = self.client.post("/budgets/", budget_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'start_date' is required
        self.assertIn("start_date", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["start_date"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_budget_missing_end_date(self):
        """Test that creating a budget without end_date fails."""
        # Create budget data without 'end_date' field
        budget_data = {
            "category_id": self.category.id,
            "start_date": "2024-01-01",
            "amount": "500.00",
            "note": "Test budget",
        }

        response = self.client.post("/budgets/", budget_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'end_date' is required
        self.assertIn("end_date", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["end_date"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_budget_negative_amount(self):
        """Test that creating a budget with negative amount fails."""
        # Create budget data with negative amount
        budget_data = {
            "category_id": self.category.id,
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "amount": "-10.00",
            "note": "Test budget",
        }

        response = self.client.post("/budgets/", budget_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'amount' is invalid
        self.assertIn("amount", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["amount"][0]).lower()
        # Check for common validation messages about negative values
        self.assertTrue(
            "greater" in error_message
            or "positive" in error_message
            or "invalid" in error_message
        )

    def test_create_budget_no_category_id(self):
        """Test that creating a budget with no category ID fails."""
        # Create budget data without 'category_id' field
        budget_data = {
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "amount": "500.00",
            "note": "Test budget",
        }

        response = self.client.post("/budgets/", budget_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'category_id' is required
        # Note: The serializer uses 'category_id' for write operations
        self.assertIn("category_id", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["category_id"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_budget_invalid_amount_type(self):
        """Test that creating a budget with invalid amount type fails."""
        # Create budget data with amount as string instead of number
        budget_data = {
            "category_id": self.category.id,
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "amount": "not a number",
            "note": "Test budget",
        }

        response = self.client.post("/budgets/", budget_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'amount' is invalid
        self.assertIn("amount", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["amount"][0]).lower()
        # Check for common validation messages about invalid number format
        self.assertTrue(
            "number" in error_message
            or "decimal" in error_message
            or "invalid" in error_message
        )

    def test_create_budget_invalid_start_date_format(self):
        """Test that creating a budget with invalid start_date format
        fails."""

        budget_data = {
            "category_id": self.category.id,
            "start_date": "not-a-date",
            "end_date": "2024-01-31",
            "amount": "500.00",
            "note": "Test budget",
        }

        response = self.client.post("/budgets/", budget_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("start_date", response.data)

        error_message = str(response.data["start_date"][0]).lower()

        self.assertTrue("date" in error_message or "invalid" in error_message)

    def test_create_budget_invalid_end_date_format(self):
        """Test that creating a budget with invalid end_date format
        fails."""

        budget_data = {
            "category_id": self.category.id,
            "start_date": "2024-01-01",
            "end_date": "not-a-date",
            "amount": "500.00",
            "note": "Test budget",
        }

        response = self.client.post("/budgets/", budget_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("end_date", response.data)

        error_message = str(response.data["end_date"][0]).lower()

        self.assertTrue("date" in error_message or "invalid" in error_message)

    def test_create_budget_invalid_category_id_type(self):
        """Test that creating a budget with invalid category ID fails."""

        budget_data = {
            "category_id": "not a number",
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "amount": "500.00",
            "note": "Test budget",
        }

        response = self.client.post("/budgets/", budget_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("category_id", response.data)

        error_message = str(response.data["category_id"][0]).lower()

        # Check for common validation messages about invalid type
        # PrimaryKeyRelatedField might return "incorrect type" or "invalid"
        self.assertTrue(
            "number" in error_message
            or "decimal" in error_message
            or "invalid" in error_message
            or "incorrect" in error_message
            or "type" in error_message
        )

    def test_create_budget_note_too_long(self):
        """Test that creating a budget with a note that is too long
        fails."""

        budget_data = {
            "category_id": self.category.id,
            "start_date": "2024-01-01",
            "end_date": "2024-01-31",
            "amount": "500.00",
            "note": ("x" * 251),
        }

        response = self.client.post("/budgets/", budget_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("note", response.data)

        error_message = str(response.data["note"][0]).lower()

        self.assertTrue(
            "length" in error_message
            or "characters" in error_message
            or "250" in error_message
        )


class GoalValidationTest(TestCase):

    def setUp(self):
        """Set up test data for validation tests."""
        # Create a user
        self.user1 = User.objects.create_user(
            username="testuser", password="testpass123"
        )
        # Create an API client
        self.client = APIClient()
        # Authenticate the client
        self.client.force_authenticate(user=self.user1)

    def test_create_goal_missing_name(self):
        """Test that creating a goal without name fails."""
        # Create goal data without 'name' field
        goal_data = {
            "target": "1000.00",
            "deadline": "2024-12-31",
            "status": "Not Started",
            "note": "Test goal",
        }

        response = self.client.post("/goals/", goal_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'name' is required
        self.assertIn("name", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["name"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_goal_missing_target(self):
        """Test that creating a goal without target fails."""
        # Create goal data without 'target' field
        goal_data = {
            "name": "Save for vacation",
            "deadline": "2024-12-31",
            "status": "Not Started",
            "note": "Test goal",
        }

        response = self.client.post("/goals/", goal_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'target' is required
        self.assertIn("target", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["target"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_goal_missing_deadline(self):
        """Test that creating a goal without deadline fails."""
        # Create goal data without 'deadline' field
        goal_data = {
            "name": "Save for vacation",
            "target": "1000.00",
            "status": "Not Started",
            "note": "Test goal",
        }

        response = self.client.post("/goals/", goal_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'deadline' is required
        self.assertIn("deadline", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["deadline"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_goal_missing_status(self):
        """Test that creating a goal without status fails."""
        # Create goal data without 'status' field
        goal_data = {
            "name": "Save for vacation",
            "target": "1000.00",
            "deadline": "2024-12-31",
            "note": "Test goal",
        }

        response = self.client.post("/goals/", goal_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'status' is required
        self.assertIn("status", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["status"][0]).lower()
        self.assertIn("required", error_message)

    def test_create_goal_negative_target(self):
        """Test that creating a goal with negative target fails."""
        # Create goal data with negative target
        goal_data = {
            "name": "Save for vacation",
            "target": "-100.00",
            "deadline": "2024-12-31",
            "status": "Not Started",
            "note": "Test goal",
        }

        response = self.client.post("/goals/", goal_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'target' is invalid
        self.assertIn("target", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["target"][0]).lower()
        # Check for common validation messages about negative values
        self.assertTrue(
            "greater" in error_message
            or "positive" in error_message
            or "invalid" in error_message
        )

    def test_create_goal_invalid_target_type(self):
        """Test that creating a goal with invalid target type fails."""
        # Create goal data with target as string instead of number
        goal_data = {
            "name": "Save for vacation",
            "target": "not a number",
            "deadline": "2024-12-31",
            "status": "Not Started",
            "note": "Test goal",
        }

        response = self.client.post("/goals/", goal_data, format="json")

        # Should return 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # Check that error message mentions 'target' is invalid
        self.assertIn("target", response.data)
        # The error is usually a list, so check the first error message
        error_message = str(response.data["target"][0]).lower()
        # Check for common validation messages about invalid number format
        self.assertTrue(
            "number" in error_message
            or "decimal" in error_message
            or "invalid" in error_message
        )

    def test_create_goal_invalid_deadline_format(self):
        """Test that creating a goal with invalid deadline format fails."""

        goal_data = {
            "name": "Save for vacation",
            "target": "1000.00",
            "deadline": "not-a-date",
            "status": "Not Started",
            "note": "Test goal",
        }

        response = self.client.post("/goals/", goal_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("deadline", response.data)

        error_message = str(response.data["deadline"][0]).lower()

        self.assertTrue("date" in error_message or "invalid" in error_message)

    def test_create_goal_name_too_long(self):
        """Test that creating a goal with a name that is too long fails."""

        goal_data = {
            "name": ("x" * 151),  # Exceeds max_length of 150
            "target": "1000.00",
            "deadline": "2024-12-31",
            "status": "Not Started",
            "note": "Test goal",
        }

        response = self.client.post("/goals/", goal_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("name", response.data)

        error_message = str(response.data["name"][0]).lower()

        self.assertTrue(
            "length" in error_message
            or "characters" in error_message
            or "150" in error_message
        )

    def test_create_goal_note_too_long(self):
        """Test that creating a goal with a note that is too long
        fails."""

        goal_data = {
            "name": "Save for vacation",
            "target": "1000.00",
            "deadline": "2024-12-31",
            "status": "Not Started",
            "note": ("x" * 251),
        }

        response = self.client.post("/goals/", goal_data, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.assertIn("note", response.data)

        error_message = str(response.data["note"][0]).lower()

        self.assertTrue(
            "length" in error_message
            or "characters" in error_message
            or "250" in error_message
        )
