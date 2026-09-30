from django.db import models
from django.db.models.functions import Now

class ClientReview(models.Model):
    score = models.PositiveIntegerField(null=False)
    notes = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(db_default=Now())
    last_edited_at = models.DateTimeField(db_default=Now())

    client = models.ForeignKey(to="users.Client", on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(to="core.Order", on_delete=models.CASCADE, null=True)