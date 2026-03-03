from django.conf import settings
from django.db import models
from django.utils.text import slugify

# Create your models here.
class Organisation(models.Model):
    """
    Core tenant entity.

    Represents an isolated company within the Saas platform.
    All tenant-scoped domain models must reference this model.
    """
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="organisations_created",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class OrganisationRole(models.TextChoices):
    """
    Fixed permission tiers for organisation-scoped authority.

    Internal permission keys must remain stable.
    """
    ADMIN = "ADMIN", "Organisation Admin"
    FINANCE = "FINANCE", "Finance"
    MANAGER = "MANAGER", "Department Manager"
    EMPLOYEE = "EMPLOYEE", "Employee"

class OrganisationMembership(models.Model):
    """
    Bridge Model linking users to organisations.

    Stores organisation-scoped authority (role).
    Enables multi-organisation membership.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="organisation_memberships",
    )

    organisation = models.ForeignKey(
        "Organisation",
        on_delete=models.CASCADE,
        related_name="memberships",
    )

    role = models.CharField(
        max_length=20,
        choices=OrganisationRole.choices,
    )

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "organisation")

    def __str__(self):
        return f"{self.user} - {self.organisation} ({self.role})"
