from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class Persons(AbstractUser):
    userId = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ("username", "password")

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.userId)