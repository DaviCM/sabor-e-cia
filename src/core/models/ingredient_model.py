from django.db import models

from src.core.models.core_enums import Units

class Ingredient(models.Model):
    UNITS = [(unit.name, unit.value) for unit in Units]

    description = models.CharField(max_length=120, null=False)
    quantity = models.PositiveIntegerField(default=0, null=False)
    unit = models.CharField(max_length=50, choices=UNITS, null=False)
    provider = models.CharField(max_length=120, null=False)