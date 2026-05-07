from django.db import models
import uuid


class User(models.Model):
    ROLE_CHOICES = [
        ("admin_global", "Admin Global"),
        ("admin_metier", "Admin Métier"),
        ("admin_externe", "Admin Externe"),
        ("user_interne", "Utilisateur Interne"),
        ("user_externe", "Utilisateur Externe"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clerk_id = models.CharField(max_length=255, unique=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="user_externe")
    is_active = models.BooleanField(default=True)
    free_access = models.BooleanField(default=False)
    organisation = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "users"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.email})"