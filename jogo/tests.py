from django.test import TestCase
from jogo.logica import logica_de_jogo as lj
from jogo.models import Rodada, Modulo, Area
from jogo.logica.time import Time

class TesteLogica(TestCase):
    fixtures = ['jogo/initial_data.json']
    def setUp(self):
        pass

    def test_inicializacao(self):
        rodadas = Rodada.objects.all()
        print(len(rodadas))
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

    def test_atributos_modulos(self):
        Area.objects.create(nome="1")
        ar = Area.objects.get(nome="1")
        #Modulo.objects.create(codigo=1,area=ar,custo_de_aquisicao=100,custo_mensal=100,tecnologia=1,conforto=1,capacidade=10,preco_do_tratamento=100)
        #Modulo.objects.create(codigo=2, area=ar, custo_de_aquisicao=200, custo_mensal=200, tecnologia=3, conforto=3, capacidade=20, preco_do_tratamento=200)

        import jogo.logica.time as time
        obj = time.Time()
        obj.adicionar_modulo(1)
        obj.adicionar_modulo(2)
        obj.modulos
        obj.atributos_modulos("1")
