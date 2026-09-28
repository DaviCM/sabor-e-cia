from django.db import models

from core.models.core_enums import ProductTypes

class ProductsOrders(models.Model):
    TYPES = [(type.name, type.value) for type in ProductTypes]

    product_type = models.CharField(max_length=120, choices=TYPES, null=False)
    is_combo = models.BooleanField(default=False, null=False)

    product = models.ForeignKey(to="core.Product", on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(to="core.Order", on_delete=models.CASCADE, null=True)