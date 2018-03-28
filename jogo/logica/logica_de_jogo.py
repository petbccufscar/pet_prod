#-*-coding:utf-8-*-
from jogo.logica.time import Time
from jogo.models import Medico, Modulo, Area_Classe_Social
from time import sleep
from channels import Group
from time import sleep
from django.http import HttpResponse
import datetime
import _thread

#para teste
JogoAtual = None


def init_timer(jogo):
    _thread.start_new_thread(jogo.atualiza_timer, ())


def inicializa_jogo(rodadas, times):
    global JogoAtual # eu sei eu sei, chame de singleton e ta ok
    JogoAtual = Logica(len(rodadas), len(times), rodadas)
    for time in times:
        JogoAtual.add_time(time)
    init_timer(JogoAtual)


def encerrar_jogo():
    pass

def vender_modulo(request, nome_time):
    print(request.POST["modulo_id"], nome_time)
    print("vendido")
    return HttpResponse("vendido")


def comprar_modulo(request, nome_time):
    print(request.POST["modulo_id"], nome_time)
    return HttpResponse("comprado")

def contratar_medico(request, nome_time):
    print(request.POST["medico_id"], nome_time)
    print("contratado")
    return HttpResponse("contratado")


def despedir_medico(request, nome_time):
    print(request.POST["medico_id"], nome_time)
    print("despedido")
    return HttpResponse("despedido")


class Logica(object):
    def __init__(self, qtd_rodadas, nrotimes, rodadas):
        self.qtd_rodadas = qtd_rodadas
        self.medicos_por_perfil = nrotimes*6
        self.medicos = {}
        self.modulos = []
        self.times = dict()
        self.rodadas = rodadas
        self.rodada_atual = 0

        self.areas_c_social = [] # PRECISA DISSO?

        med = Medico.objects.all()
        mod = Modulo.objects.all()
        for medico in med:
            # inicia todos os perfis existentes no bd com 0 médicos
            self.medicos[medico.perfil] = 0
        for modulo in mod:
            self.modulos.append(modulo.codigo)

    def add_time(self, time):
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
            #TODO: tratar questão de preço do modulo 
            del self.times[id_time].modulos[i]
            return True
        else:
            return False


    def comprar_medico(self, time_id, perfil_medico):
        if (self.medicos[perfil_medico] > 0):
            self.times[time_id].adicionar_medico(perfil_medico)
            self.medicos[perfil_medico] -= 1
            return True

        return False



    def vender_medico(self, time_id, perfil_medico):
        # retorna true caso tenha tido sucesso, e false caso contrario
        # lembrar disso quando criar a view para renderizar a resposta correta
        if (self.times[time_id].remover_medico(perfil_medico)):
            self.medicos[perfil_medico] += 1
            return True

        return False


    def encerrar_rodada(self):

 #       for time in self.times:

            #LEO, AQUI CALCULAR DEMANDA (para cada time é diferente a demanda??) (se não for, fazer isso fora do for)


            #  VERIFICAR SE AS CLASSES SAO DE ACORDO
            # (o modelo está montado, mas o acesso a varias variaveis e dados estão incorretos ainda.
            # Então ficará comentado o bloco abaixo por enquanto, para não atrapalhar o código a rodar em outras partes)

            # atr_med = self.times[time].atributos_medicos()
            # for area_c in self.areas_c_social:
            #     ar_c = Area_Classe_Social.objects.get(area=area_c)  # COMO FAZ ISSO COM O AREA_CLASSE_SOCIAL? O ID SERIA COMO?
            #
            #     atr_mod = self.times[time].atributos_modulos(ar_c.area)
            #
            #     for classe in ar_c.classe_social:  # ESSE FOR TA ERRADO , oq quero é percorrer todas as classes sociais que tem daquela area
            #         if ar_c.classe_social.media_conforto <= atr_mod['conforto'] and ar_c.classe_social.nivel_tecnologia <= atr_mod['tecnologia'] and ar_c.classe_social.preco_atendimento <= atr_mod['preco_do_tratamento'] and ar_c.classe_social.nivel_especialidade <= atr_med['expertise'] and ar_c.classe_social.velocidade_atendimento <= atr_med['atendimento']:
            #             #é assim que acessa mesmo o dicionario?
            #             #faltou o pontualidade. E velocidade_atendimento = atendimento?
            #
            #             # Se o IF for verdadeiro, então pode atender essa classe!
            #             print("pode atender essa classe")


        pass

    def nova_rodada(self):
        # TODO: tratar sincronização das threads
        # TODO: código de fim de rodada
        # Notificar os clients que acabou a rodada (websockets)
        # Fazer Calculo das estatisticas

        self.encerrar_rodada()

        # setup da nova rodada
        self.rodada_atual = self.rodada_atual + 1
        print(self.rodada_atual)
        Group("rodada").send({
        "text": "Rodada Atual: %s" % str(self.rodada_atual),
        })

        if(self.rodada_atual == len(self.rodadas)):
            # Notificar fim de jogo
            return None

        # Notificar os clients que a proxima rodada comecou
        return self.rodadas[self.rodada_atual].duracao * 60 * 1000000

    def atualiza_timer(self):
        timer = self.rodadas[0].duracao * 60 * 1000000
        anterior = datetime.datetime.utcnow()
        #print (anterior)
        while timer is not None:
            atual = datetime.datetime.utcnow()
            delta_time = atual - anterior
            anterior = datetime.datetime.utcnow()
            timer = timer - delta_time.microseconds - delta_time.seconds*1000000
            #print(timer)
            sleep(0.1)
            if(timer < 0):
                timer = self.nova_rodada()
