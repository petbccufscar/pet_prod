from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse
import jogo.logica.logica_de_jogo as logica_jogo
from jogo.logica.time import Time as LTime

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
