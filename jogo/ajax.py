from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
import jogo.logica.logica_de_jogo as logica_jogo
from jogo.logica.time import Time as LTime
from jogo.models import Medico
from jogo.models import Modulo

def tela_de_jogo_graficos(request):
    if logica_jogo.JogoAtual is None:
        return HttpResponse("Jogo Não Iniciado")
    if 'nome_time' not in request.session:
        return HttpResponse("Usuário Não Logado")

    nome_time = request.session['nome_time']

    rodada = int(request.POST["rodada"])
    time = logica_jogo.JogoAtual.times[nome_time]
    labels = list(time.estatisticas.lista_demandas[rodada].keys())
    total_atendidos = list(time.estatisticas.lista_total_atendidos[rodada].values())
    procuraram_atendimento = time.estatisticas.lista_demandas[rodada].values()
    demanda = []
    for i in procuraram_atendimento:
        demanda.append(sum(i.values()))
    labels_tabela = list(time.estatisticas.get_estatisticas().keys())
    json = {
        "nome_time": time.nome,
        "labels": labels,
        "total_atendidos": total_atendidos,
        "procuraram_atendimento": demanda,
        "labels_tabela": labels_tabela,
        }
    return JsonResponse(json)

def tela_de_jogo_hospital_medicos(request):
    if logica_jogo.JogoAtual is None:
        return HttpResponse("Jogo Não Iniciado")
    if 'nome_time' not in request.session:
        return HttpResponse("Usuário Não Logado")

    nome_time = request.session['nome_time']

    time = logica_jogo.JogoAtual.times[nome_time]
    medicos = []
    time = logica_jogo.JogoAtual.times[nome_time];
    for id_med in time.medicos:
        medico = Medico.objects.get(id = id_med)
        medicos.append(medico)
        medico.salario =  "{:,.2f}".format(medico.salario)
        medico.expertise = range(0, medico.expertise)
        medico.atendimento = range(0, medico.atendimento)
        medico.pontualidade = range(0, medico.pontualidade)

    contexto = {
        "medicos": medicos,
    }
    return render(request, 'jogo/hospital_medicos.html', contexto)

def tela_de_jogo_hospital_modulos(request):
    if logica_jogo.JogoAtual is None:
        return HttpResponse("Jogo Não Iniciado")
    if 'nome_time' not in request.session:
        return HttpResponse("Usuário Não Logado")

    nome_time = request.session['nome_time']
    time = logica_jogo.JogoAtual.times[nome_time]
    # Separando modulos por area
    time_modulos_p_areas = {}
    for id_mod in time.modulos:
        modulo = Modulo.objects.get(id = id_mod)
        if modulo.area.nome in time_modulos_p_areas:
            time_modulos_p_areas[modulo.area.nome].append(modulo)
        else:
            time_modulos_p_areas[modulo.area.nome] = [modulo]

        modulo.custo_de_aquisicao = "{:,.2f}".format(modulo.custo_de_aquisicao)
        modulo.custo_mensal = "{:,.0f}".format(modulo.custo_mensal)
        modulo.preco_do_tratamento = "{:,.0f}".format(modulo.preco_do_tratamento)
        modulo.tecnologia = range(0, modulo.tecnologia)
        modulo.conforto = range(0, modulo.conforto)
    contexto = {
        "areas": list(time_modulos_p_areas.keys()),
        "mod_p_area": time_modulos_p_areas,
    }
    return render(request, 'jogo/hospital_modulos.html', contexto)
