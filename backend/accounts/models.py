from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

# Create your models here.
class User(AbstractUser):
    """
    Platform-level authentication identity.
    """
    username = None

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150, blank=True)

    email_verified = models.BooleanField(default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email
