import datetime
import _thread
from time import sleep


class Logica(object):
    def __init__(self, qtd_rodadas, nrotimes):
        self.qtd_rodadas = qtd_rodadas
        self.medicos_por_perfil = nrotimes*6
        self.modulos = []
        self.rodadas = []
        self.rodada_atual = 0

    def next(self):
        # TODO: código de fim de rodada
        # Notificar os clients que acabou a rodada (websockets)
        # Fazer Calculo das estatisticas

        self.rodada_atual = self.rodada_atual + 1
        print(self.rodada_atual)
        if(self.rodada_atual == len(self.rodadas)):
            # Notificar fim de jogo
            return 0

        # Notificar os clients que a proxima rodada comecou
        return self.rodadas[self.rodada_atual].duracao * 60 * 1000000

    def atualiza_timer(self):
        timer = self.rodadas[0].duracao * 60 * 1000000
        anterior = datetime.datetime.utcnow()
        print (anterior)
        while(True):
            atual = datetime.datetime.utcnow()
            delta_time = atual - anterior
            anterior = datetime.datetime.utcnow()
            timer = timer - delta_time.microseconds - delta_time.seconds*1000000
            print(timer)
            sleep(0.1)
            if(timer < 0):
                print("zerou")
                timer = next()

#para teste
JogoAtual = Logica(5,5)
def init_timer():
    _thread.start_new_thread(JogoAtual.atualiza_timer, ())
