from rest_framework import serializers as se

class ResponseDeliveryLogSerializer(se.Serializer):
    id = se.IntegerField(read_only=True)
    datetime = se.DateTimeField(read_only=True)
    delivery_fee = se.DecimalField(read_only=True)

    address_id = se.IntegerField()
    address_cep = se.CharField(max_length=50, read_only=True)
    address_description = se.CharField(max_length=120, read_only=True)
    address_number = se.IntegerField(read_only=True)

    deliverer_id = se.IntegerField(read_only=True)
    deliverer_username = se.CharField(max_length=120, read_only=True)

    order_id = se.IntegerField(read_only=True)



class QueryDeliveryLogSerializer(se.Serializer):
    id = se.IntegerField(allow_null=True)
    minimum_date = se.DateTimeField(allow_null=True)
    maximum_date = se.DateTimeField(allow_null=True)
    minimum_fee = se.DecimalField(allow_null=True)
    maximum_fee = se.DecimalField(allow_null=True)

    address_id = se.IntegerField(allow_null=True)
    address_cep = se.CharField(max_length=50, allow_null=True)
    address_description = se.CharField(max_length=120, allow_null=True)
    address_number = se.IntegerField(allow_null=True)

    deliverer_id = se.IntegerField(allow_null=True)
    deliverer_username = se.CharField(max_length=120, allow_null=True)

    order_id = se.IntegerField(allow_null=True)