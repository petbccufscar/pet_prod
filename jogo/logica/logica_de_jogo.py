from jogo.models import Medico, Modulo
from jogo.logica.Time import Time

class Logica:

    def __init__(self):
        self.medicos= {}
        self.modulos = []
        self.times = []
        med = Medico.objects.all()
        mod = Modulo.objects.all()
        for medico in med:
            # inicia todos os perfis existentes no bd com 0 médicos
            self.medicos[medico.perfil] = 0
        for modulo in mod:
            self.modulos.append(modulo.codigo)


    def adicionar_time(self, nome = 'Nome do time'):
        self.times.append(Time(nome))


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


    def atributos_medicos(self, time_id):
        time = self.times[time_id]
        expertise = 0
        atendimento = 0
        pontualidade = 0
        quantidade = len(time.medicos)
        for medico in time.medicos:
            med = Medico.objects.get(perfil=medico)
            expertise += med.expertise
            atendimento += med.atendimento
            pontualidade += med.pontualidade
        return {
            'expertise' : expertise / quantidade,
            'atendimento' : atendimento / quantidade,
            'pontualidade' : pontualidade / quantidade
        }

    # todo: gerar links
