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

def vender_modulo(request):
    if 'nome_time' not in request.session:
        return HttpResponse("Usuário Não Logado")

    nome_time = request.session['nome_time']

    print("VENTI UM MODULO")

    # JogoAtual.encerrar_rodada()
    JogoAtual.vender_modulo(nome_time, int(request.POST["modulo_id"]))
    return HttpResponse(JogoAtual.times[nome_time].estatisticas.get_ultimo_caixa())


def comprar_modulo(request):
    if 'nome_time' not in request.session:
        return HttpResponse("Usuário Não Logado")

    nome_time = request.session['nome_time']

    print("COMPREI UM MODULO")
    print(request.POST["modulo_id"], nome_time)
    JogoAtual.comprar_modulo(nome_time,int(request.POST["modulo_id"]))
    return HttpResponse(JogoAtual.times[nome_time].estatisticas.get_ultimo_caixa())

def contratar_medico(request):
    if 'nome_time' not in request.session:
        return HttpResponse("Usuário Não Logado")

    nome_time = request.session['nome_time']

    print(request.POST["medico_id"], nome_time)
    print("contratado")
    JogoAtual.comprar_medico(nome_time,int(request.POST["medico_id"]))
    return HttpResponse("contratado")


def despedir_medico(request):
    if 'nome_time' not in request.session:
        return HttpResponse("Usuário Não Logado")

    nome_time = request.session['nome_time']

    print(request.POST["medico_id"], nome_time)
    JogoAtual.vender_medico(nome_time, int(request.POST["medico_id"]))
    print("despedido")
    return HttpResponse("despedido")

def busca_modulo(request):
    data = serializers.serialize("json", [Modulo.objects.get(id = request.POST["modulo_id"]), ])
    return HttpResponse(data)

def busca_medico(request):
    data = serializers.serialize("json", [Medico.objects.get(id = request.POST["medico_id"]), ])
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
            self.medicos[medico.id] = 3
        for modulo in mod:
            self.modulos.append(modulo.id)

    def add_time(self, time):
        self.times[time.nome] = time

    def comprar_modulo(self, id_time, id_modulo):
        if id_modulo in self.modulos:           # verificação se existe esse módulo
            time = self.times[id_time]
            custo_modulo = Modulo.objects.get(id=id_modulo).custo_de_aquisicao
            if time.estatisticas.get_ultimo_caixa() >= custo_modulo:
                time.adicionar_modulo(id_modulo)
                time.estatisticas.comprasModulo[-1] += custo_modulo # [-1] acessa a última posição do vetor
                time.estatisticas.caixa[-1] -= custo_modulo # ja deve ser feito essa conta na hora pois não pode ficar endividado por compra, apenas por má administração
                return True
            else:
                return False

    def vender_modulo(self, id_time, id_modulo):
        if self.rodada_atual < len(self.rodadas) - 1:         # Só pode vender módulos até antes do último mês
            time = self.times[id_time]
            if id_modulo in time.modulos:        # verificação se o time tem esse módulo
                time.remover_modulo(id_modulo)
                custo_modulo = Modulo.objects.get(id=id_modulo).custo_de_aquisicao * 0.4 # o módulo é vendido por 40% do preco de aquisição
                time.estatisticas.vendasModulo[-1] += custo_modulo  # [-1] acessa a última posição do vetor
                time.estatisticas.caixa[-1] += custo_modulo  # para ser igual a compra, a venda já é calculada agora
                return True
            else:
                return False
        else:
            return False


    def comprar_medico(self, id_time, perfil_medico):
        if (self.medicos[perfil_medico] > 0):
            time = self.times[id_time]
            time.adicionar_medico(perfil_medico)
            self.medicos[perfil_medico] -= 1
            return True
        else:
            return False

    def vender_medico(self, id_time, perfil_medico):
        #TODO: fazer verificação se pode vender o médico .. 3 meses depois de contratado?
        # retorna true caso tenha tido sucesso, e false caso contrario
        # lembrar disso quando criar a view para renderizar a resposta correta
        time = self.times[id_time]
        if (time.remover_medico(perfil_medico)):
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
            total_atendidos, entrada_atendimento, entradas_por_area, salarios_medicos, manutencao_modulos, atributos_modulos = time.calcular_total_atendidos(demanda, areas, classes)
            # salvar em estatisticas
            # REVIEW: talvez salvar_estatisticas seja um nome melhor para a função (Verificar)
            time.estatisticas.nova_rodada(entrada_atendimento, demanda, total_atendidos, entradas_por_area, salarios_medicos, manutencao_modulos, atributos_modulos)



    def nova_rodada(self):
        # TODO: tratar sincronização das threads
        # TODO: código de fim de rodada
        # Notificar os clients que acabou a rodada (websockets)
        # Fazer Calculo das estatisticas

        self.encerrar_rodada()

        # setup da nova rodada
        self.rodada_atual = self.rodada_atual + 1
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
