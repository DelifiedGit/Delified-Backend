from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    username = models.CharField(max_length=255, unique=True)
    gender = models.CharField(max_length=10)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=15)
    institution = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']

class MUN(models.Model):
    creator = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    event_name = models.CharField(max_length=255)
    date = models.DateField()
    venue = models.CharField(max_length=255)
    description = models.CharField(max_length=500)
    registration_fees = models.DecimalField(max_digits=10, decimal_places=2)
    custom_fields = models.JSONField(default=dict)



    def __str__(self):
        return self.event_name