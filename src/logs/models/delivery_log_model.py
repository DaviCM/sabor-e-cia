from django.db import models
from django.db.models.functions import Now

from src.auth.models.employee_model import Employees
from src.auth.models.client_address_model import ClientAddresses
from src.core.models.order_model import Orders

class DeliveryLogs(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    datetime = models.DateTimeField(db_default=Now(), null=False)
    delivery_fee = models.DecimalField(null=False)

    address_id = models.ForeignKey(to=ClientAddresses, on_delete=models.CASCADE, null=False)
    deliverer_id = models.ForeignKey(to=Employees, on_delete=models.CASCADE, null=False)
    order_id = models.ForeignKey(to=Orders, on_delete=models.CASCADE, null=False)