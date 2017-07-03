from django.contrib import admin
from .models import Medico
from .models import Evento

# Register your models here.
# Ao implementar uma classe nova no Models
# Colocar ela aqui, para que o django admin gerencie ela
admin.site.register(Medico)
admin.site.register(Evento)