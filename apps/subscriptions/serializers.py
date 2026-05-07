from rest_framework import serializers
from .models import Subscription


class SubscriptionSerializer(serializers.ModelSerializer):
    group_id = serializers.UUIDField(source="group.id", read_only=True)

    class Meta:
        model = Subscription
        fields = [
            "id", "group_id", "date_debut", "date_fin",
            "statut", "stripe_subscription_id",
        ]
        read_only_fields = ["id", "group_id", "stripe_subscription_id"]


class SubscriptionStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ["statut"]


class CheckoutSessionSerializer(serializers.Serializer):
    group_id = serializers.UUIDField()