from django.db import models
import uuid


class Subscription(models.Model):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("inactive", "Inactive"),
        ("expired", "Expired"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="subscriptions",
    )
    date_debut = models.DateTimeField()
    date_fin = models.DateTimeField()
    statut = models.CharField(max_length=20, choices=STATUS_CHOICES, default="inactive")
    stripe_subscription_id = models.CharField(max_length=255, blank=True, default="")
    stripe_customer_id = models.CharField(max_length=255, blank=True, default="")

    class Meta:
        db_table = "subscriptions"
        ordering = ["-date_debut"]

    def __str__(self):
        return f"{self.group.nom} - {self.statut}"