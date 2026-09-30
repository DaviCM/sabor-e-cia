from rest_framework import serializers as se

from core.models import Units

UNITS = [(unit.name, unit.value) for unit in Units]

class CreateIngredientSerializer(se.Serializer):
    id = se.IntegerField(read_only=True)
    description = se.CharField(max_length=120)
    quantity = se.IntegerField(default=0)
    unit = se.ChoiceField(choices=UNITS)
    provider = se.CharField(max_length=120)



class UpdateIngredientSerializer(se.Serializer):
    description = se.CharField(max_length=120, allow_null=True)
    quantity = se.IntegerField(allow_null=True)
    unit = se.ChoiceField(choices=UNITS, allow_null=True)
    provider = se.CharField(allow_null=True)



class QueryIngredientSerializer(se.Serializer):
    id = se.IntegerField(allow_null=True)
    description = se.CharField(max_length=120, allow_null=True)
    minimum_quantity = se.IntegerField(allow_null=True)
    maximum_quantity = se.IntegerField(allow_null=True)
    unit = se.ChoiceField(choices=UNITS, allow_null=True)
    provider = se.CharField(max_length=120, allow_null=True)

