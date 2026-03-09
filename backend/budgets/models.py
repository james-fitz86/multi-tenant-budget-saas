from django.db import models
from config.base_models import TenantScopedModel

# Create your models here.

class BudgetPeriod(models.TextChoices):
    """
    Defines the supported budget period types
    for orgabisation-level budgets.
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
