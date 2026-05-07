from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Group
from .serializers import GroupSerializer, GroupCreateSerializer, GroupMemberSerializer
from apps.users.permissions import IsAdminGlobal, IsAdminExterne, IsAdminGlobalOrExterne
from apps.users.models import User


class GroupListCreateView(generics.ListCreateAPIView):
    def get_queryset(self):
        user = self.request.user
        if user.role in ["admin_global"]:
            return Group.objects.all()
        if user.role in ["admin_externe", "user_externe"]:
            return Group.objects.filter(membres=user)
        return Group.objects.none()

    def get_serializer_class(self):
        if self.request.method == "POST":
            return GroupCreateSerializer
        return GroupSerializer

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminExterne()]
        return [IsAdminGlobalOrExterne()]

    def perform_create(self, serializer):
        group = serializer.save()
        group.membres.add(self.request.user)


class GroupDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return GroupCreateSerializer
        return GroupSerializer

    def get_permissions(self):
        if self.request.method == "DELETE":
            return [IsAdminGlobalOrExterne()]
        if self.request.method in ["PATCH", "PUT"]:
            return [IsAdminGlobal()]
        return super().get_permissions()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GroupMemberAddView(APIView):
    permission_classes = [IsAdminGlobalOrExterne]

    def post(self, request, pk):
        group = Group.objects.get(pk=pk)
        serializer = GroupMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            user = User.objects.get(id=serializer.validated_data["user_id"])
        except User.DoesNotExist:
            return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

        group.membres.add(user)
        return Response(GroupSerializer(group).data)


class GroupMemberRemoveView(APIView):
    permission_classes = [IsAdminGlobalOrExterne]

    def delete(self, request, pk, user_id):
        try:
            group = Group.objects.get(pk=pk)
            user = User.objects.get(id=user_id)
        except (Group.DoesNotExist, User.DoesNotExist):
            return Response({"detail": "Not found."}, status=status.HTTP_404_NOT_FOUND)

        group.membres.remove(user)
        return Response(status=status.HTTP_204_NO_CONTENT)