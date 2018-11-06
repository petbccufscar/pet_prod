from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render

from jogo.logica import controlador as ctrler
from jogo.models import Modulo


def ajax_sanitizer(func):
    def requisicao_ajax(request):
        controlador = ctrler.InstanciaJogo()
        if controlador.estado_jogo == ctrler.JG_NAO_INICIADO:
            return HttpResponse("Jogo Não Iniciado")
        if controlador.estado_jogo == ctrler.JG_PAUSADO:
            return HttpResponse("Jogo Não Iniciado")
        if controlador.estado_jogo == ctrler.JG_PRONTO:
            return HttpResponse("Jogo Não Iniciado")
        if 'nome_time' not in request.session:
            return HttpResponse("Usuário Não Logado")

        return func(request)

    return requisicao_ajax


def encerrar_jogo():
    pass


def aplicar_acao(request):
    acao = request.POST['acao']
    controlador = ctrler.InstanciaJogo()
    if acao == "start_jogo":
        if controlador.get_estado_jogo() != ctrler.JG_EXECUTANDO:
            controlador.init_timer()
            request.session['nome_time'] = "Time 1"
    if acao == "stop_jogo":
        if controlador.get_estado_jogo() == ctrler.JG_EXECUTANDO:
            controlador.finalizar_jogo()
    if acao == "avancar_rodada":
        if controlador.get_estado_jogo() == ctrler.JG_EXECUTANDO:
            controlador.avancar_rodada()
    return HttpResponse("grrrr")


@ajax_sanitizer
def vender_modulo(request):
    controlador = ctrler.InstanciaJogo()
    nome_time = request.session['nome_time']
    print("Modulo Vendido")
    controlador.vender_modulo(nome_time, int(request.POST["modulo_id"]))
    return HttpResponse(controlador.get_caixa(nome_time))


@ajax_sanitizer
def comprar_modulo(request):
    controlador = ctrler.InstanciaJogo()
    nome_time = request.session['nome_time']
    print("Modulo comprado")
    estado, msg = controlador.comprar_modulo(nome_time, int(request.POST["modulo_id"]))
    if estado == 200:
        return HttpResponse(controlador.get_caixa(nome_time), status=200)
    else:
        return HttpResponse(msg, status=estado)


@ajax_sanitizer
def contratar_medico(request):
    nome_time = request.session['nome_time']
    controlador = ctrler.InstanciaJogo()
    print("Medico Contratado")
    controlador.contratar_medico(nome_time, int(request.POST["medico_id"]))
    return HttpResponse("contratado")


@ajax_sanitizer
def despedir_medico(request):
    nome_time = request.session['nome_time']
    controlador = ctrler.InstanciaJogo()

    controlador.despedir_medico(nome_time, int(request.POST["medico_id"]))
    print("despedido")
    return HttpResponse("despedido")


def abre_emprestimos(request):
    data = serializers.serialize("json", [Modulo.objects.get(id=request.POST["modulo_id"]), ])
    return HttpResponse(data)


@ajax_sanitizer
def tela_de_jogo_graficos(request):
    controlador = ctrler.InstanciaJogo()
    nome_time = request.session['nome_time']

    rodada = int(request.POST["rodada"])
    time = controlador.jogo_atual.times[nome_time]
    labels = list(time.estatisticas.lista_demandas[rodada].keys())
    total_atendidos = list(time.estatisticas.lista_total_atendidos[rodada].values())
    procuraram_atendimento = time.estatisticas.lista_demandas[rodada].values()
    demanda = []
    for i in procuraram_atendimento:
        demanda.append(sum(i.values()))
    labels_tabela = list(time.estatisticas.get_estatisticas().keys())
    dados_graf_pizza = controlador.get_dados_graf_pizza(nome_time, rodada)
    json = {
        "nome_time": time.nome,
        "labels": labels,
        "total_atendidos": total_atendidos,
        "procuraram_atendimento": demanda,
        "labels_tabela": labels_tabela,
        "dados_graf_pizza": dados_graf_pizza,
    }
    return JsonResponse(json)


@ajax_sanitizer
def tela_de_jogo_hospital_medicos(request):
    controlador = ctrler.InstanciaJogo()

    nome_time = request.session['nome_time']
    medicos = controlador.get_medicos(nome_time)
    contexto = {
        "medicos": medicos,
    }
    return render(request, 'jogo/hospital_medicos.html', contexto)


@ajax_sanitizer
def tela_de_jogo_hospital_modulos(request):
    nome_time = request.session['nome_time']
    controlador = ctrler.InstanciaJogo()
    areas, modulos_p_areas = controlador.get_modulos(nome_time)
    contexto = {
        "areas": areas,
        "mod_p_area": modulos_p_areas,
    }
    return render(request, 'jogo/hospital_modulos.html', contexto)
