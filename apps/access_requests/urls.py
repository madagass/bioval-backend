from django.urls import path
from .views import AccessRequestListCreateView, AccessRequestDetailView

urlpatterns = [
    path("", AccessRequestListCreateView.as_view(), name="request-list"),
    path("<uuid:pk>/", AccessRequestDetailView.as_view(), name="request-detail"),
]