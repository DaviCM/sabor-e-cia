from django.db import models

from src.users.models.client_model import Client

class ClientAddress(models.Model):
    cep = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=120, null=False)
    number = models.PositiveIntegerField(null=False)

    client_id = models.ForeignKey(to=Client, on_delete=models.CASCADE, null=True)