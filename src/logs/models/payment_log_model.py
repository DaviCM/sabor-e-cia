from django.db import models
from django.db.models.functions import Now

from src.core.models.order_model import Order
from src.logs.models.log_enums import PaymentMethods

class DeliveryLog(models.Model):
    METHODS = [(method.name, method.value) for method in PaymentMethods]

    datetime = models.DateTimeField(db_default=Now(), null=False)
    payment_method = models.CharField(max_length=50, choices=METHODS, null=False)
    value = models.DecimalField(null=False)

    order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE, null=False)