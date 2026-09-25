from django.db import models
from django.db.models.functions import Now

from src.users.models.employee_model import Employee
from src.users.models.auth_enums import Roles

class EmployeeLog(models.Model):
    ROLES = [(role.name, role.value) for role in Roles]

    datetime = models.DateTimeField(db_default=Now(), null=False)
    role = models.CharField(max_length=50, choices=ROLES, null=False)
    employee_id = models.ForeignKey(to=Employee, on_delete=models.CASCADE, null=True)