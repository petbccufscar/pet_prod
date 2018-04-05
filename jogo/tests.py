from django.test import TestCase
from jogo.logica import logica_de_jogo as lj
from jogo.models import Rodada, Modulo, Area
from jogo.logica.time import Time
from jogo.logica.logica_de_jogo import Logica
import jogo.logica.time as time

class TesteLogica(TestCase):
    fixtures = ['jogo/initial_data.json']
    JogoAtual = None
    def setUp(self):
        times = []
        time1 = Time("time1")
        times.append(time1)
        rodadas = Rodada.objects.all()
        TesteLogica.JogoAtual = Logica(len(rodadas), len(times), rodadas)
        for time in times:
            TesteLogica.JogoAtual.add_time(time)

    def test_comprar_modulo(self):
        timeT = Time("timeT")
        TesteLogica.JogoAtual.modulos.append(0)
        TesteLogica.JogoAtual.add_time(timeT)
        TesteLogica.JogoAtual.comprar_modulo("timeT",0)
        assert(len(timeT.modulos) == 1)
        TesteLogica.JogoAtual.comprar_modulo("timeT",0)

    def test_atributos_modulos(self):
        resultado_esperado = {
            'tecnologia': 0,
            'conforto': 0,
            'preco_do_tratamento': 0,
            'capacidade': 0
        }

        obj = time.Time()
        """Quando o time não tem modulos"""
        assert(resultado_esperado == obj.atributos_modulos("Psicologia"))

        obj.adicionar_modulo(1)
        obj.adicionar_modulo(2)
        resultado_esperado = {
            'tecnologia': 1.5,
            'conforto': 2.5,
            'preco_do_tratamento': 25.0,
            'capacidade': 255
        }
        """Quando o time tem modulos"""
        assert(resultado_esperado == obj.atributos_modulos("Psicologia"))
