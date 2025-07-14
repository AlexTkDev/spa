from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator

# Username can only contain letters and numbers
username_validator = RegexValidator(
    regex=r'^[a-zA-Z0-9]+$',
    message="Username can only contain letters and numbers."
)

class User(AbstractUser):
    """Custom user model with unique email and optional homepage."""
    email = models.EmailField(
        unique=True, blank=False, null=False,
        help_text="Required. Enter a valid email address. Must be unique."
    )
    homepage = models.URLField(blank=True, null=True)

    username = models.CharField(
        max_length=150,
        unique=True,
        validators=[username_validator],
        help_text="Required. 150 characters or fewer. Letters and digits only."
    )

    def __str__(self):
        return f"{self.username} ({self.email})"
