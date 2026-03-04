from django.contrib import admin
from .models import Organisation, OrganisationMembership
# Register your models here.

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_by", "created_at", "is_active")
    search_fields = ("name", "slug")


@admin.register(OrganisationMembership)
class OrganisationMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "organisation", "role", "joined_at")
    list_filter = ("role", "organisation")
