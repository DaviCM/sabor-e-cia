from rest_framework import serializers as se

from users.models import Roles

class CreateEmployeeSerializer(se.Serializer):
    id = se.IntegerField(read_only=True)
    first_name = se.CharField(max_length=120)
    last_name = se.CharField(max_length=120)
    username = se.CharField(max_length=120)
    email = se.EmailField(max_length=120)
    password = se.CharField(max_length=255, write_only=True)
    cpf = se.CharField(max_length=50)
    role = se.CharField(max_length=50)



class UpdateEmployeeSerializer(se.Serializer):
    ROLES = [(role.name, role.value) for role in Roles]

    first_name = se.CharField(max_length=120, allow_null=True)
    last_name = se.CharField(max_length=120, allow_null=True)
    username = se.CharField(max_length=120, allow_null=True)
    email = se.EmailField(max_length=120, allow_null=True)
    password = se.CharField(max_length=255, write_only=True, allow_null=True)
    cpf = se.CharField(max_length=50, allow_null=True)
    role = se.ChoiceField(choices=ROLES)