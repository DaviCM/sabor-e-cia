from rest_framework import serializers as se

class CreateAddressSerializer(se.Serializer):
    id = se.IntegerField(read_only=True)
    cep = se.CharField(max_length=50)
    description = se.CharField(max_length=120)
    number = se.IntegerField()



class UpdateAddressSerializer(se.Serializer):
    cep = se.CharField(max_length=50, allow_null=True)
    description = se.CharField(max_length=120, allow_null=True)
    number = se.IntegerField(allow_null=True)


