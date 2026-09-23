from django.db import models
from django.db.models.functions import Now

class Coupoms(models.Model):
    id = models.PositiveIntegerField(primary_key=True)
    token = models.CharField(max_length=50, null=False)
    multiplier = models.DecimalField(null=False)
    created_at = models.DateTimeField(db_default=Now(), null=False)
    expires_at = models.DateTimeField(null=False)