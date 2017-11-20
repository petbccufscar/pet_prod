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

class Evento(models.Model):
    class Meta:
        verbose_name = 'evento'
        verbose_name_plural = 'eventos'

    def __str__(self):
        return self.nome
    def __unicode__(self):
        return self.nome

    nome = models.CharField(max_length=50)
    multiplicador_classeA = models.FloatField(validators=[MinValueValidator(0.0)])
    multiplicador_classeB = models.FloatField(validators=[MinValueValidator(0.0)])
    multiplicador_classeC = models.FloatField(validators=[MinValueValidator(0.0)])
    multiplicador_classeD = models.FloatField(validators=[MinValueValidator(0.0)])
    multiplicador_classeE = models.FloatField(validators=[MinValueValidator(0.0)])


class Emprestimo(models.Model):
    valor = models.FloatField(validators=[MinValueValidator(1.0)])
    # Nao deveria ter uma chave de um time?
    # TODO Não é "um time faz um emprestimo"?

#Tabela Time
class Time(models.Model):
    nome = models.CharField(max_length=20) #NOME DO TIME
    login = models.CharField(max_length=15) #LOGIN PARA ENTRAR NO SISTEMA
    senha = models.CharField(max_length=20)
    caixa = models.FloatField(validators=[MinValueValidator(0.0)]) #QUANTIDADE NO CAIXA

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
    # nivel_especialidade = models.IntegerField(default=1, choices=classificacao)
    # nivel_tecnologia = models.IntegerField(default=1, choices=classificacao)
    # media_conforto = models.IntegerField(default=1, choices=classificacao)
    # velocidade_atendimento = models.IntegerField(default=1, choices=classificacao)

class Rodada(models.Model):
    verbose_name = 'rodada'
    verbose_name_plural = 'rodadas'

    numeroRodada = models.IntegerField(validators=[MinValueValidator(1)])
    duracao = models.IntegerField(validators=[MinValueValidator(1)])
    # TODO implementar apos a implementacao da classe evento
    evento = models.ForeignKey(Evento, on_delete=models.CASCADE, default=1)



class Area_Classe_Social(models.Model):
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    classe_social = models.ForeignKey(Classe_Social, on_delete=models.CASCADE)
    entrada = models.IntegerField(validators=[MinValueValidator(1)])
    desvios = models.IntegerField(validators=[MinValueValidator(0)])

class Modulo(models.Model):
    classificacao = ((1, '1'), (2, '2'), (3, '3'))
    codigo = models.IntegerField(validators=[MinValueValidator(1)])
    area = models.ForeignKey(Area, on_delete=models.CASCADE)
    custo_de_aquisicao = models.FloatField(validators=[MinValueValidator(0.0)])
    custo_mensal = models.FloatField(validators=[MinValueValidator(0.0)])
    tecnologia = models.IntegerField(default=1, choices=classificacao)
    conforto = models.IntegerField(default=1, choices=classificacao)
    capacidade = models.IntegerField(validators=[MinValueValidator(1)])
    preco_do_tratamento = models.FloatField(validators=[MinValueValidator(0.0)])