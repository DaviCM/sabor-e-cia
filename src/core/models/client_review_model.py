from django.db import models

class ClientReview(models.Model):
    score = models.PositiveIntegerField(null=False)
    notes = models.CharField(max_length=255, null=True)

    client = models.ForeignKey(to="users.Client", on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(to="core.Order", on_delete=models.CASCADE, null=True)