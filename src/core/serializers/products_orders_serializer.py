from rest_framework import serializers as se

from core.models import Product, Order, ProductTypes

TYPES = [(type.value, type.name) for type in ProductTypes]

class CreateProductOrderSerializer(se.Serializer):
    is_combo = se.BooleanField(default=False)
    product_type = se.ChoiceField(TYPES)

    product = se.PrimaryKeyRelatedField(queryset=Product.objects.all())

    # Como os produtos estão sendo associados especificamente ao pedido
    # que está sendo criado, não é necessário incluir o id do pedido no
    # serializador. Isso seria impossível, pois o pedido ainda não existe
    # no banco.



class QueryProductOrderSerializer(se.Serializer):
    is_combo = se.BooleanField(allow_null=True)
    product_type = se.ChoiceField(TYPES, allow_null=True)

    product = se.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, allow_null=True)
    order = se.PrimaryKeyRelatedField(queryset=Order.objects.all(), many=True, allow_null=True)