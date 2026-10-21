from rest_framework import serializers as se

from core.models import ProductsOrders, Coupom, OrderStatus, OrderCategories, ProductTypes
from core.serializers import CreateProductOrderSerializer, QueryProductOrderSerializer

STATUS = [(status.value, status.name) for status in OrderStatus]
CATEGORIES = [(category.value, category.name) for category in OrderCategories]
TYPES = [(type.value, type.name) for type in ProductTypes]

class CreateOrderSerializer(se.Serializer):
    id = se.IntegerField(read_only=True)
    datetime = se.DateTimeField(read_only=True)
    quantity = se.IntegerField()
    total_value = se.DecimalField()
    category = se.ChoiceField(CATEGORIES)
    status = se.ChoiceField(STATUS)
    cover = se.IntegerField(allow_null=True)
    notes = se.CharField(max_length=255, allow_null=True)

    client_id = se.IntegerField()
    employee_id = se.IntegerField()

    # Crio uma referência ao modelo intermediário para salvar os produtos,
    # assim tenho como enviar um POST body como campo do outro. 
    products = CreateProductOrderSerializer(many=True)

    coupoms = se.PrimaryKeyRelatedField(queryset=Coupom.objects.all(), many=True, allow_null=True)



class QueryOrderSerializer(se.Serializer):
    id = se.IntegerField(allow_null=True)
    minimum_date = se.DateTimeField(allow_null=True)
    maximum_date = se.DateTimeField(allow_null=True)
    minimum_quantity = se.IntegerField(allow_null=True)
    maximum_quantity = se.IntegerField(allow_null=True)
    minimum_value = se.DecimalField(allow_null=True)
    minimum_value = se.DecimalField(allow_null=True)
    category = se.ChoiceField(choices=CATEGORIES,allow_null=True)
    status = se.ChoiceField(choices=STATUS, allow_null=True)
    notes = se.CharField(max_length=255, allow_null=True)

    client_id = se.IntegerField(allow_null=True)
    employee_id = se.IntegerField(allow_null=True)

    products = QueryProductOrderSerializer(many=True, allow_null=True)

    coupoms = se.PrimaryKeyRelatedField(queryset=Coupom.objects.all(), many=True, allow_null=True)



class UpdateOrderStatusSerializer(se.Serializer):
    id = se.IntegerField()
    status = se.ChoiceField(STATUS)