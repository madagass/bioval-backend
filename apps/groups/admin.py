from django.contrib import admin
from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ["nom", "data_creation", "member_count"]
    search_fields = ["nom"]
    readonly_fields = ["id", "data_creation"]
    filter_horizontal = ["membres"]

    def member_count(self, obj):
        return obj.membres.count()
    member_count.short_description = "Members"