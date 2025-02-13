from django.contrib.auth.models import AbstractUser
from django.db import models

class UserAccount(AbstractUser):
    email = models.EmailField(unique=True)
    points = models.IntegerField(default=0)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
