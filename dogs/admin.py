from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Dogs)
admin.site.register(Adoption)
admin.site.register(PossibleBreeds)