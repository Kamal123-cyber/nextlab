from django.db import models
from django.conf import settings
import uuid

class App(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique identifier
    name = models.CharField(max_length=255)
    package_name = models.CharField(max_length=255, unique=True)  # Unique package ID
    play_store_link = models.URLField(null=True, blank=True)  # Play Store URL
    points = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    uid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)  # Unique identifier
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    app = models.ForeignKey(
        App,
        on_delete=models.CASCADE,
        related_name="tasks"
    )
    screenshot = models.ImageField(upload_to="screenshots/", null=True, blank=True)
    points_earned = models.PositiveIntegerField(default=0, null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username} - {self.app.name} ({self.status})"

    def save(self, *args, **kwargs):
        # Check if status is changing to approved
        if self.pk:
            original = Task.objects.get(uid=self.uid)
            if original.status != "approved" and self.status == "approved":
                self.user.points += self.points_earned
                self.user.save()

        super().save(*args, **kwargs)
