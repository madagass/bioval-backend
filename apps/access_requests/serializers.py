from rest_framework import serializers
from .models import AccessRequest


class AccessRequestSerializer(serializers.ModelSerializer):
    reviewed_by = serializers.SerializerMethodField()

    class Meta:
        model = AccessRequest
        fields = [
            "id", "email", "company_name", "status",
            "reviewed_by", "reviewed_at", "created_at",
        ]
        read_only_fields = ["id", "reviewed_by", "reviewed_at", "created_at"]

    def get_reviewed_by(self, obj):
        if obj.reviewed_by:
            return obj.reviewed_by.email
        return None


class AccessRequestCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRequest
        fields = ["email", "company_name"]

    def validate_email(self, value):
        if AccessRequest.objects.filter(email=value, status="pending").exists():
            raise serializers.ValidationError(
                "A pending request already exists for this email."
            )
        return value


class AccessRequestStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccessRequest
        fields = ["status"]