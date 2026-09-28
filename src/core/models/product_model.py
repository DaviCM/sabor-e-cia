from django.db import models

from core.models.core_enums import ProductCategories

class Product(models.Model):
    CATEGORIES = [(category.name, category.value) for category in ProductCategories]

    description = models.CharField(max_length=120, null=False)
    category = models.CharField(max_length=50, choices=CATEGORIES, null=False)
    value = models.DecimalField(null=False)
    
    coupoms = models.ManyToManyField(to="core.Coupom", blank=True)