from rest_framework import serializers
from .models import Dataset, Famille


class FamilleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Famille
        fields = ["id", "nom", "description"]


class DatasetSerializer(serializers.ModelSerializer):
    famille = serializers.SerializerMethodField()
    importe_par = serializers.SerializerMethodField()

    class Meta:
        model = Dataset
        fields = [
            "id", "nom", "date_import", "importe_par",
            "taille", "format", "famille", "status",
        ]

    def get_famille(self, obj):
        return obj.famille.nom if obj.famille else None

    def get_importe_par(self, obj):
        if obj.importe_par:
            return obj.importe_par.email
        return None


class DatasetUploadSerializer(serializers.ModelSerializer):
    famille_id = serializers.UUIDField(write_only=True)
    file = serializers.FileField()

    class Meta:
        model = Dataset
        fields = ["nom", "taille", "format", "famille_id", "file"]

    def create(self, validated_data):
        famille_id = validated_data.pop("famille_id")
        famille = Famille.objects.get(id=famille_id)
        user = self.context["request"].user
        return Dataset.objects.create(
            famille=famille,
            importe_par=user,
            **validated_data,
        )


class DatasetStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataset
        fields = ["status"]