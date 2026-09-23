from django.db import models

from src.auth.models.client_model import Clients

class ClientAddresses(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    cep = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=120, null=False)
    number = models.PositiveIntegerField(null=False)

    client_id = models.ForeignKey(to=Clients, on_delete=models.CASCADE, null=True)