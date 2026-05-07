from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ["email", "prenom", "nom", "role", "is_active", "free_access", "created_at"]
    list_filter = ["role", "is_active", "free_access"]
    search_fields = ["email", "nom", "prenom", "clerk_id"]
    readonly_fields = ["id", "clerk_id", "created_at"]