from django.db import models
from django.db.models.functions import Now

from users.models.user_enums import Roles

class EmployeeLog(models.Model):
    ROLES = [(role.name, role.value) for role in Roles]

    datetime = models.DateTimeField(db_default=Now(), null=False)
    role = models.CharField(max_length=50, choices=ROLES, null=False)
    employee = models.ForeignKey(to="users.Employee", on_delete=models.CASCADE, null=True)