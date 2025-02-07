from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

class User(AbstractUser):
    email = models.EmailField(unique=True)
    homepage = models.URLField(blank=True, null=True)

    username_validator = RegexValidator(
        regex=r'^[a-zA-Z0-9]+$',
        message="Username can only contain letters and numbers."
    )
    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator]
    )

    def __str__(self):
        return f"{self.username} ({self.email})"
