from django.http import JsonResponse

class Estatistica:

    def __init__(self, caixa_inicial = 20000):
        self.entrada = []
        self.saida = []
        self.caixa = []
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

    def __init__(self, nome='Team with no name'):
        self.nome = nome
        self.medicos = []
        self.modulos = []
        self.estatisticas = Estatistica()
        self.atributos = {}
        self.nome = nome

    def adicionar_medico(self, med_id):
        self.medicos.append(med_id)

    # retorna true caso a operacao tenha sido bem sucedida
    def remover_medico(self, med_id):
        if med_id in self.medicos:
            self.medicos.remove(med_id)
            return True
        else:
            return False

    def gerar_link(self):
        pass
        # TODO: gerar link (logica do jogo)
