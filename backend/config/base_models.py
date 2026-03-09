from django.db import models
from .querysets import TenantManager

class TenantScopedModel(models.Model):
    """
    Base model for all tenant-scoped entities.

    Ensures every domain object belongs to an Organisation.
    """

    organisation = models.ForeignKey(
        "organisations.Organisation",
        on_delete=models.CASCADE,
        related_name="%(class)ss"
    )

    created_at = models.DateTimeField(auto_now_add=True)

    objects = TenantManager()

    class Meta:
        abstract = True

