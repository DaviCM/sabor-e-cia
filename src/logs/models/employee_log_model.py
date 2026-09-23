from django.db import models
from django.db.models.functions import Now

from src.auth.models.employee_model import Employees
from src.auth.models.auth_enums import Roles

class EmployeeLogs(models.Model):
    ROLES = [(role.name, role.value) for role in Roles]

    id = models.PositiveIntegerField(primary_key=True)
    datetime = models.DateTimeField(db_default=Now(), null=False)
    role = models.CharField(max_length=50, choices=ROLES, null=False)
    employee_id = models.ForeignKey(to=Employees, on_delete=models.CASCADE, null=True)