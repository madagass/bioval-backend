from .models import Log


def log_action(user, action: str):
    """Helper to create a log entry from anywhere in the codebase."""
    Log.objects.create(
        user=user,
        user_email=user.email if user else "",
        action=action,
    )