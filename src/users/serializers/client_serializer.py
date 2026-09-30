from rest_framework import serializers as se

class CreateClientSerializer(se.Serializer):
    id = se.IntegerField(read_only=True)
    first_name = se.CharField(max_length=120)
    last_name = se.CharField(max_length=120)
    username = se.CharField(max_length=120)
    email = se.EmailField(max_length=120)
    password = se.CharField(max_length=255, write_only=True)
    phone = se.CharField(max_length=50)



class UpdateClientSerializer(se.Serializer):
    first_name = se.CharField(max_length=120, allow_null=True)
    last_name = se.CharField(max_length=120, allow_null=True)
    username = se.CharField(max_length=120, allow_null=True)
    email = se.EmailField(max_length=120, allow_null=True)
    password = se.CharField(max_length=255, write_only=True, allow_null=True)
    phone = se.CharField(max_length=50, allow_null=True)