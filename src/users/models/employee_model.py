from django.db import models

from src.users.models.auth_enums import Roles

class Employee(models.Model):
    ROLES = [(role.name, role.value) for role in Roles]

    email = models.CharField(max_length=120, null=False)
    password = models.CharField(max_length=255, null=False)
    cpf = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=50, choices=ROLES, null=False)