"""Django ORM models for transactions: Category, Expense, Income,
Budget, and Goal.

Mirrors the CLI/SQLite schema to ease migration.
"""

from django.db import models


# ----------------------Category Models----------------------


class Category(models.Model):
    """Transaction category with name and type of category (expense
    or income)."""

    class CategoryType(models.TextChoices):
        """Type of category (expense or income)."""

        EXPENSE = "EXPENSE", "Expense"
        INCOME = "INCOME", "Income"

    name = models.CharField(max_length=100)
    category_type = models.CharField(
        max_length=7,
        choices=CategoryType.choices,
        default=CategoryType.EXPENSE,
    )

    def __str__(self):
        return f"{self.name}"

    class Meta:
        """Meta class for the Category model."""

        constraints = [
            models.UniqueConstraint(
                fields=["name", "category_type"],
                name="unique_category_name_per_type",
            )
        ]


# ----------------------Expense Model----------------------


class Expense(models.Model):
    """Expense record with amount, date, note and category ID."""

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="expenses"
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    note = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.category.name} - ${self.amount}"


# ----------------------Income Model----------------------


class Income(models.Model):
    """Income record with amount, date, note and category ID."""

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    note = models.CharField(max_length=250, blank=True, null=True)

    def __str__(self):
        return f"{self.date} - {self.category.name} - ${self.amount}"


# ----------------------Budget Model----------------------


class Budget(models.Model):
    """Budget for a category with start/end dates, amount and
    progress."""

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    note = models.CharField(max_length=250, blank=True, null=True)
    dates = models.CharField(
        max_length=255,
        blank=True,
        help_text=(
            "Comma-separated list of YYYY-MM-DD checkpoints " "(start,end,...)"
        ),
    )
    remaining_amount = models.DecimalField(max_digits=10, decimal_places=2)
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        help_text="Store as a whole number (e.g., 82.50 for 82.5%)",
    )

    def __str__(self):
        return (
            f"{self.category.name} budget "
            f"{self.start_date} to {self.end_date} (${self.amount})"
        )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["category", "start_date", "end_date"],
                name="unique_budget_date_range_per_category",
            )
        ]


# ----------------------Goal Model----------------------


class Goal(models.Model):
    """Financial goal with target, deadline and status."""

    name = models.CharField(max_length=150)
    target = models.DecimalField(max_digits=10, decimal_places=2)
    deadline = models.DateField()
    note = models.CharField(max_length=250, blank=True, null=True)
    status = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.name} - ${self.target} ({self.status})"
