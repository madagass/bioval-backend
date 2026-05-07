from rest_framework import serializers
from .models import Group
from apps.users.serializers import UserSerializer


class GroupSerializer(serializers.ModelSerializer):
    membres = UserSerializer(many=True, read_only=True)
    abonnement = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ["id", "nom", "membres", "abonnement", "data_creation"]
        read_only_fields = ["id", "data_creation"]

    def get_abonnement(self, obj):
        from apps.subscriptions.serializers import SubscriptionSerializer
        sub = obj.subscriptions.filter(
            statut="active"
        ).first() or obj.subscriptions.first()
        if sub:
            return SubscriptionSerializer(sub).data
        return None


class GroupCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ["nom"]


class GroupMemberSerializer(serializers.Serializer):
    user_id = serializers.UUIDField()