from django.db import models

from src.core.models.core_enums import ProductTypes
from src.core.models.product_model import Product
from src.core.models.order_model import Order

class ProductsOrders(models.Model):
    TYPES = [(type.name, type.value) for type in ProductTypes]

    product_type = models.CharField(max_length=120, choices=TYPES, null=False)
    is_combo = models.BooleanField(default=False, null=False)

    product_id = models.ForeignKey(to=Product, on_delete=models.CASCADE, null=True)
    order_id = models.ForeignKey(to=Order, on_delete=models.CASCADE, null=True)