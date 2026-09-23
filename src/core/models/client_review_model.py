from django.db import models

from src.auth.models.client_model import Clients
from src.core.models.order_model import Orders

class ClientReviews(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    score = models.PositiveIntegerField(null=False)
    notes = models.CharField(max_length=255, null=True)

    client_id = models.ForeignKey(to=Clients, on_delete=models.CASCADE, null=True)
    order_id = models.ForeignKey(to=Orders, on_delete=models.CASCADE, null=True)