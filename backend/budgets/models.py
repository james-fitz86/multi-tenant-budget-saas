from django.db import models
from config.base_models import TenantScopedModel
from django.core.exceptions import ValidationError

# Create your models here.

class BudgetPeriod(models.TextChoices):
    """
    Defines the supported budget period types
    for organisation-level budgets.
    """
    MONTHLY = "MONTHLY", "Monthly"
    QUARTERLY = "QUARTERLY", "Quarterly"
    YEARLY = "YEARLY", "Yearly"

class OrganisationBudget(TenantScopedModel):
    """
    Represents a time-bound financial budget
    allocated to an organisation.

    Tracks total allocation along with committed 
    and actual spend for governance and reporting.
    """
    name = models.CharField(max_length=255)

    period = models.CharField(
        max_length=20,
        choices=BudgetPeriod.choices,
    )
    
    start_date = models.DateField()
    end_date = models.DateField()

    total_budget = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    committed_spend = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    actual_spend = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:
        ordering = ["-start_date"]

    def __str__(self):
        return f"{self.name} ({self.organisation.name})"

class DepartmentBudget(TenantScopedModel):
    """
    Represents the portion of an OrganisationBudget
    allocated to a specific department for a budget period.

    Tracks the department's allocated amount along with
    committed and actual spend for governance and reporting.
    """
    organisation_budget = models.ForeignKey(
        "OrganisationBudget",
        on_delete=models.CASCADE,
        related_name="department_budgets"
    )

    department = models.ForeignKey(
        "organisations.Department",
        on_delete=models.CASCADE,
        related_name="department_budgets"
    )

    allocated_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    committed_spend = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    actual_spend = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    class Meta:
        ordering = ["-allocated_amount"]

        constraints = [
            models.UniqueConstraint(
                fields=["department", "organisation_budget"],
                name="unique_department_budget_per_period"
            )
        ]

        indexes = [
            models.Index(fields=["organisation_budget", "department"])
        ]

    def __str__(self):
        return f"{self.department.name} - {self.organisation_budget.name}"

    def clean(self):
        # Ensure department and budget belong to the same organisation
        if self.department.organisation != self.organisation_budget.organisation:
            raise ValidationError(
                "Department must belong to the same organisation as the budget."
            )

        #Calculate current allocated total for all the other departments
        existing_allocations = (
            DepartmentBudget.objects
            .filter(organisation_budget=self.organisation_budget)
            .exclude(pk=self.pk)
            .aggregate(total=models.Sum("allocated_amount"))["total"] or 0
        )

        if existing_allocations + self.allocated_amount > self.organisation_budget.total_budget:
            raise ValidationError(
                "Department allocations exceed the organisation budget"
            )
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class StatusChoices(models.TextChoices):
    """
    Defines the lifecycle states of a spend request
    within the approval workflow.
    """

    PENDING = "PENDING", "Pending"
    APPROVED = "APPROVED", "Approved"
    REJECTED = "REJECTED", "Rejected"

class SpendRequest(TenantScopedModel):
    """
    Represents a request to spend funds from a department's allocated budget.

    Captures the requested amount, associated department budget,
    current approval status, and review metadata.
    """

    department_budget = models.ForeignKey(
        "DepartmentBudget",
        on_delete=models.CASCADE,
        related_name="spend_requests"
    )

    requested_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="spend_requests_created"
    )

    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0
    )

    description = models.CharField(max_length=255)

    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING
    )

    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="spend_requests_reviewed",
        null=True,
        blank=True
    )

    reviewed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        
        indexes = [
            models.Index(fields=["department_budget", "status"])
        ]

    def __str__(self):
        return f"{self.department_budget.department.name} - €{self.amount} ({self.status})"

    def clean(self):
        # Ensure department and budget belong to the same organisation
        if self.department_budget.organisation != self.organisation:
            raise ValidationError(
                "Department budget must belong to the same organisation as the spend request"
            )

        # Ensure request does not exceed the department's allocated amount
        if self.department_budget.committed_spend + self.amount > self.department_budget.allocated_amount:
            raise ValidationError(
                "Spend request exceeds the department's allocated budget"
            )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
