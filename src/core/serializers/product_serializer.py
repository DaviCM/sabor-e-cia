from rest_framework import serializers as se

from core.models import ProductCategories

CATEGORIES = [(category.name, category.value) for category in ProductCategories]

class CreateProductSerializer(se.Serializer):

    id = se.IntegerField(read_only=True)
    description = se.CharField(max_length=120)
    category = se.ChoiceField(choices=CATEGORIES)
    value = se.DecimalField()



class UpdateProductSerializer(se.Serializer):
    id = se.IntegerField(read_only=True, allow_null=True)
    description = se.CharField(max_length=120, allow_null=True)
    category = se.ChoiceField(choices=CATEGORIES, allow_null=True)
    value = se.DecimalField(allow_null=True)



class QueryProductSerializer(se.Serializer):
    id = se.IntegerField(allow_null=True)
    description = se.CharField(max_length=120, allow_null=True)
    category = se.ChoiceField(choices=CATEGORIES, allow_null=True)
    minimum_value = se.DecimalField(allow_null=True)
    maximum_value = se.DecimalField(allow_null=True)
