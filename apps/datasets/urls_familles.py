from django.urls import path
from .views import FamilleListCreateView, FamilleDetailView

urlpatterns = [
    path("", FamilleListCreateView.as_view(), name="famille-list"),
    path("<uuid:pk>/", FamilleDetailView.as_view(), name="famille-detail"),
]