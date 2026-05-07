from django.contrib import admin
from .models import Log


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ["user_email", "action", "created_at"]
    search_fields = ["user_email", "action"]
    readonly_fields = ["id", "created_at"]
    list_filter = ["created_at"]