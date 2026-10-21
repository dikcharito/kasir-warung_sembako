from django.db import models
from django.contrib.auth.models import User

class Shipping(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    locality = models.CharField(max_length=100)
    landmark = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.user.username} - {self.address}"

    class Meta:
        verbose_name_plural = "Shipping Addresses"