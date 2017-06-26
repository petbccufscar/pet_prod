from django.db import models
from django.core.validators import MinValueValidator


# Tabela Médico
class Medico(models.Model):
    classificacao = ((1,'1'),(2,'2'),(3,'3'))
    # id = models.AutoField(u'id', primary_key=True, unique=True)
    # Só deixei comentado aqui para lembrar todos de fazer isso!
    perfil = models.IntegerField(validators=[MinValueValidator(1)])
    salario = models.FloatField(validators=[MinValueValidator(0.0)])
    expertise = models.IntegerField(default=1, choices=classificacao)
    atendimento = models.IntegerField(default=1, choices=classificacao)
    pontualidade = models.IntegerField(default=1, choices=classificacao)
    # Não esqueçam de fazer a migração para o novo BD:
    # Tools -> Run manage.py task -> makemigrations -> migrate

class Rodada(models.Model):
    verbose_name = 'rodada'
    verbose_name_plural = 'rodadas'

    numeroRodada = models.IntegerField(validators=[MinValueValidator(1)])
    duracao = models.IntegerField(validators=[MinValueValidator(1)])
    # TODO implementar apos a implementacao da classe evento
    # evento = models.ForeignKey(Evento, on_delete=models.CASCADE, default=1)
