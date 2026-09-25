from django.db import models

from src.users.models.client_model import Client
from src.core.models.order_model import Order

class ClientReview(models.Model):
    score = models.PositiveIntegerField(null=False)
    notes = models.CharField(max_length=255, null=True)

    client_id = models.ForeignKey(to=Client, on_delete=models.CASCADE, null=True)
    order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE, null=True)