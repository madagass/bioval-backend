from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer, UserUpdateSerializer, UserSyncSerializer
from apps.users.permissions import IsAdminGlobal, IsAdminGlobalOrMetier


class UserSyncView(APIView):
    """Called after Clerk sign-in to create/sync user in our DB."""
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSyncSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user, created = User.objects.get_or_create(
            clerk_id=data["clerk_id"],
            defaults={
                "email": data["email"],
                "nom": data.get("nom", ""),
                "prenom": data.get("prenom", ""),
            },
        )

        if not created:
            user.email = data["email"]
            user.save(update_fields=["email"])

        return Response(UserSerializer(user).data, status=status.HTTP_200_OK)


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAdminGlobalOrMetier]

    def get_queryset(self):
        return User.objects.all()


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdminGlobal]

    def get_serializer_class(self):
        if self.request.method in ["PATCH", "PUT"]:
            return UserUpdateSerializer
        return UserSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class MeView(APIView):
    """Returns the currently authenticated user."""
    def get(self, request):
        return Response(UserSerializer(request.user).data)