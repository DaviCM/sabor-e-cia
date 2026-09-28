from django.db import models
from django.db.models.functions import Now

class DeliveryLog(models.Model):
    datetime = models.DateTimeField(db_default=Now(), null=False)
    delivery_fee = models.DecimalField(null=False)

    address = models.ForeignKey(to="users.ClientAddress", on_delete=models.CASCADE, null=False)
    deliverer = models.ForeignKey(to="users.Employee", on_delete=models.CASCADE, null=False)
    order = models.ForeignKey(to="core.Order", on_delete=models.CASCADE, null=False)