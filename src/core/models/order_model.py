from django.db import models
from django.db.models.functions import Now

from core.models.products_orders_model import ProductsOrders
from core.models.core_enums import OrderCategories, OrderStatus


class Order(models.Model):
    STATUS = [(status.name, status.value) for status in OrderStatus]
    CATEGORIES = [(category.name, category.value) for category in OrderCategories]

    datetime = models.DateTimeField(db_default=Now(), null=False)
    quantity = models.PositiveIntegerField(null=False)
    total_value = models.DecimalField(null=False)
    category = models.CharField(max_length=50, choices=CATEGORIES, null=False)
    status = models.CharField(max_length=50, choices=STATUS, null=False)
    cover = models.PositiveIntegerField(null=True)
    notes = models.CharField(max_length=255, null=True)

    client = models.ForeignKey(to="users.Client", on_delete=models.CASCADE, null=True)
    employee = models.ForeignKey(to="users.Employee", on_delete=models.CASCADE, null=True)

    products = models.ManyToManyField(to="core.Product", through=ProductsOrders, blank=True)
    coupoms = models.ManyToManyField(to="core.Coupom", blank=True)
