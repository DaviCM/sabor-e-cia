from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    id = models.PositiveIntegerField(primary_key=True)
    email = models.CharField(max_length=120, null=False)
    password = models.CharField(max_length=255, null=False)