from jogo.logica import logica_de_jogo as lj
from jogo.logica import utils
from jogo.models import Modulo, Medico, Rodada
from jogo.logica.time import Time
from threading import Lock
import datetime
import threading
import copy
from time import sleep
from channels import Group

JG_PRONTO = 0
JG_PAUSADO = 1
JG_NAO_INICIADO = 2
JG_EXECUTANDO = 3


class Timer(threading.Thread):
    def __init__(self, pausado, jogo):
        threading.Thread.__init__(self)
        self.se_pausado = pausado
        self.atualiza_timer = jogo.atualiza_timer;
        self.jogo = jogo
        self.timer = None

    def run(self):
        self.timer = self.jogo.rodadas[0].duracao * 60 * 1000000
        anterior = datetime.datetime.utcnow()
        #print (anterior)
        while self.timer is not None:
            if self.se_pausado.isSet() == False:
                self.se_pausado.wait()
                anterior = datetime.datetime.utcnow()

            atual = datetime.datetime.utcnow()
            delta_time = atual - anterior
            anterior = datetime.datetime.utcnow()
            self.timer = self.timer - delta_time.microseconds - delta_time.seconds*1000000
            #print(self.timer)
            segundos = (round(self.timer/1e6)) % 60
            minutos = (round(self.timer)/1e6)/60
            Group("timer").send({
            "text" : "%02d:%02d" % (minutos, segundos),
            })
            #print("timer: %0d" % (timer /1e6))
            sleep(0.5)
            if(self.timer < 0):
                self.timer = self.jogo.nova_rodada()


