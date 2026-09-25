from django.db import models

from src.core.models.core_enums import ProductCategories
from src.core.models.coupom_model import Coupom

class Product(models.Model):
    CATEGORIES = [(category.name, category.value) for category in ProductCategories]

    description = models.CharField(max_length=120, null=False)
    category = models.CharField(max_length=50, choices=CATEGORIES, null=False)
    value = models.DecimalField(null=False)

    coupoms = models.ManyToManyField(to=Coupom, null=True)