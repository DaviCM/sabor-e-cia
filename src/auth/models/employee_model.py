from django.db import models

from auth.models.auth_enums import Roles

class Employees(models.Model):
    ROLES = [(role.name, role.value) for role in Roles]

    id = models.PositiveIntegerField(primary_key=True)
    login = models.CharField(max_length=120, null=False)
    password = models.CharField(max_length=255, null=False)
    cpf = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=50, choices=ROLES, null=False)