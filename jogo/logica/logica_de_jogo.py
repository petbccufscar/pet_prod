#-*-coding:utf-8-*-
from jogo.logica.time import Time
from jogo.models import Medico, Modulo, Area_Classe_Social, Evento, Area, Classe_Social
from time import sleep
from channels import Group
from time import sleep
from django.http import HttpResponse
from django.core import serializers
import datetime
from random import randint
import _thread
import random
import simplejson
import datetime

#para teste
JogoAtual = None


def init_timer(jogo):
    _thread.start_new_thread(jogo.atualiza_timer, ())


def inicializa_jogo(rodadas, times):
    global JogoAtual # eu sei eu sei, chame de singleton e ta ok
    JogoAtual = Logica(len(rodadas), len(times), rodadas)
    for time in times:
        JogoAtual.add_time(time)
    init_timer(JogoAtual)


def encerrar_jogo():
    pass

def vender_modulo(request, nome_time):
    print(request.POST["modulo_id"], nome_time)
    print("vendido")
    return HttpResponse("vendido")


def comprar_modulo(request, nome_time):
    print("COMPREI UM MODULO")
    print(request.POST["modulo_id"], nome_time)
    JogoAtual.comprar_modulo(nome_time,int(request.POST["modulo_id"]))
    JogoAtual.encerrar_rodada()
    return HttpResponse("comprado")

def contratar_medico(request, nome_time):
    print(request.POST["medico_id"], nome_time)
    print("contratado")
    JogoAtual.comprar_medico(nome_time,int(request.POST["medico_id"]))
    return HttpResponse("contratado")


def despedir_medico(request, nome_time):
    print(request.POST["medico_id"], nome_time)
    print("despedido")
    return HttpResponse("despedido")

def busca_modulo(request, nome_time):
    print(request.POST["modulo_id"], nome_time)
    print("buscou id")
    data = serializers.serialize("json", [Modulo.objects.get(codigo = request.POST["modulo_id"]),])
    print(data)
    return HttpResponse(data)


class Logica(object):
    def __init__(self, qtd_rodadas, nrotimes, rodadas):
        self.qtd_rodadas = qtd_rodadas #TODO: talvez pegar qtd_rodadas com len()
        self.medicos_por_perfil = nrotimes*6 #TODO: Não deve ser hardcoded
        self.medicos = {}
        self.modulos = []
        self.times = dict()
        self.rodadas = rodadas
        self.rodada_atual = 0

        self.areas_c_social = [] # PRECISA DISSO?

        med = Medico.objects.all()
        mod = Modulo.objects.all()
        #TODO: isso deve ser pego da interface
        for medico in med:
            # inicia todos os perfis existentes no bd com 3 médicos
            self.medicos[medico.perfil] = 3
        for modulo in mod:
            self.modulos.append(modulo.codigo)

    def add_time(self, time):
        self.times[time.nome] = time

    def comprar_modulo(self, id_time, id_modulo):
        if id_modulo in self.modulos:           # fazer verificação se existe esse módulo
            self.times[id_time].modulos.append(id_modulo)
            self.times[id_time].estatisticas.comprasModulo[len(self.times[id_time].estatisticas.comprasModulo) - 1] += Modulo.objects.get(codigo=id_modulo).custo_de_aquisicao
            self.times[id_time].estatisticas.caixa[len(self.times[id_time].estatisticas.caixa) - 1] -= self.times[id_time].estatisticas.comprasModulo[len(self.times[id_time].estatisticas.comprasModulo) - 1]
            return True
        else:
            return False

    def vender_modulo(self, id_time, id_modulo):
        if id_modulo in self.times[id_time].modulos:        # fazer verificação se existe o time tem esse módulo
            i = self.times[id_time].modulos.index(id_modulo)
            #TODO: tratar questão de preço do modulo
            del self.times[id_time].modulos[i]
            return True
        else:
            return False


    def comprar_medico(self, time_id, perfil_medico):
        if (self.medicos[perfil_medico] > 0):
            self.times[time_id].adicionar_medico(perfil_medico)
            self.medicos[perfil_medico] -= 1
            return True

        return False



    def vender_medico(self, time_id, perfil_medico):
        # retorna true caso tenha tido sucesso, e false caso contrario
        # lembrar disso quando criar a view para renderizar a resposta correta
        if (self.times[time_id].remover_medico(perfil_medico)):
            self.medicos[perfil_medico] += 1
            return True

        return False


    def get_multiplicador(self, nomeEvento):
        evento = Evento.objects.get(nome=nomeEvento)
        multiplicadores  = {}
        multiplicadores['A'] = evento.multiplicador_classeA
        multiplicadores['B'] = evento.multiplicador_classeB
        multiplicadores['C'] = evento.multiplicador_classeC
        multiplicadores['D'] = evento.multiplicador_classeD
        multiplicadores['E'] = evento.multiplicador_classeE
        return multiplicadores


    def encerrar_rodada(self):
        print("ENCERRAR RODADA")
        areaClasse = Area_Classe_Social.objects.all()
        demanda = {}
        classeSocialDict = {}
        for i in areaClasse:

            try:
                classeSocialDict = demanda[i.area.nome]
            except KeyError:
                classeSocialDict = {}
                pass
            classeSocialDict[i.classe_social.nome] = randint(i.entrada - i.desvios, i.entrada + i.desvios)
            demanda[i.area.nome] = classeSocialDict

        #  CALCULAR TOTAL ATENDIDOS
        areas = Area.objects.all()
        classes = Classe_Social.objects.all()
        for time in self.times.values():
            capacidade_ocupada, entrada, saida = time.calcular_total_atendidos(demanda, areas, classes)
            # salvar em estatisticas
            #print("Entao, pra cada time: ", capacidade_ocupada,entrada,saida)
            # TODO: ta dando erro nessa chamada de função
            time.estatisticas.nova_rodada(entrada,saida,demanda, capacidade_ocupada)



    def nova_rodada(self):
        # TODO: tratar sincronização das threads
        # TODO: código de fim de rodada
        # Notificar os clients que acabou a rodada (websockets)
        # Fazer Calculo das estatisticas

        self.encerrar_rodada()

        # setup da nova rodada
        self.rodada_atual = self.rodada_atual + 1
        #print(self.rodada_atual)
        Group("rodada").send({
        "text": "Rodada: %s" % str(self.rodada_atual + 1),
        })

        if(self.rodada_atual == len(self.rodadas)):
            # Notificar fim de jogo
            return None

        # Notificar os clients que a proxima rodada comecou
        return self.rodadas[self.rodada_atual].duracao * 60 * 1000000

    def atualiza_timer(self):
        timer = self.rodadas[0].duracao * 60 * 1000000
        anterior = datetime.datetime.utcnow()
        #print (anterior)
        while timer is not None:
            atual = datetime.datetime.utcnow()
            delta_time = atual - anterior
            anterior = datetime.datetime.utcnow()
            timer = timer - delta_time.microseconds - delta_time.seconds*1000000
            #print(timer)
            segundos = (round(timer/1e6)) % 60
            minutos = (round(timer)/1e6)/60
            Group("timer").send({
            "text" : "%02d:%02d" % (minutos, segundos),
            })
            #print("timer: %0d" % (timer /1e6))
            sleep(0.5)
            if(timer < 0):
                timer = self.nova_rodada()
