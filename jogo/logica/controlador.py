import copy
import datetime
import threading
from threading import Lock
from time import sleep

from channels import Group

from jogo.logica import logica_de_jogo as lj
from jogo.logica import utils
from jogo.models import Modulo, Medico, Rodada, Time
from jogo.logica import time as timeClass

JG_PRONTO = 0
JG_PAUSADO = 1
JG_NAO_INICIADO = 2
JG_EXECUTANDO = 3
JG_FINALIZADO = 4


class Timer(threading.Thread):
    def __init__(self, pausado, jogo):
        threading.Thread.__init__(self)
        self.se_pausado = pausado
        self.atualiza_timer = jogo.atualiza_timer
        self.jogo = jogo
        self.timer = None
        self.lock = Lock()
        self.fim_jogo = False
        self.waiting = threading.Event()

    def run(self):
        self.timer = self.jogo.rodadas[0].duracao * 60 * 1000000
        anterior = datetime.datetime.utcnow()
        Group("rodada").send({"text": "Rodada: %s" % str(1)})
        while self.timer is not None:
            if not self.se_pausado.isSet():
                self.waiting.set()
                self.se_pausado.wait()
                self.waiting.clear()
                anterior = datetime.datetime.utcnow()

            atual = datetime.datetime.utcnow()
            delta_time = atual - anterior
            anterior = datetime.datetime.utcnow()
            self.timer = self.timer - delta_time.microseconds - delta_time.seconds * 1000000
            segundos = (round(self.timer / 1e6)) % 60
            minutos = (round(self.timer) / 1e6) / 60
            Group("timer").send(dict(text="%02d:%02d" % (minutos, segundos)))
            print("%02d:%02d" % (minutos, segundos), file=open("timelog.txt", "a"))
            sleep(0.5)
            with self.lock:
                if self.fim_jogo:
                    break
            if self.timer < 0:
                print("Nova Rodada:", file=open("timelog.txt", "a"))
                self.timer = self.jogo.nova_rodada()

        InstanciaJogo.estado_jogo = JG_FINALIZADO
        Group("rodada").send(dict(text="Rodada:"))


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
        InstanciaJogo.jogo_atual = lj.Logica(modulos, tp_medicos, rodadas, times)
        InstanciaJogo.pausado = threading.Event()
        InstanciaJogo.timer_thread = Timer(InstanciaJogo.pausado, InstanciaJogo.jogo_atual)
        InstanciaJogo.jogo_lock = Lock()
        InstanciaJogo.estado_jogo = JG_PRONTO

    def avancar_rodada(self):
        self.pausado.clear()
        print("wtf")
        self.timer_thread.waiting.wait()
        print("wtff")
        self.timer_thread.timer = self.jogo_atual.nova_rodada()
        segundos = (round(self.timer_thread.timer / 1e6)) % 60
        minutos = (round(self.timer_thread.timer) / 1e6) / 60
        Group("timer").send(dict(text="%02d:%02d" % (minutos, segundos)))
        self.pausado.set()
        print("saind0")

    def init_timer(self):
        self.timer_thread.start()
        self.pausado.set()
        InstanciaJogo.estado_jogo = JG_EXECUTANDO

    def pause(self):
        self.pausado.clear()

    def resume(self):
        self.pausado.set()

    def finalizar_jogo(self):
        with self.timer_thread.lock:
            self.timer_thread.fim_jogo = True
            self.timer_thread.fim_jogo.join()

    def vender_modulo(self, nome_time, modulo_id):
        with self.jogo_lock:
            self.jogo_atual.vender_modulo(nome_time, modulo_id)
        return "ok"

    def comprar_modulo(self, nome_time, modulo_id):
        resultados = {
            lj.SUCESSO: (200, "Modulo Comprado"),
            lj.CAIXA_INSUFICIENTE: (405, "Caixa Insuficiente"),
        }
        with self.jogo_lock:
            ret = self.jogo_atual.comprar_modulo(nome_time, modulo_id)
            qtd = self.jogo_atual.modulos[modulo_id]
        Group("mercado").send(dict(text=utils.json_para_mercado("Modulo", modulo_id, qtd)))
        # Retorna mensagem de erro ou sucesso
        return resultados[ret]

    def contratar_medico(self, nome_time, medico_id):
        with self.jogo_lock:
            self.jogo_atual.comprar_medico(nome_time, medico_id)
            qtd = self.jogo_atual.medicos[medico_id]
        Group("mercado").send(dict(text=utils.json_para_mercado("Medico", medico_id, qtd)))
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
        if not nome_time:
            with self.jogo_lock:
                lista_medicos = copy.deepcopy(self.jogo_atual.medicos)
            medicos = []
            for id_med, qtd in lista_medicos.items():
                medico = Medico.objects.get(id=id_med)
                med = {"id": medico.id,
                       "salario": "{:,.2f}".format(medico.salario),
                       "expertise": range(0, medico.expertise),
                       "atendimento": range(0, medico.atendimento),
                       "pontualidade": range(0, medico.pontualidade), "qtd_disponiveis": qtd}
                medicos.append(med)
            return medicos
        else:
            with self.jogo_lock:
                time = self.jogo_atual.times[nome_time]
                lista_medicos = copy.deepcopy(time.medicos)
            medicos = []
            for id_med in lista_medicos:
                medico = Medico.objects.get(id=id_med)
                med = {
                    "id": medico.id,
                    "salario":
                        "{:,.2f}".format(medico.salario),
                    "expertise": range(0, medico.expertise),
                    "atendimento": range(0, medico.atendimento),
                    "pontualidade": range(0, medico.pontualidade)
                }
                medicos.append(med)
            return medicos

    def get_modulos(self, nome_time=None):
        if nome_time is None:
            with self.jogo_lock:
                modulos = copy.deepcopy(self.jogo_atual.modulos)
        else:
            with self.jogo_lock:
                time = self.jogo_atual.times[nome_time]
                modulos = copy.deepcopy(time.modulos)

        modulos_p_areas = {}
        for id_mod in modulos:
            modulo = Modulo.objects.get(id=id_mod)
            if modulo.area.nome in modulos_p_areas:
                modulos_p_areas[modulo.area.nome].append(modulo)
            else:
                modulos_p_areas[modulo.area.nome] = [modulo]

            modulo.custo_de_aquisicao = f"{modulo.custo_de_aquisicao:,.2f}"
            modulo.custo_mensal = f"{modulo.custo_mensal:,.0f}"
            modulo.preco_do_tratamento = f"{modulo.preco_do_tratamento:,.0f}"
            modulo.tecnologia = range(0,modulo.tecnologia)
            modulo.conforto = range(0,modulo.conforto)
            modulo.__dict__["qtd_disponiveis"] = modulos[id_mod]

        return list(modulos_p_areas.keys()), modulos_p_areas

    def get_dados_graf_pizza(self, nome_time, rodada):
        data = {}
        estat = self.jogo_atual.times[nome_time].estatisticas
        for area in estat.lista_atr_mod[0].keys():
            temp = {}
            """lista com capacidades d"""
            temp["capacidade"] = estat.lista_atr_mod[rodada][area]["capacidade"]
            temp["total_atendidos"] = estat.lista_total_atendidos[rodada][area]
            data[area] = temp
        return data

    def pontuacao(self):
        with self.jogo_lock:
            return [(x.nome, x.estatisticas.get_ultimo_caixa()) for x in self.jogo_atual.times.values()]


def __inicializa_jogo():
    if InstanciaJogo.jogo_atual:
        return False
    rodadas = Rodada.objects.all()
    times_cadastrados = Time.objects.order_by('id')
    times = []
    for t in times_cadastrados:
        tokens = utils.gerar_token()
        time = timeClass.Time(tokens, t.nome, t.caixa)
        times.append(time)

    modulos = Modulo.objects.all()
    medicos = Medico.objects.all()
    modulos = [x.id for x in modulos]
    medicos = [(x.id, 3) for x in medicos]
    InstanciaJogo.inicializa_jogo(modulos, medicos, rodadas, times)
    return InstanciaJogo()
