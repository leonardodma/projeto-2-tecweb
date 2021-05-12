from os import name
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class PossibleBreeds(models.Model):
    breed = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.id}. {self.breed}'


class Dogs(models.Model):
    breed = models.CharField(max_length=200)
    img_url = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.breed}. {self.img_url}'


class Adoption(models.Model):
    name = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    adoption_url = models.CharField(max_length=300)
    breed_primary = models.CharField(max_length=100)
    breed_secondary = models.CharField(max_length=100)
    age = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    size = models.CharField(max_length=100)
    img_url = models.CharField(max_length=300)
    phone = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=100)
    adress = models.CharField(max_length=100)
    
    spayed_neutered = models.BooleanField()
    house_trained = models.BooleanField()
    special_needs = models.BooleanField()
    shots_current = models.BooleanField()

    favorite = models.BooleanField(default=False)

    
    def __str__(self):
        return f'{self.name}. {self.breed_primary} - {self.id}'
