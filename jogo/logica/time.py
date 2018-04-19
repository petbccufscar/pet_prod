from django.http import JsonResponse
from jogo.models import Medico, Modulo

class Estatistica:

    def __init__(self, caixa_inicial = 20000):
        self.entrada = []
        self.saida = []
        self.caixa = []
        self.demanda = [] # lista de dicionarios
        self.total_atendidos = [] # lista de dicionarios
        self.caixa.append(caixa_inicial)
        self.demanda.append(None)
        self.total_atendidos.append(None)
        self.comprasModulo = []
        self.comprasModulo.append(0)

    def nova_rodada(self, entrada, saida, demanda, total_atendidos):
        self.entrada.append(entrada)
        self.saida.append(saida)
        self.caixa.append(self.caixa[-1] + entrada - saida)
        self.demanda.append(demanda)
        self.total_atendidos.append(total_atendidos)
        self.comprasModulo.append(0)
        #print("TEM CAIXA: ", self.caixa)


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

    def adicionar_modulo(self, mod_id):
        self.modulos.append(mod_id)

        # retorna true caso a operacao tenha sido bem sucedida

    def remover_modulo(self, mod_id):
        if mod_id in self.modulos:
            self.modulos.remove(mod_id)
            return True
        else:
            return False

    def atributos_medicos(self):
        expertise = 0
        atendimento = 0
        pontualidade = 0
        total_salarios =0
        quantidade = len(self.medicos)
        if quantidade == 0:
            return {
                'expertise': 0,
                'atendimento': 0,
                'pontualidade': 0,
                'total_salarios': 0
            }
        for medico in self.medicos:
            med = Medico.objects.get(perfil=medico)
            expertise += med.expertise
            atendimento += med.atendimento
            pontualidade += med.pontualidade
            total_salarios += med.salario
        return {
            'expertise': expertise / quantidade,
            'atendimento': atendimento / quantidade,
            'pontualidade': pontualidade / quantidade,
            'total_salarios': total_salarios
        }

    def atributos_modulos(self, area):
        tecnologia = 0
        conforto = 0
        capacidade = 0
        preco_do_tratamento = 0
        total_custo_mensal = 0
        quantidade = len(self.modulos)
        if quantidade == 0:
            return {
            'tecnologia': 0,
            'conforto': 0,
            'preco_do_tratamento': 0,
            'capacidade': 0,
            'total_custo_mensal': 0

        }
        for modulo_id in self.modulos:
            mod = Modulo.objects.get(codigo=modulo_id)
            if mod.area.nome == area.nome: # transformar para id
                tecnologia += mod.tecnologia
                conforto += mod.conforto
                preco_do_tratamento += mod.preco_do_tratamento
                capacidade += mod.capacidade
                total_custo_mensal += mod.custo_mensal
        return {
            'tecnologia': tecnologia / quantidade,
            'conforto': conforto / quantidade,
            'preco_do_tratamento': preco_do_tratamento / quantidade,
            'capacidade': capacidade,
            'total_custo_mensal': total_custo_mensal
        }

    def gerar_link(self):
        pass
        # TODO: gerar link (logica do jogo)


    def calcular_total_atendidos(self, demanda, areas, classes):
        #print("CALCULANDO ")

        #  VERIFICAR SE AS CLASSES SAO DE ACORDO

        capacidade_ocupada = {}
        entrada = 0
        saida = 0
        atr_med = self.atributos_medicos()
        for ar in areas:
            atr_mod = self.atributos_modulos(ar)
            capacidade_disponivel = atr_mod['capacidade']

            for classe in classes:


                if classe.media_conforto <= atr_mod['conforto'] and classe.nivel_tecnologia <= atr_mod['tecnologia'] and classe.preco_atendimento >= atr_mod['preco_do_tratamento'] and classe.nivel_especialidade <= atr_med['expertise'] and classe.velocidade_atendimento <= atr_med['atendimento']:
                     #faltou o pontualidade. E velocidade_atendimento = atendimento?

                     # Se o IF for verdadeiro, então pode atender essa classe!
                    #print("pode atender essa classe ", classe )

                    # CALCULAR TOTAL DE ATENDIDOS
                    #print("demanda dessa area classe: ", demanda[ar.nome][classe.nome])
                            # VER SE ACESSA A DEMANDA ASSIM
                    if demanda[ar.nome][classe.nome] < capacidade_disponivel:
                        capacidade_disponivel -= demanda[ar.nome][classe.nome]
                    elif capacidade_disponivel > 0:
                        capacidade_disponivel = 0
                        break
            #print("capacidade disponivel", capacidade_disponivel)

            # CALCULAR DEPOIS O DINHEIRO GANHO COM ISSO

            capacidade_ocupada[ar.nome] = atr_mod['capacidade'] - capacidade_disponivel
            entrada= entrada + capacidade_ocupada[ar.nome] * atr_mod['preco_do_tratamento']
            saida = saida + atr_mod['total_custo_mensal']

        saida = saida + atr_med['total_salarios']

        return capacidade_ocupada, entrada, saida
