from django.db import models

class Client(models.Model):
    phone = models.CharField(max_length=50,null=False)

    user = models.OneToOneField(to="users.User", on_delete=models.CASCADE)