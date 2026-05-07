from django.contrib import admin
from .models import AccessRequest


@admin.register(AccessRequest)
class AccessRequestAdmin(admin.ModelAdmin):
    list_display = ["email", "company_name", "status", "reviewed_by", "created_at"]
    list_filter = ["status"]
    search_fields = ["email", "company_name"]
    readonly_fields = ["id", "created_at", "reviewed_at"]