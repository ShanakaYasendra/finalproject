from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Country(models.Model):
    countryId= models.CharField(max_length=3)
    iso2Code= models.CharField(max_length=3)
    name= models.CharField(max_length=100)
    region= models.CharField(max_length=3)
    regionIso=models.CharField(max_length=3)
    regionValue= models.CharField(max_length=50)
    capitalCity= models.CharField(max_length=100)
    longitude=models.CharField(max_length=10)
    latitude= models.CharField(max_length=10)

    def __str__(self):
        return f"{self.id}-{self.iso2Code}-{self.name}-{self.region}-{self.regionIso}-{self.regionValue}-{self.capitalCity}-{self.longitude}-{self.latitude}"