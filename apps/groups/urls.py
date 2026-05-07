from django.urls import path
from .views import GroupListCreateView, GroupDetailView, GroupMemberAddView, GroupMemberRemoveView

urlpatterns = [
    path("", GroupListCreateView.as_view(), name="group-list"),
    path("<uuid:pk>/", GroupDetailView.as_view(), name="group-detail"),
    path("<uuid:pk>/members/", GroupMemberAddView.as_view(), name="group-member-add"),
    path("<uuid:pk>/members/<uuid:user_id>/", GroupMemberRemoveView.as_view(), name="group-member-remove"),
]