from django.test import TestCase
from jogo.logica import logica_de_jogo as lj
from jogo.models import Rodada
from jogo.logica.time import Time

class TesteLogica(TestCase):
    def setUp(self):
        Rodada.objects.create(numeroRodada=1,duracao=1)
        Rodada.objects.create(numeroRodada=1,duracao=1)

    def test_inicializacao(self):
        rodadas = Rodada.objects.all()
        times = []
        lj.inicializa_jogo(rodadas, times)

    def test_comprar_modulo(self):
        rodadas = Rodada.objects.all()
        times = []
        time1 = Time("time1")
        times.append(time1)
        lj.inicializa_jogo(rodadas, times)
        lj.JogoAtual.modulos.append(0)
        lj.JogoAtual.comprar_modulo("time1",0)
        assert(len(time1.modulos) == 1)
        lj.JogoAtual.comprar_modulo("time1",0)
