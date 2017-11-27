class Time:
    nome = ''
    medicos = []
    modulos = []
    estatisticas = Estatistica()


    def __init__(self, nome):
        self.nome = nome


    def gerar_link(self):
        pass
        # todo: gerar link (logica do jogo)

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


    #todo get_ultimo_caixa

    #todo implementar um get_estatisticas retornando JSON
