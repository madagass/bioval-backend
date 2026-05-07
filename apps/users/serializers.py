from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id", "clerk_id", "nom", "prenom", "email",
            "role", "is_active", "free_access", "organisation", "created_at",
        ]
        read_only_fields = ["id", "clerk_id", "created_at"]


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["nom", "prenom", "role", "is_active", "free_access", "organisation"]


class UserSyncSerializer(serializers.Serializer):
    clerk_id = serializers.CharField()
    email = serializers.EmailField()
    nom = serializers.CharField(required=False, default="")
    prenom = serializers.CharField(required=False, default="")