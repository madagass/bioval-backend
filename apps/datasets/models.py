from django.db import models
import uuid


class Famille(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")

    class Meta:
        db_table = "familles"
        ordering = ["nom"]

    def __str__(self):
        return self.nom


class Dataset(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("validated", "Validated"),
        ("rejected", "Rejected"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    date_import = models.DateTimeField(auto_now_add=True)
    importe_par = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="datasets",
    )
    taille = models.BigIntegerField(help_text="File size in bytes")
    format = models.CharField(max_length=20)
    famille = models.ForeignKey(
        Famille,
        on_delete=models.SET_NULL,
        null=True,
        related_name="datasets",
    )
    file = models.FileField(upload_to="datasets/")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    class Meta:
        db_table = "datasets"
        ordering = ["-date_import"]

    def __str__(self):
        return self.nom