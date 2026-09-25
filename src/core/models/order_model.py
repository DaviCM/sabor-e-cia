from django.db import models
from django.db.models.functions import Now

from src.users.models.client_model import Client
from src.users.models.employee_model import Employee
from src.core.models.core_enums import OrderStatus, OrderCategories
from src.core.models.product_model import Product
from src.core.models.coupom_model import Coupom
from src.core.models.products_orders_model import ProductsOrders

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

    client_id = models.ForeignKey(to=Client, on_delete=models.CASCADE, null=True)
    employee_id = models.ForeignKey(to=Employee, on_delete=models.CASCADE, null=True)

    products = models.ManyToManyField(to=Product, through=ProductsOrders, null=True)
    coupoms = models.ManyToManyField(to=Coupom, null=True)
