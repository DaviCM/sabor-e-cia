from django.db import models

from users.models.user_enums import Roles

class Employee(models.Model):
    # Inverti valor e nome em todas as tuplas, para salvar em lowercase
    ROLES = [(role.value, role.name) for role in Roles]

    cpf = models.CharField(max_length=50, null=False)
    role = models.CharField(max_length=50, choices=ROLES, null=False)

    user = models.OneToOneField(to="users.User", on_delete=models.CASCADE, null=False)