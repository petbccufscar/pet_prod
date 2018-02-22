#-*-coding:utf-8-*-
from jogo.logica.Time import Time

class Logica():
    times = []
    def __init__(self, qtd_rodadas, nrotimes):
        self.qtd_rodadas = qtd_rodadas
        self.medicos_por_perfil = nrotimes*6
        self.modulos = []
        self.times = dict()

    def add_time(time):
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
