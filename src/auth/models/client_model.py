from django.db import models

class Clients(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    email = models.EmailField(max_length=120, null=False)
    password = models.CharField(max_length=255, null=False)
    name = models.CharField(max_length=255, null=False)
    phone = models.CharField(max_length=50,null=False)

