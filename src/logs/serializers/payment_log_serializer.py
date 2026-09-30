from rest_framework import serializers as se

from logs.models import PaymentMethods

METHODS = [(method.name, method.value) for method in PaymentMethods]

class ResponsePaymentLogSerializer(se.Serializer):
    id = se.IntegerField(read_only=True)
    datetime = se.DateTimeField(read_only=True)
    payment_method = se.ChoiceField(choices=METHODS, read_only=True)
    value = se.DecimalField(read_only=True)

    order_id = se.IntegerField(read_only=True)



class QueryPaymentLogSchema(se.Serializer):
    id = se.IntegerField(allow_null=True)
    minimum_date = se.DateTimeField(allow_null=True)
    maximum_date = se.DateTimeField(allow_null=True)
    payment_method = se.ChoiceField(choices=METHODS, allow_null=True)
    minimum_value = se.DecimalField(allow_null=True)
    maximum_value = se.DecimalField(allow_null=True)

    order_id = se.IntegerField(allow_null=True)