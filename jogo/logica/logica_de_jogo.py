#-*-coding:utf-8-*-
from jogo.logica.time import Time
import datetime
import _thread
from time import sleep
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

class Logica(object):
    def __init__(self, qtd_rodadas, nrotimes, rodadas):
        self.qtd_rodadas = qtd_rodadas
        self.medicos_por_perfil = nrotimes*6
        self.modulos = []
        self.rodadas = rodadas
        self.times = dict()
        self.rodada_atual = 0

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
            del self.times[id_time].modulos[i]
            return True
        else:
            return False
        self.rodadas = []
        self.rodada_atual = 0

    def next(self):
        # TODO: tratar sincronização das threads
        # TODO: código de fim de rodada
        # Notificar os clients que acabou a rodada (websockets)
        # Fazer Calculo das estatisticas

        self.rodada_atual = self.rodada_atual + 1
        #print(self.rodada_atual)
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
                #print("zerou")
                timer = self.next()
