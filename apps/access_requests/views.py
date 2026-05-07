from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from .models import AccessRequest
from .serializers import (
    AccessRequestSerializer,
    AccessRequestCreateSerializer,
    AccessRequestStatusSerializer,
)
from apps.users.permissions import IsAdminMetier


class AccessRequestListView(generics.ListAPIView):
    serializer_class = AccessRequestSerializer
    permission_classes = [IsAdminMetier]

    def get_queryset(self):
        qs = AccessRequest.objects.all()
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs


class AccessRequestListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        qs = AccessRequest.objects.all()
        status_filter = self.request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs

    def get_serializer_class(self):
        if self.request.method == "POST":
            return AccessRequestCreateSerializer
        return AccessRequestSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [AllowAny()]
        return [IsAdminMetier()]

    def get_authenticators(self):
        if self.request.method == "POST":
            return []
        return super().get_authenticators()


class AccessRequestDetailView(generics.RetrieveUpdateAPIView):
    queryset = AccessRequest.objects.all()
    permission_classes = [IsAdminMetier]

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return AccessRequestStatusSerializer
        return AccessRequestSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        new_status = serializer.validated_data.get("status")
        if new_status in ["accepted", "rejected"]:
            instance.reviewed_by = request.user
            instance.reviewed_at = timezone.now()

        instance.status = new_status
        instance.save()

        return Response(AccessRequestSerializer(instance).data)