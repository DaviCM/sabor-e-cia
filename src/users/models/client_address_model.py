from django.db import models

class ClientAddress(models.Model):
    cep = models.CharField(max_length=50, null=False)
    description = models.CharField(max_length=120, null=False)
    number = models.PositiveIntegerField(null=False)

    client = models.ForeignKey(to="users.Client", on_delete=models.CASCADE, null=True)