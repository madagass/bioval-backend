from django.contrib import admin
from .models import Dataset, Famille


@admin.register(Famille)
class FamilleAdmin(admin.ModelAdmin):
    list_display = ["nom", "description"]
    search_fields = ["nom"]


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ["nom", "format", "taille", "status", "importe_par", "date_import"]
    list_filter = ["status", "format", "famille"]
    search_fields = ["nom"]
    readonly_fields = ["id", "date_import"]