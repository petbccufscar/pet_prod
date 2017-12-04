from django.http import JsonResponse

class Estatistica:
    entrada = []
    saida  = []
    caixa = []


    def __init__(self, caixa_inicial = 20000):
        self.entrada.append(0)
        self.saida.append(0)
        self.caixa.append(caixa_inicial)


    def nova_rodada(self, entrada, saida):
        self.entrada.append(entrada)
        self.saida.append(saida)
        self.caixa.append(self.caixa[-1] + entrada - saida)


    def get_ultimo_caixa(self):
        return self.caixa[-1]


    def get_estatisticas(self):
        data = {
            'caixa' : self.caixa,
            'entrada': self.entrada,
            'saida': self.saida
        }
        return JsonResponse({
            'status': 'ok',
            'data': data
        })



class Time:
    nome = ''
    medicos = []
    modulos = []
    estatisticas = Estatistica()


    def __init__(self, nome='Team with no name'):
        self.nome = nome


    def gerar_link(self):
        pass
        # todo: gerar link (logica do jogo)


