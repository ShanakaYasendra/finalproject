from django.contrib import admin
from .models import Country,CountryCity,CountryDetails
# Register your models here.

admin.site.register(Country)
admin.site.register(CountryCity)
admin.site.register(CountryDetails)
