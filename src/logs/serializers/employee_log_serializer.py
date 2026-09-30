from rest_framework import serializers as se

from users.models import Roles

ROLES = [(role.name, role.value) for role in Roles]

class ResponseEmployeeLogSerializer(se.Serializer):
    id = se.IntegerField(read_only=True)
    datetime = se.DateTimeField(read_only=True)
    role = se.ChoiceField(max_length=120, read_only=True)

    employee_id = se.IntegerField(read_only=True)
    employee_username = se.CharField(max_length=120, read_only=True)



class QueryEmployeeLogSerializer(se.Serializer):
    id = se.IntegerField(allow_null=True)
    minimum_date = se.DateTimeField(allow_null=True)
    maximum_date = se.DateTimeField(allow_null=True)
    role = se.ChoiceField(choices=ROLES, allow_null=True)

    employee_id = se.IntegerField(allow_null=True)
    employee_username = se.CharField(max_length=120, allow_null=True)