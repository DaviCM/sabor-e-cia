from django.db import models

from src.core.models.core_enums import Units

class Ingredients(models.Model):
    UNITS = [(unit.name, unit.value) for unit in Units]

    id = models.PositiveIntegerField(primary_key=True)
    description = models.CharField(max_length=120, null=False)
    quantity = models.PositiveIntegerField(default=0, null=False)
    unit = models.CharField(max_length=50, choices=UNITS, null=False)
    provider = models.CharField(max_length=120, null=False)