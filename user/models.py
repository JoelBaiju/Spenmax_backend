from django.contrib.auth.models import AbstractUser
from django.db import models
from user.variable import ADMIN ,USER,VENDOR

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        (USER, 'User'),
        (ADMIN, 'Admin'),
        (VENDOR, 'Vendor'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='user')
    block = models.BooleanField(default=False)





