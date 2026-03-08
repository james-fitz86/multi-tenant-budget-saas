from django.db import models

class TenantQuerySet(models.QuerySet):
    def for_organisation(self, organisation):
        return self.filter(organisation=organisation)

class TenantManager(models.Manager):
    def get_queryset(self):
        return TenantQuerySet(self.model, using=self._db)

    def for_organisation(self, organisation):
        return self.get_queryset().for_organisation(organisation)
