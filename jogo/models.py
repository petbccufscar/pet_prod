from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

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

#template -> views -> models
# Tabela Area
class Area(models.Model):
    # id = models.AutoField(u'id', primary_key=True, unique=True)
    nome = models.CharField(max_length=200)
    def __str__(self):
        return self.nome
    def __unicode__(self):
        return self.nome

# Classe_Social

class Classe_Social(models.Model):
    classificacao = ((1, '1'), (2, '2'), (3, '3'))
    #id = models.AutoField(u'id', primary_key=True, unique=True)
    nome = models.CharField(max_length=200)
    preco_atendimento = models.FloatField(validators=[MinValueValidator(0.0)])
    nivel_especialidade = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(3.0)])
    nivel_tecnologia = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(3.0)])
    media_conforto = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(3.0)])
    velocidade_atendimento = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(3.0)])

# Tabela Area_Classe_Social TODO

class Area_Classe_Social(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    classe_social = models.ForeignKey(Classe_Social, on_delete=models.CASCADE) 
    entrada = models.IntegerField(validators=[MinValueValidator(1)])
    desvios = models.IntegerField(validators=[MinValueValidator(0)])
