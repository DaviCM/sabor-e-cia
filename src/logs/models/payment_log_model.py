from django.db import models
from django.db.models.functions import Now

from src.core.models.order_model import Orders
from src.logs.models.log_enums import PaymentMethods

class DeliveryLogs(models.Model):
    METHODS = [(method.name, method.value) for method in PaymentMethods]

    id = models.PositiveIntegerField(primary_key=True)
    datetime = models.DateTimeField(db_default=Now(), null=False)
    payment_method = models.CharField(max_length=50, choices=METHODS, null=False)
    value = models.DecimalField(null=False)

    order_id = models.ForeignKey(to=Orders, on_delete=models.CASCADE, null=False)