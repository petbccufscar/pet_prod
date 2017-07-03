from django.contrib import admin
from .models import Medico, Classe_Social

# Register your models here.
# Ao implementar uma classe nova no Models
# Colocar ela aqui, para que o django admin gerencie ela
admin.site.register(Medico)
admin.site.register(Classe_Social)