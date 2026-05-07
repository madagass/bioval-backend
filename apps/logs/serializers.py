from rest_framework import serializers
from .models import Log


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ["id", "user_id", "user_email", "action", "created_at"]
        read_only_fields = ["id", "created_at"]