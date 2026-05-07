from django.urls import path
from .views import UserListView, UserDetailView, UserSyncView, MeView

urlpatterns = [
    path("", UserListView.as_view(), name="user-list"),
    path("me/", MeView.as_view(), name="user-me"),
    path("sync/", UserSyncView.as_view(), name="user-sync"),
    path("<uuid:pk>/", UserDetailView.as_view(), name="user-detail"),
]