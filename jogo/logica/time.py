from django.http import JsonResponse
from jogo.models import Medico, Modulo

class Estatistica:
    """
        comentarios sobre a classe e explicação das variaveis devem vir aqui
        porque ai pode acessar a documentacao com "Estatistica.__doc__"

    """
    def __init__(self, caixa_inicial = 2000000):
        #TODO: Explicação do que são essas variaveis todas
        self.entrada_atendimento = [] # total ganho com a soma do que foi ganho em cada area
        self.caixa = []

        self.lista_demandas = [] # lista de dicionarios

        self.lista_total_atendidos = [] # lista de dicionarios com o total de pessoas atendidas separadas por area (cada indice é uma rodada)

        self.lista_entradas_por_area = [] # lista de dicionarios

        # Todas as contas do caixa são realizadas no final, porem o jogador não pode ficar endividado por compra sem dinheiro,
        # apenas por má administração. Então as compras de módulos já são descontadas do caixa na hora. Porém é necessário armazenar
        # isso para aparecer no relatório depois, somado à saída, obtendo o valor total de gastos da rodada
        self.comprasModulo = []


        # O mesmo descrito acima serve para a venda de módulos
        self.vendasModulo = []

        # Listas para armazenar os custos de cada rodada sobre salario de medico e manutencao de modulo
        self.lista_salarios_medicos = []
        self.lista_manutencao_modulos = []


        # Lista de dicionarios que contem dicionarios com os atributos de modulos de cada rodada
        self.lista_atr_mod = []

        # Iniciando a primeira posição de cada vetor para ser usada na primeira rodada
        self.entrada_atendimento.append(0)
        self.caixa.append(caixa_inicial)
        self.lista_demandas.append({})
        self.lista_total_atendidos.append({})
        self.lista_entradas_por_area.append({})
        self.comprasModulo.append(0)
        self.vendasModulo.append(0)
        self.lista_salarios_medicos.append(0)
        self.lista_manutencao_modulos.append(0)
        self.lista_atr_mod.append(0)


    def nova_rodada(self, entrada_atendimento, demanda, total_atendidos, entradas_por_area, salarios_medicos, manutencao_modulos, atributos_modulos):
        # Atualizando ultima posição de cada vetor
        self.entrada_atendimento[-1] = entrada_atendimento

        self.caixa[-1] = self.caixa[-1] + entrada_atendimento - salarios_medicos - manutencao_modulos

        self.lista_demandas[-1] = demanda
        self.lista_total_atendidos[-1] = total_atendidos
        self.lista_entradas_por_area[-1] = entradas_por_area

        self.lista_salarios_medicos[-1] = salarios_medicos
        self.lista_manutencao_modulos[-1] = manutencao_modulos
        self.lista_atr_mod[-1] = atributos_modulos


        print("TEM CAIXA: ", self.caixa)

        # Preparando os vetores para a próxima rodada
        self.entrada_atendimento.append(0)
        self.caixa.append(self.caixa[-1])
        self.lista_demandas.append({})
        self.lista_total_atendidos.append({})
        self.lista_entradas_por_area.append({})
        self.comprasModulo.append(0)
        self.vendasModulo.append(0)
        self.lista_salarios_medicos.append(0)
        self.lista_manutencao_modulos.append(0)
        self.lista_atr_mod.append(0)



    def get_ultimo_caixa(self):
        return self.caixa[-1]


    def get_estatisticas(self):
        total_saida = []
        total_entrada = []
        lucro = []

        for i in range(0, len(self.lista_salarios_medicos)):
            total_saida.append(self.comprasModulo[i] + self.lista_manutencao_modulos[i] + self.lista_salarios_medicos[i]) #TODO: depois vai ter - saida de emprestimo[i] aqui
            total_entrada.append(self.entrada_atendimento[i] + self.vendasModulo[i]) # TODO: depois vai ter + entrada de emprestimo[i]
            lucro.append(total_entrada[-1] - total_saida[-1])

        data = {
            # TODO: no futuro vai ter entrada e saida de emprestimo aqui
            'vendas_modulos': self.vendasModulo,
             'total_entrada': total_entrada,
            'custo_aquisicao': self.comprasModulo,
            'custos_modulos': self.lista_manutencao_modulos,
            'salarios_medicos': self.lista_salarios_medicos,
            'total_saida': total_saida,
            'lucro': lucro,
            'caixa': self.caixa
        }

        # Adicionando lista de entradas por area
        areas = self.lista_entradas_por_area[0].keys()
        for area in areas:
            entradas_da_area = [entrada[area] for entrada in self.lista_entradas_por_area if entrada]
            data.update({area: entradas_da_area})
        return data


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
            med = Medico.objects.get(id=medico)
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
        quantidade = 0

        for modulo_id in self.modulos:
            mod = Modulo.objects.get(id=modulo_id)
            if mod.area.nome == area.nome: # transformar para id
                quantidade += 1
                tecnologia += mod.tecnologia
                conforto += mod.conforto
                preco_do_tratamento += mod.preco_do_tratamento
                capacidade += mod.capacidade
                total_custo_mensal += mod.custo_mensal

        if quantidade == 0:
            return {
                'tecnologia': 0,
                'conforto': 0,
                'preco_do_tratamento': 0,
                'capacidade': 0,
                'total_custo_mensal': 0

            }
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

        #  VERIFICAR SE AS CLASSES SAO DE ACORDO

        total_atendidos = {}
        entradas_por_area = {}
        entrada_atendimento = 0
        manutencao_modulos = 0
        atributos_modulos = {}

        atr_med = self.atributos_medicos()

        for area in areas:
            atr_mod = self.atributos_modulos(area)
            atributos_modulos[area.nome] = atr_mod

            capacidade_disponivel = atr_mod['capacidade']

            for classe in classes:

                if (classe.media_conforto <= atr_mod['conforto'] and
                        classe.nivel_tecnologia <= atr_mod['tecnologia'] and
                        classe.preco_atendimento >= atr_mod['preco_do_tratamento'] and
                        classe.nivel_especialidade <= atr_med['expertise'] and
                        classe.velocidade_atendimento <= atr_med['atendimento']):

                     #TODO: faltou o pontualidade. E velocidade_atendimento = atendimento?

                    # CALCULAR TOTAL DE ATENDIDOS

                    if demanda[area.nome][classe.nome] < capacidade_disponivel:
                        capacidade_disponivel -= demanda[area.nome][classe.nome]
                    elif capacidade_disponivel > 0:
                        capacidade_disponivel = 0
                        break

            # CALCULAR DEPOIS O DINHEIRO GANHO COM ISSO

            total_atendidos[area.nome] = atr_mod['capacidade'] - capacidade_disponivel
            entradas_por_area[area.nome] = total_atendidos[area.nome] * atr_mod['preco_do_tratamento']
            entrada_atendimento = entrada_atendimento + entradas_por_area[area.nome]
            manutencao_modulos = manutencao_modulos + atr_mod['total_custo_mensal']

        salarios_medicos = atr_med['total_salarios']

        return total_atendidos, entrada_atendimento, entradas_por_area, salarios_medicos, manutencao_modulos, atributos_modulos
