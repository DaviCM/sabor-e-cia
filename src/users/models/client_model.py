from django.db import models

from src.users.models.generic_user_model import User

class Clients(models.Model):
    phone = models.CharField(max_length=50,null=False)

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)