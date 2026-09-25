from django.db import models
from django.db.models.functions import Now

from src.users.models.employee_model import Employee
from src.users.models.client_address_model import ClientAddress
from src.core.models.order_model import Order

class DeliveryLog(models.Model):
    datetime = models.DateTimeField(db_default=Now(), null=False)
    delivery_fee = models.DecimalField(null=False)

    address_id = models.ForeignKey(to=ClientAddress, on_delete=models.CASCADE, null=False)
    deliverer_id = models.ForeignKey(to=Employee, on_delete=models.CASCADE, null=False)
    order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE, null=False)