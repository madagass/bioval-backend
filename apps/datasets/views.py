from rest_framework import generics, status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from .models import Dataset, Famille
from .serializers import (
    DatasetSerializer, DatasetUploadSerializer,
    DatasetStatusSerializer, FamilleSerializer,
)
from apps.users.permissions import IsAdminGlobal, IsAdminMetier


class DatasetListCreateView(generics.ListCreateAPIView):
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        user = self.request.user
        if user.role in ["admin_global", "admin_metier"]:
            return Dataset.objects.all()
        if user.role == "admin_externe":
            return Dataset.objects.filter(status="validated")
        if user.role == "user_interne":
            return Dataset.objects.filter(status="validated")
        if user.role == "user_externe":
            return Dataset.objects.filter(
                status="validated",
                importe_par__organisation=user.organisation,
            )
        return Dataset.objects.none()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return DatasetUploadSerializer
        return DatasetSerializer


class DatasetDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Dataset.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return DatasetStatusSerializer
        return DatasetSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminGlobal()]
        if self.request.method in ["PATCH", "PUT"]:
            return [IsAdminMetier()]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.file.delete(save=False)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# ── Famille Views ─────────────────────────────────────────────────────────────

class FamilleListCreateView(generics.ListCreateAPIView):
    queryset = Famille.objects.all()
    serializer_class = FamilleSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminGlobal()]
        return super().get_permissions()


class FamilleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Famille.objects.all()
    serializer_class = FamilleSerializer
    permission_classes = [IsAdminGlobal]