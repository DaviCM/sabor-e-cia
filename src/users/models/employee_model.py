from django.db import models

from src.users.models.auth_enums import Roles
from src.users.models.generic_user_model import User

class Employee(models.Model):
    ROLES = [(role.name, role.value) for role in Roles]

    cpf = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=50, choices=ROLES, null=False)

    user = models.OneToOneField(to=User, on_delete=models.CASCADE)