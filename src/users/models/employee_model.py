from django.db import models

from users.models.user_enums import Roles

class Employee(models.Model):
    ROLES = [(role.name, role.value) for role in Roles]

    cpf = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=50, choices=ROLES, null=False)

    user = models.OneToOneField(to="users.User", on_delete=models.CASCADE)