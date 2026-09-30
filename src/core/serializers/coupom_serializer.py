from rest_framework import serializers as se

class CreateCoupomSchema(se.Serializer):
    id = se.IntegerField(read_only=True)
    token = se.CharField(max_length=50)
    multiplier = se.DecimalField()
    created_at = se.DateTimeField(read_only=True)
    expires_at = se.DateTimeField()



class UpdateCoupomSchema(se.Serializer):
    token = se.CharField(max_length=50, allow_null=True)
    multiplier = se.DecimalField(allow_null=True)
    expires_at = se.DateTimeField(allow_null=True)



class QueryCoupomSchema(se.Serializer):
    id = se.IntegerField(allow_null=True)
    token = se.CharField(max_length=50, allow_null=True)
    multiplier = se.DecimalField(allow_null=True)
    created_before = se.DateTimeField(allow_null=True)
    created_after = se.DateTimeField(allow_null=True)
    expires_before = se.DateTimeField(allow_null=True)
    expires_after = se.DateTimeField(allow_null=True)