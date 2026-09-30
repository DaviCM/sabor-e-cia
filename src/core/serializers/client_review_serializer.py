from rest_framework import serializers as se

class CreateClientReviewSerializer(se.Serializer):
    id = se.IntegerField(read_only=True)
    score = se.IntegerField()
    notes = se.CharField(max_length=255)
    created_at = se.DateTimeField(read_only=True)
    last_edited_at = se.DateTimeField(read_only=True)

    client_id = se.IntegerField()
    order_id = se.IntegerField()



class UpdateClientReviewSerializer(se.Serializer):
    score = se.IntegerField(allow_null=True)
    notes = se.CharField(max_length=255, allow_null=True)



class QueryClientReviewSchema(se.Serializer):
    id = se.IntegerField(allow_null=True)
    minimum_date = se.DateTimeField(allow_null=True)
    maximum_date = se.DateTimeField(allow_null=True)
    minimum_score = se.IntegerField(allow_null=True)
    maximum_score = se.IntegerField(allow_null=True)
    notes = se.CharField(max_length=255, allow_null=True)
    client_id = se.IntegerField(allow_null=True)
    order_id = se.IntegerField(allow_null=True)