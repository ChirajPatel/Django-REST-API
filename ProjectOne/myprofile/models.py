from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class MyProfile(models.Model):
    phone = models.IntegerField(null=True, blank=True, verbose_name="Phone number")
    address = models.TextField(null=True, blank=True, verbose_name="Address")
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="User id")

    def __str__(self):
        return self.user.first_name
