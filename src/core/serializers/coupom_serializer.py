from rest_framework import serializers as se

from core.models import Product

class CreateCoupomSerializer(se.Serializer):
    id = se.IntegerField(read_only=True)
    token = se.CharField(max_length=50)
    multiplier = se.DecimalField()
    created_at = se.DateTimeField(allow_null=True)
    expires_at = se.DateTimeField()

    # DRF fornece esse campo, que com many=True funciona como uma coleção das PKs dos produtos associados
    # Em um ManyToManyField, que é o caso no banco de dados.
    products = se.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, allow_null=True)



class UpdateCoupomSerializer(se.Serializer):
    id = se.IntegerField()
    token = se.CharField(max_length=50, allow_null=True)
    multiplier = se.DecimalField(allow_null=True)
    expires_at = se.DateTimeField(allow_null=True)

    products = se.PrimaryKeyRelatedField(queryset=Product.objects.all(), many=True, allow_null=True)



class QueryCoupomSerializer(se.Serializer):
    id = se.IntegerField(allow_null=True)
    token = se.CharField(max_length=50, allow_null=True)
    minimum_multiplier = se.DecimalField(allow_null=True)
    maximum_multiplier = se.DecimalField(allow_null=True)
    created_before = se.DateTimeField(allow_null=True)
    created_after = se.DateTimeField(allow_null=True)
    expires_before = se.DateTimeField(allow_null=True)
    expires_after = se.DateTimeField(allow_null=True)
    product_id = se.IntegerField(allow_null=True)