from django.db import models
from django.db.models.functions import Now

from src.auth.models.client_model import Clients
from src.auth.models.employee_model import Employees
from src.core.models.core_enums import OrderStatus, OrderCategories
from src.core.models.product_model import Products
from src.core.models.coupom_model import Coupoms
from src.core.models.products_orders_model import ProductsOrders

class Orders(models.Model):
    STATUS = [(status.name, status.value) for status in OrderStatus]
    CATEGORIES = [(category.name, category.value) for category in OrderCategories]

    id = models.PositiveIntegerField(primary_key=True)
    datetime = models.DateTimeField(db_default=Now(), null=False)
    quantity = models.PositiveIntegerField(null=False)
    total_value = models.DecimalField(null=False)
    category = models.CharField(max_length=50, choices=CATEGORIES, null=False)
    status = models.CharField(max_length=50, choices=STATUS, null=False)
    cover = models.PositiveIntegerField(null=True)
    notes = models.CharField(max_length=255, null=True)

    client_id = models.ForeignKey(to=Clients, on_delete=models.CASCADE, null=True)
    employee_id = models.ForeignKey(to=Employees, on_delete=models.CASCADE, null=True)

    products = models.ManyToManyField(to=Products, through=ProductsOrders, null=True)
    coupoms = models.ManyToManyField(to=Coupoms, null=True)
