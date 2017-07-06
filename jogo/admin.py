from django.contrib import admin
from .models import Rodada
from .models import Evento
from .models import Emprestimo, Area
from .models import Medico, Classe_Social, Modulo

# Register your models here.
# Ao implementar uma classe nova no Models
# Colocar ela aqui, para que o django admin gerencie ela
admin.site.register(Medico)
admin.site.register(Evento)
admin.site.register(Emprestimo)
admin.site.register(Area)
admin.site.register(Classe_Social)
admin.site.register(Rodada)
admin.site.register(Modulo)