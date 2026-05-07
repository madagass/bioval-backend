from django.db import models
import uuid


class Log(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        related_name="logs",
    )
    user_email = models.EmailField()
    action = models.CharField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "logs"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user_email} - {self.action}"