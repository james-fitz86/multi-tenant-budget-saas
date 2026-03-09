from django.contrib import admin
from .models import Organisation, OrganisationMembership, Department
# Register your models here.

@admin.register(Organisation)
class OrganisationAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_by", "created_at", "is_active")
    search_fields = ("name", "slug")


@admin.register(OrganisationMembership)
class OrganisationMembershipAdmin(admin.ModelAdmin):
    list_display = ("user", "organisation", "role", "joined_at")
    list_filter = ("role", "organisation")

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "organisation", "manager", "created_at")
    list_filter = ("organisation",)
    search_fields = ("name",)