class InstanciaJogo:
    jogo_atual = None
    timer_thread = None
    pausado = None
    jogo_lock = None
    estado_jogo = JG_NAO_INICIADO
    def __init__(self):
        self.jogo = InstanciaJogo.jogo_atual
        self.timer_thread = InstanciaJogo.timer_thread
        self.pausado = InstanciaJogo.pausado
        self.jogo_lock = InstanciaJogo.jogo_lock
        self.estado_jogo = InstanciaJogo.estado_jogo

    @staticmethod
    def inicializa_jogo(modulos, tp_medicos, rodadas, times):
        """
            times: Lista de jogo.logica.time.Time
            rodadas: lista de jogo.models.Rodada
            tp_medicos: listas de tupla (id, qtd) de jogo.models.Medico
                        onde qtd é quantidade disponivel inicializar
            modulos: listas de id de jogo.models.Modulo
        """
        InstanciaJogo.jogo_atual = lj.Logica(modulos, tp_medicos, rodadas, times)
        InstanciaJogo.pausado = threading.Event()
        InstanciaJogo.timer_thread = t = Timer( InstanciaJogo.pausado, InstanciaJogo.jogo_atual)
        InstanciaJogo.jogo_lock = Lock()
        InstanciaJogo.estado_jogo = "inicializado"

    def avancar_rodada(self):
        pass

    def init_timer(self):
        self.timer_thread.start()
        self.pausado.set()
        InstanciaJogo.estado_jogo = "rodando"

    def pause(self):
        self.pausado.clear()

    def resume(self):
        self.pausado.set()

    def vender_modulo(self, nome_time, modulo_id):
        with self.jogo_lock:
            self.jogo_atual.vender_modulo(nome_time, modulo_id)
        return "ok"

    def comprar_modulo(self, nome_time, modulo_id):
        with self.jogo_lock:
            self.jogo_atual.comprar_modulo(nome_time, modulo_id)
        return "ok" # Retorna mensagem de erro ou sucesso

    def contratar_medico(self, nome_time, medico_id):
        with self.jogo_lock:
            self.jogo_atual.comprar_medico(nome_time, medico_id)
        return "ok"

    def despedir_medico(self, nome_time, medico_id):
        with self.jogo_lock:
            self.jogo_atual.vender_medico(nome_time, medico_id)
        return "ok"

    def get_estado_jogo(self):
        return self.estado_jogo

    def get_caixa(self, nome_time):
        return self.jogo.times[nome_time].estatisticas.get_ultimo_caixa()

    def get_medicos(self, nome_time=None):
        lista_medicos = None
        if nome_time == None:
            with self.jogo_lock:
                lista_medicos = copy.deepcopy(self.jogo_atual.medicos)
            medicos = []
            for id_med, qtd in lista_medicos.items():
                medico = Medico.objects.get(id = id_med)
                med = {}
                med["id"] = medico.id
                med["salario"] = "{:,.2f}".format(medico.salario)
                med["expertise"] = range(0, medico.expertise)
                med["atendimento"] = range(0, medico.atendimento)
                med["pontualidade"] = range(0, medico.pontualidade)
                med["qtd_disponiveis"] = qtd
                medicos.append(med)
            return medicos
        else:
            with self.jogo_lock:
                time = self.jogo_atual.times[nome_time]
                lista_medicos = copy.deepcopy(time.medicos)
            medicos = []
            for id_med in lista_medicos:
                medico = Medico.objects.get(id = id_med)
                med = {}
                med["id"] = medico.id
                med["salario"] = "{:,.2f}".format(medico.salario)
                med["expertise"] = range(0, medico.expertise)
                med["atendimento"] = range(0, medico.atendimento)
                med["pontualidade"] = range(0, medico.pontualidade)
                medicos.append(med)
            return medicos

        medicos = []
        for id_med, qtd in lista_medicos.items():
            medico = Medico.objects.get(id = id_med)
            med = {}
            med["id"] = medico.id
            med["salario"] = "{:,.2f}".format(medico.salario)
            med["expertise"] = range(0, medico.expertise)
            med["atendimento"] = range(0, medico.atendimento)
            med["pontualidade"] = range(0, medico.pontualidade)
            med["qtd_disponiveis"] = qtd
            medicos.append(med)
        return medicos

    def get_modulos(self, nome_time=None):
        modulos = None
        if nome_time is None:
            with self.jogo_lock:
                modulos = copy.deepcopy(self.jogo_atual.modulos)
        else:
            with self.jogo_lock:
                time = self.jogo_atual.times[nome_time]
                modulos = copy.deepcopy(time.modulos)

        modulos_p_areas = {}
        for id_mod in modulos:
            modulo = Modulo.objects.get(id = id_mod)
            if modulo.area.nome in modulos_p_areas:
                modulos_p_areas[modulo.area.nome].append(modulo)
            else:
                modulos_p_areas[modulo.area.nome] = [modulo]

            modulo.custo_de_aquisicao = "{:,.2f}".format(modulo.custo_de_aquisicao)
            modulo.custo_mensal = "{:,.0f}".format(modulo.custo_mensal)
            modulo.preco_do_tratamento = "{:,.0f}".format(modulo.preco_do_tratamento)
            modulo.tecnologia = range(0, modulo.tecnologia)
            modulo.conforto = range(0, modulo.conforto)

        return list(modulos_p_areas.keys()), modulos_p_areas

    def get_dados_graf_pizza(self, nome_time, rodada):
        data = {}
        estat = self.jogo_atual.times[nome_time].estatisticas
        for area in estat.lista_atr_mod[0].keys():
            temp = {}
            """lista com capacidades d"""
            temp["capacidade"] = estat.lista_atr_mod[rodada][area]["capacidade"]
            temp["total_atendidos"] =  estat.lista_total_atendidos[rodada][area]
            data[area] = temp
        return data

def __inicializa_jogo_pra_teste():
    if(InstanciaJogo.jogo_atual != None):
        return False
    i_jogo = InstanciaJogo()
    rodadas = Rodada.objects.all()
    times = []
    times.append(Time("time2"))
    tokens = utils.gerar_token(1)
    times[-1].codigo_login = tokens[-1]
    modulos = Modulo.objects.all()
    medicos = Medico.objects.all()
    modulos = [x.id for x in modulos]
    medicos = [(x.id, 3) for x in medicos]
    InstanciaJogo.inicializa_jogo(modulos, medicos, rodadas, times)
    return InstanciaJogo()
