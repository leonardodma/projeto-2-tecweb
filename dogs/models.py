from os import name
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class Dogs(models.Model):
    breed = models.CharField(max_length=200)
    img_url = models.CharField(max_length=1000)

    def __str__(self):
        return f'{self.breed}. {self.img_url}'


class Adoption(models.Model):
    breed = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    phone = PhoneNumberField(null=False, blank=False, unique=True)
    
    def __str__(self):
        return f'{self.id}. {self.name}'