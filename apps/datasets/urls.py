from django.urls import path
from .views import DatasetListCreateView, DatasetDetailView

urlpatterns = [
    path("", DatasetListCreateView.as_view(), name="dataset-list"),
    path("<uuid:pk>/", DatasetDetailView.as_view(), name="dataset-detail"),
]