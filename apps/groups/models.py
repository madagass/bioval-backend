from django.db import models
import uuid


class Group(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nom = models.CharField(max_length=255)
    membres = models.ManyToManyField(
        "users.User",
        related_name="groups",
        blank=True,
    )
    data_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "groups"
        ordering = ["-data_creation"]

    def __str__(self):
        return self.nom