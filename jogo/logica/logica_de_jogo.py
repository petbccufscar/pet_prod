#-*-coding:utf-8-*-
from jogo.logica.time import Time
from jogo.models import Medico, Modulo
from time import sleep
from channels import Group
from time import sleep
from django.http import HttpResponse
import datetime
import _thread

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
    return HttpResponse("comprado")


class Logica(object):
    def __init__(self, qtd_rodadas, nrotimes, rodadas):
        self.qtd_rodadas = qtd_rodadas
        self.medicos_por_perfil = nrotimes*6
        self.medicos = {}
        self.modulos = []
        self.times = dict()
        self.rodadas = rodadas
        self.rodada_atual = 0
        med = Medico.objects.all()
        mod = Modulo.objects.all()
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


    def atributos_medicos(self, time_id):
        time = self.times[time_id]
        expertise = 0
        atendimento = 0
        pontualidade = 0
        quantidade = len(time.medicos)
        for medico in time.medicos:
            med = Medico.objects.get(perfil=medico)
            expertise += med.expertise
            atendimento += med.atendimento
            pontualidade += med.pontualidade
        return {
            'expertise' : expertise / quantidade,
            'atendimento' : atendimento / quantidade,
            'pontualidade' : pontualidade / quantidade
        }

    def encerrar_rodada(self):
        pass

    def nova_rodada(self):
        # TODO: tratar sincronização das threads
        # TODO: código de fim de rodada
        # Notificar os clients que acabou a rodada (websockets)
        # Fazer Calculo das estatisticas

        self.encerrar_rodada()

        # setup da nova rodada
        self.rodada_atual = self.rodada_atual + 1
        print(self.rodada_atual)
        Group("time").send({
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
        while timer is not None:
            atual = datetime.datetime.utcnow()
            delta_time = atual - anterior
            anterior = datetime.datetime.utcnow()
            timer = timer - delta_time.microseconds - delta_time.seconds*1000000
            sleep(0.1)
            if(timer < 0):
                timer = self.nova_rodada()
