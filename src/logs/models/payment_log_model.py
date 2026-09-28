from django.db import models
from django.db.models.functions import Now

from logs.models.log_enums import PaymentMethods

class PaymentLog(models.Model):
    METHODS = [(method.name, method.value) for method in PaymentMethods]

    datetime = models.DateTimeField(db_default=Now(), null=False)
    payment_method = models.CharField(max_length=50, choices=METHODS, null=False)
    value = models.DecimalField(null=False)

    order = models.ForeignKey(to="core.Order", on_delete=models.CASCADE, null=False)