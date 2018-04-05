#-*-coding:utf-8-*-
from jogo.logica.time import Time
from jogo.models import Medico, Modulo, Area_Classe_Social, Evento, Area, Classe_Social
from time import sleep
from channels import Group
from time import sleep
from django.http import HttpResponse
import datetime
from random import randint
import _thread
import random

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
    print(request.POST["modulo_id"], nome_time)
    JogoAtual.encerrar_rodada()
    return HttpResponse("comprado")

def contratar_medico(request, nome_time):
    print(request.POST["medico_id"], nome_time)
    print("contratado")
    return HttpResponse("contratado")


def despedir_medico(request, nome_time):
    print(request.POST["medico_id"], nome_time)
    print("despedido")
    return HttpResponse("despedido")


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
            # inicia todos os perfis existentes no bd com 0 médicos
            self.medicos[medico.perfil] = 0
        for modulo in mod:
            self.modulos.append(modulo.codigo)

    def add_time(self, time):
        self.times[time.nome] = time

    def comprar_modulo(self, id_time, id_modulo):
        if id_modulo in self.modulos:           # fazer verificação se existe esse módulo
            self.times[id_time].modulos.append(id_modulo)
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

        for time in self.times:
            capacidade_ocupada = self.calcular_total_atendidos(time,demanda)
            # salvar em estatisticas
            time.estatisticas.nova_rodada(0,0,demanda, capacidade_ocupada) #substituir os 0,0 por entrada e saida


    def calcular_total_atendidos(self, time, demanda):
        print("CALCULANDO ")
        areas = Area.objects.all()
        classes = Classe_Social.objects.all()

            #  VERIFICAR SE AS CLASSES SAO DE ACORDO

            capacidade_ocupada = {}

            atr_med = self.times[time].atributos_medicos()
            for ar in areas:

                atr_mod = self.times[time].atributos_modulos(ar)

                capacidade_disponivel = atr_mod['capacidade']

                for classe in classes:
                    if classe.media_conforto <= atr_mod['conforto'] and classe.nivel_tecnologia <= atr_mod['tecnologia'] and classe.preco_atendimento <= atr_mod['preco_do_tratamento'] and classe.nivel_especialidade <= atr_med['expertise'] and classe.velocidade_atendimento <= atr_med['atendimento']:
                         #faltou o pontualidade. E velocidade_atendimento = atendimento?

                         # Se o IF for verdadeiro, então pode atender essa classe!
                        print("pode atender essa classe ", classe )

                        # CALCULAR TOTAL DE ATENDIDOS
                        print("demanda dessa area classe: ", demanda[ar.nome][classe.nome])
                                # VER SE ACESSA A DEMANDA ASSIM
                        if demanda[ar.nome][classe.nome] < capacidade_disponivel:
                            capacidade_disponivel -= demanda[ar.nome][classe.nome]
                        elif capacidade_disponivel > 0:
                            capacidade_disponivel = 0
                            break
                print("capacidade disponivel", capacidade_disponivel)
                # CALCULAR DEPOIS O DINHEIRO GANHO COM ISSO
                # IRA UTILIZAR ALGO COMO
                capacidade_ocupada[ar.nome] = atr_mod['capacidade'] - capacidade_disponivel

            return capacidade_ocupada

    def nova_rodada(self):
        # TODO: tratar sincronização das threads
        # TODO: código de fim de rodada
        # Notificar os clients que acabou a rodada (websockets)
        # Fazer Calculo das estatisticas

        self.encerrar_rodada()

        # setup da nova rodada
        self.rodada_atual = self.rodada_atual + 1
        print(self.rodada_atual)
        Group("rodada").send({
        "text": "Rodada Atual: %s" % str(self.rodada_atual),
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
            sleep(0.1)
            if(timer < 0):
                timer = self.nova_rodada()
