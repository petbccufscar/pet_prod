from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse  # utilizado apenas para teste
from django.shortcuts import get_object_or_404
from django.shortcuts import render, HttpResponseRedirect
from django.views.decorators.csrf import ensure_csrf_cookie

import jogo.logica.controlador as ctrler
import jogo.logica.logica_de_jogo as logica_jogo
from jogo.logica import time as timeClass
from jogo.logica import utils
from jogo.logica.time import Time as LTime
from .forms import AreaClasseSocialForm
from .forms import AreaForm
from .forms import ClasseSocialForm, MultiplicadorForm
from .forms import EmprestimoForm
from .forms import EventoForm
from .forms import MedicoForm
from .forms import ModuloForm
from .forms import Multiplicador
from .forms import RodadaForm
from .forms import TimeForm
from .models import Area
from .models import Area_Classe_Social
from .models import Classe_Social
from .models import Emprestimo
from .models import Evento
# NAO ESQUEÇAM DE ATUALIZAR OS IMPORTS
from .models import Medico, Modulo
from .models import Rodada
from .models import Time
from jogo.constants import *


# from django.core.exceptions import ObjectDoesNotExist

# views para home

@login_required(login_url='/login/')
def index(request):
    return render(request, TEMPLATE_JOGO_INDEX, {})


def base_configuracoes(request):
    return render(request, TEMPLATE_JOGO_BASE_CONFIGURACOES, {})


def base_aplicar_dinamica(request):
    return render(request, TEMPLATE_JOGO_BASE_APLICAR_DINAMICA, {})


def login(request):
    contexto = {}
    if request.method == 'POST':
        try:
            usuario = request.POST['usuario']
            senha = request.POST['senha']

            try:
                user = User.objects.get(username=usuario)

                if user.is_active:
                    usuario_autenticado = authenticate(username=usuario, password=senha)

                    if usuario_autenticado is not None:
                        django_login(request, usuario_autenticado)
                        return HttpResponseRedirect('/home/')
                    else:
                        contexto['erro'] = 'Usuário ou senha inválidos.'
                else:
                    contexto['erro'] = 'Usuário inativo.'
            except:
                contexto['erro'] = 'Usuário inexistente.'
        except:
            contexto['erro'] = 'Parâmetros inválidos.'

    return render(request, TEMPLATE_JOGO_LOGIN, contexto)


def logout(request):
    if request.user.is_authenticated:
        django_logout(request)

    return HttpResponseRedirect('/login/')


# Views para médico:

def medico_index(request):
    medicos = Medico.objects.order_by('perfil')
    return render(request, TEMPLATE_MEDICO_INDEX, {'medicos':medicos})


# TODO login_required
# @login_required(login_url='/adm/login/')
def medico_new(request):
    # medico = None
    # try:
    #     medico = Medico.objects.latest('id')
    # except:
    #     pass
    # if medico == None:
    #     id = 1
    # else:
    #     id = medico.id + 1

    if request.method == 'POST':
        form = MedicoForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/medico')
        else:
            return render(request, TEMPLATE_MEDICO_NEW, {'form':form})
    else:
        form = Medico_Form()
        return render(request, TEMPLATE_MEDICO_NEW, {'form': form})


# TODO login_required
# @login_required(login_url='/adm/login/')
def medico_edit(request, id):
    medico = get_object_or_404(Medico, id=id)
    form = MedicoForm(instance=medico)

    if request.method == 'POST':
        form = MedicoForm(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/medico')

    return render(request, TEMPLATE_MEDICO_EDIT, {'form':form, 'id':id})


# TODO login_required
# @login_required(login_url='/adm/login/')
def medico_delete(request, id):
    get_object_or_404(Medico, pk=id).delete()
    return HttpResponseRedirect('/medico')


# VIEWS PARA EVENTO
# VIEWS PARA EVENTO
def evento_index(request):
    eventos = Evento.objects.all()
    classes = Classe_Social.objects.all()
    mu = Multiplicador.objects.all()
    for m in mu:
        print(m.classeNome, " ", m.eventoNome, " ", m.valor, "\n")
    listaEventos = []
    for evento in eventos:
        event = []
        event.append(evento)
        mult = []
        for classe in classes:
            multiplicadores = Multiplicador.objects.get(eventoNome=evento.nome, classeNome=classe.nome)
            mult.append(multiplicadores)
        event.append(mult)
        listaEventos.append(event)
        print(listaEventos)
    return render(request, TEMPLATE_EVENTO_INDEX, {'eventos': eventos, 'classes': classes, 'listaEventos':listaEventos})


def evento_new(request):
    classes = Classe_Social.objects.all()
    if request.method == 'POST':
        form = EventoForm(request.POST)
        multiForm = []
        for classe in classes:
            mul = []
            mul.append(classe)
            m = MultiplicadorForm(request.POST)

            mul.append(m)
            multiForm.append(mul)

        if (form.is_valid()):
            form.save()

            for e, multi in multiForm:
                multiplicador = Multiplicador()
                multiplicador.valor = multi['valor'].value()
                multiplicador.eventoNome = form['nome'].value()
                multiplicador.classeNome = e.nome
                multiplicador.save()

                print(Multiplicador.objects.all())
            return HttpResponseRedirect('/evento')
        else:
            print(form.errors)
            return render(request, TEMPLATE_EVENTO_NEW, {'form': form, 'multiForm': multiForm})
    else:
        form = EventoForm()
        multiForm = []
        for classe in classes:
            mul = []
            mul.append(classe)
            m = MultiplicadorForm()
            mul.append(m)
            multiForm.append(mul)
        return render(request, TEMPLATE_EVENTO_NEW, {'form': form, 'multiForm': multiForm})


def evento_edit(request, id):
    evento = get_object_or_404(Evento, pk=id)
    eventoNome = get_object_or_404(Evento, pk=id).nome
    form = EventoForm(instance=evento)
    multiplicadores = Multiplicador.objects.all()
    classes = Classe_Social.objects.all()
    multiForm = []
    for classe in classes:
        for multiplicador in multiplicadores:
            mul = []
            if (multiplicador.classeNome == classe.nome and multiplicador.eventoNome == evento.nome):
                mul.append(classe)
                m = MultiplicadorForm(request.POST)
                mul.append(m)
                multiForm.append(mul)

    if request.method == 'POST':
        form = EventoForm(request.POST, instance=evento)

        for e, multi in multiForm:
            mul = Multiplicador.objects.filter(eventoNome=eventoNome, classeNome=e.nome)
            mul.update(valor=multi['valor'].value(), eventoNome=form['nome'].value())

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/evento')
    return render(request, TEMPLATE_EVENTO_EDIT, {'form': form, 'multiForm': multiForm})


def evento_delete(request, id):
    classes = Classe_Social.objects.all()
    evento = get_object_or_404(Evento, pk=id)
    for classe in classes:
        Multiplicador.objects.filter(eventoNome=evento.nome, classeNome=classe.nome).delete()
    get_object_or_404(Evento, pk=id).delete()
    return HttpResponseRedirect('/evento')


# Views para Rodada
def rodada_index(request):
    rodadas = Rodada.objects.order_by('numeroRodada')
    return render(request, TEMPLATE_RODADA_INDEX, {'rodadas':rodadas})


# Views para Area e Area Classe Social
# Preciso do Classe Social para testar TODO mudar ClasseSocial para Classe_Social

def rodada_new(request):
    if request.method == 'POST':
        form = RodadaForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/rodada')
        else:
            return render(request, TEMPLATE_RODADA_NEW, {'form': form})
    else:
        form = Rodada_Form()
        return render(request, TEMPLATE_RODADA_NEW, {'form': form})


# TODO login_required
# @login_required(login_url='/adm/login/')
def rodada_edit(request, id):
    rodada = get_object_or_404(Rodada, pk=id)
    form = RodadaForm(instance=rodada)

    if request.method == 'POST':
        form = RodadaForm(request.POST, instance=rodada)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/rodada')
    return render(request, TEMPLATE_RODADA_EDIT, {'form':form})


def rodada_delete(request, id):
    get_object_or_404(Rodada, id=id).delete()
    return HttpResponseRedirect('/rodada')


def area_index(request):
    areas = Area.objects.order_by('id')
    classes = Classe_Social.objects.all()
    classesNomes = []
    desvios_entradas_areas = []
    valores = []
    for c in classes:
        classesNomes.append("Desvio " + c.nome)
        classesNomes.append("Entrada " + c.nome)
    for area in areas:
        desvios_entradas = []
        valores = []
        for classe in classes:
            area_classe = Area_Classe_Social.objects.get(area=area.nome, classe_social=classe.nome)
            desvios_entradas.append(area_classe.desvios)
            desvios_entradas.append(area_classe.entrada)
        valores.append(area)
        valores.append(desvios_entradas)
        desvios_entradas_areas.append(valores)

    print (desvios_entradas_areas)
    return render(request, TEMPLATE_AREA_INDEX, {'desvios_entradas_areas': desvios_entradas_areas , 'classesNomes': classesNomes})


def area_new(request):
    if request.method == 'POST':

        form = AreaForm(request.POST)

        classes_sociais = Classe_Social.objects.order_by('id')

        list_entradas = request.POST.getlist('entrada')
        list_desvios = request.POST.getlist('desvios')
        request.POST = request.POST.copy()
        form_ac = []
        nomes = []
        for i in range(0, len(list_entradas)):
            form_area_classesocial = AreaClasseSocialForm(
                initial={'entrada': list_entradas[i], 'desvios': list_desvios[i]})
            form_ac.append(form_area_classesocial)
        classes_sociais = Classe_Social.objects.order_by('id')
        for a in classes_sociais:
            nomes.append(a.nome)
        list = zip(form_ac, nomes)
        if form.is_valid():
            for entrada in list_entradas:
                request.POST['entrada'] = entrada
                form_area_classesocial = AreaClasseSocialForm(request.POST)
                if not form_area_classesocial.is_valid():
                        #retorna o erro
                        return render(request, TEMPLATE_AREA_EDIT,
                                      {'form': form, 'id': id, 'classes_sociais': classes_sociais,
                                       'form_area_classesocial': form_area_classesocial,'list':list})
            for desvio in list_desvios:
                request.POST['desvios'] = desvio
                form_area_classesocial = AreaClasseSocialForm(request.POST)
                if not form_area_classesocial.is_valid():
                    # retorna o erro
                    return render(request, TEMPLATE_AREA_EDIT,
                                  {'form': form, 'id': id, 'classes_sociais': classes_sociais,
                                   'form_area_classesocial': form_area_classesocial, 'list': list})

            area = form.save()
            list_entradas = iter(list_entradas)
            list_desvios = iter(list_desvios)
            for classe in Classe_Social.objects.order_by('id'):
                area_classesocial = Area_Classe_Social(area=area.nome, classe_social=classe.nome,
                                                       entrada=next(list_entradas), desvios=next(list_desvios))
                area_classesocial.save()

            return HttpResponseRedirect('/area')
        else:
            #form_area_classesocial = Area_ClasseSocial_Form(request.POST)
            return render(request, TEMPLATE_AREA_EDIT,
                          {'form': form, 'id': id, 'classes_sociais': classes_sociais,
                           'form_area_classesocial': form_area_classesocial, 'list': list})
    else:
        form = AreaForm()
        classes_sociais = Classe_Social.objects.order_by('id')
        form_ac = []
        nomes = []
        for a in classes_sociais:
            form_area_classesocial = AreaClasseSocialForm()
            form_ac.append(form_area_classesocial)
            nomes.append(a.nome)
        list = zip(form_ac, nomes)
        return render(request, TEMPLATE_AREA_NEW,
                      {'form': form, 'id': id, 'classes_sociais': classes_sociais, 'list':list})


# TODO entender essa parte do codigo
def area_edit(request, id):
    area = get_object_or_404(Area, pk=id)

    if request.method == 'POST':
        form = AreaForm(request.POST, instance=area)
        classes_sociais = Classe_Social.objects.order_by('id')
        list_entradas = request.POST.getlist('entrada')
        list_desvios = request.POST.getlist('desvios')
        request.POST = request.POST.copy()
        form_ac = []
        nomes = []
        for a in classes_sociais:
            nomes.append(a.nome)
        list = zip(form_ac, nomes)
        for i in range(0, len(list_entradas)):
            form_area_classesocial = AreaClasseSocialForm(
                initial={'entrada': list_entradas[i], 'desvios': list_desvios[i]})
            form_ac.append(form_area_classesocial)
        if form.is_valid():

            for entrada in list_entradas:
                request.POST['entrada'] = entrada
                form_area_classesocial = AreaClasseSocialForm(request.POST)

                if not form_area_classesocial.is_valid():
                    # form_ac[iterador-1] = Area_ClasseSocial_Form(initial={'desvios': list_desvios[iterador-1]})
                    # retorna o erro em form_area_classesocial e valores em form_ac
                    return render(request, TEMPLATE_AREA_EDIT,
                                  {'form': form, 'id': id, 'classes_sociais': classes_sociais, 'form_area_classesocial': form_area_classesocial,'list':list})

            for desvio in list_desvios:
                request.POST['desvios'] = desvio
                form_area_classesocial = AreaClasseSocialForm(request.POST)

                if not form_area_classesocial.is_valid():
                    # retorna o erro
                    #form_ac[iterador - 1] = Area_ClasseSocial_Form(initial={'entrada': list_entradas[iterador - 1]})
                    return render(request, TEMPLATE_AREA_EDIT,
                                  {'form': form, 'id': id, 'classes_sociais': classes_sociais,
                                   'form_area_classesocial': form_area_classesocial, 'list': list})

            get_object_or_404(Area, pk=id).delete()
            area = form.save()
            list_entradas = iter(list_entradas)
            list_desvios = iter(list_desvios)
            for classe in Classe_Social.objects.order_by('id'):
                area_classesocial = Area_Classe_Social.objects.get(area=area.nome, classe_social=classe.nome)
                area_classesocial.entrada = next(list_entradas)
                area_classesocial.desvios = next(list_desvios)
                area_classesocial.save()

            return HttpResponseRedirect('/area')
        else:
            return render(request, TEMPLATE_AREA_EDIT,
                          {'form': form, 'id': id, 'classes_sociais': classes_sociais,
                           'form_area_classesocial': form_area_classesocial, 'list': list})

    form = AreaForm(instance=area)
    area_classes = Area_Classe_Social.objects.all()
    form_ac = []
    nomes = []
    for a in area_classes:
        if a.area == area.nome:
            form_area_classesocial = AreaClasseSocialForm(instance=a)
            form_ac.append(form_area_classesocial)

    classes_sociais = Classe_Social.objects.order_by('id')
    for a in classes_sociais:
        nomes.append(a.nome)
    list = zip(form_ac, nomes)
    return render(request, TEMPLATE_AREA_EDIT, {'form': form, 'id': id, 'classes_sociais':classes_sociais,'list':list})


def area_delete(request, id):
    get_object_or_404(Area, id=id).delete()
    ##get_object_or_404(Area_ClasseSocial, pk=id).delete()
    return HttpResponseRedirect('/area')


# VIEWS PARA TIME
def time_index(request):
    times = Time.objects.order_by('id')
    return render(request, TEMPLATE_TIME_INDEX, {'times': times})


# @login_required(login_url='/adm/login')
def time_new(request):
    if request.method == 'POST':
        form = TimeForm(request.POST)
        if form.is_valid():
            repetesenha = form.cleaned_data['repetesenha']
            senha = form.cleaned_data['senha']
            if (repetesenha == senha):
                form.save()
                return HttpResponseRedirect('/time')
            else:
                return render(request, TEMPLATE_TIME_NEW, {'form': form, 'id': id})
        else:
            return render(request, TEMPLATE_TIME_NEW, {'form': form, 'id': id})
    else:
        form = Time_Form()
        return render(request, TEMPLATE_TIME_NEW, {'form': form, 'id': id})


# @login_required(login_url='/adm/login/')
def time_edit(request, id):
    time = get_object_or_404(Time, pk=id)
    form = TimeForm(instance=time)

    if request.method == 'POST':
        form = TimeForm(request.POST, instance=time)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/time')

    return render(request, TEMPLATE_TIME_EDIT, {'form':form, 'id':id})


# @login_required(login_url='/adm/login/')
def time_delete(request, id):
    get_object_or_404(Time, pk=id).delete()
    return HttpResponseRedirect('/time')


# Views para empréstimo:
def emprestimo_index(request):
    emprestimos = Emprestimo.objects.order_by('valor')
    return render(request, TEMPLATE_EMPRESTIMO_INDEX, {'emprestimos':emprestimos})


def emprestimo_new(request):
    if request.method == 'POST':
        form = EmprestimoForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/emprestimo')
        else:
            return render(request, TEMPLATE_EMPRESTIMO_NEW, {'form': form})
    else:
        form = Emprestimo_Form()
        return render(request, TEMPLATE_EMPRESTIMO_NEW, {'form': form})
#@login_required(login_url='/adm/login/')


# @login_required(login_url='/adm/login/')

def emprestimo_edit(request, id):
    emprestimo = get_object_or_404(Emprestimo, pk=id)
    form = EmprestimoForm(instance=emprestimo)

    if request.method == 'POST':
        form = EmprestimoForm(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/emprestimo')

    return render(request, TEMPLATE_EMPRESTIMO_EDIT, {'form': form})


def emprestimo_delete(request, id):
    get_object_or_404(Emprestimo, pk=id).delete()
    return HttpResponseRedirect('/emprestimo')


def classe_social_index(request):
    classes = Classe_Social.objects.order_by('id')
    return render(request, TEMPLATE_CLASSESOCIAL_INDEX, {'classes':classes})


def classe_social_new(request):
    if request.method == 'POST':
        print(request.POST)
        form = ClasseSocialForm(request.POST)
        eventos = Evento.objects.all()
        areas = Area.objects.all()
        if form.is_valid():
            for evento in eventos:
                multiplicador = Multiplicador()
                multiplicador.valor = 0.1
                multiplicador.eventoNome = evento.nome
                multiplicador.classeNome = form['nome'].value()
                multiplicador.save()
            for area in areas:
                area_classe = Area_Classe_Social()
                area_classe.area = area.nome
                area_classe.classe_social = form['nome'].value()
                area_classe.entrada = 1
                area_classe.desvios = 0
                area_classe.save()
            form.save()
            return HttpResponseRedirect('/classe_social')
        else:
            return render(request, TEMPLATE_CLASSESOCIAL_NEW, {'form': form, 'id': id})
    else:
        form = Classe_Social_Form()
        return render(request, TEMPLATE_CLASSESOCIAL_NEW, {'form': form, 'id': id})


def classe_social_edit(request, id):
    classe = get_object_or_404(Classe_Social, pk=id)
    form = ClasseSocialForm(instance=classe)
    nomeClasse = ClasseSocialForm(instance=classe)['nome'].value()
    eventos = Evento.objects.all()
    areas = Area.objects.all()
    if request.method == 'POST':
        form = ClasseSocialForm(request.POST, instance=classe)
        if form.is_valid():
            for evento in eventos:
                multi = Multiplicador.objects.filter(eventoNome=evento.nome, classeNome=nomeClasse)
                multi.update(classeNome=form['nome'].value())
            form.save()
            for area in areas:
                multi = Area_Classe_Social.objects.filter(area=area.nome, classe_social=nomeClasse)
                multi.update(classe_social=form['nome'].value())
            return HttpResponseRedirect('/classe_social')

    return render(request, TEMPLATE_CLASSESOCIAL_EDIT, {'form': form, 'id': id})


def classe_social_delete(request, id):
    eventos = Evento.objects.all()
    classe = get_object_or_404(Classe_Social, pk=id)
    for evento in eventos:
        Multiplicador.objects.filter(eventoNome=evento.nome, classeNome=classe.nome).delete()
    get_object_or_404(Classe_Social, pk=id).delete()
    return HttpResponseRedirect('/classe_social')


def modulo_index(request):
    modulos = Modulo.objects.order_by('codigo')
    return render(request, TEMPLATE_MODULO_INDEX, {'modulos':modulos})


# @login_required(login_url='/adm/login/')
def modulo_new(request):
    if request.method == 'POST':
        form = ModuloForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/modulo')
        else:
            return render(request, TEMPLATE_MODULO_NEW, {'form': form, 'id': id})
    else:
        form = Modulo_Form()
        return render(request, TEMPLATE_MODULO_NEW, {'form': form, 'id': id})


# @login_required(login_url='/adm/login/')
def modulo_edit(request, id):
    modulo = get_object_or_404(Modulo, pk=id)
    form = ModuloForm(instance=modulo)

    if request.method == 'POST':
        form = ModuloForm(request.POST, instance=modulo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/modulo')

    return render(request, TEMPLATE_MODULO_EDIT, {'form': form, 'id': id})


# @login_required(login_url='/adm/login/')
def modulo_delete(request, id):
    # get_object_or_404(Modulo, pk=id).delete()
    Modulo.objects.get(id=id).delete()
    return HttpResponseRedirect('/modulo')


def iniciar_jogo(request):
    # TODO: codigo de inicialização de jogo
    rodadas = Rodada.objects.all()
    times = []  # TODO: inicializar times
    # times hardcoded para fins de teste
    timesCadastrados = Time.objects.order_by(id)
    for t in timesCadastrados:
        times.append(LTime(t.nome))
        tokens = utils.gerar_token(1)
        times[-1].codigo_login = tokens[-1]
        print("codigo: ", times[-1].codigo_login)
        request.session['nome_time'] = t.nome
    print(request.session['nome_time'])
    logica_jogo.inicializa_jogo(rodadas, times)
    return HttpResponse("Iniciou")


@ensure_csrf_cookie
def tela_aplicar_dinamica(request):
    ctrler.__inicializa_jogo()
    controlador = ctrler.InstanciaJogo()

    times = controlador.jogo_atual.times
    contexto = {
        "times": [{"nome": x.nome, "codigo": x.codigo_login} for x in times.values()]
    }
    request.session['nome_time'] = {}
    for x in times.values():
        request.session['nome_time'] = x.nome
    print(request.session['nome_time'])
    return render(request, TEMPLATE_JOGO_BASE_APLICAR_DINAMICA, contexto)


@ensure_csrf_cookie
def tela_de_jogo(request):
    controlador = ctrler.InstanciaJogo()

    if controlador.get_estado_jogo() == ctrler.JG_NAO_INICIADO:
        return HttpResponse("Jogo Ainda não comecou")

    if 'nome_time' not in request.session:
        return HttpResponseRedirect("/jogo/")

    if controlador.get_estado_jogo() == ctrler.JG_PRONTO:
        return render(request, TEMPLATE_JOGO_NAO_INICIADO)

    if controlador.get_estado_jogo() == ctrler.JG_FINALIZADO:
        return HttpResponseRedirect("/jogo/ranking")

    nome_time = request.session['nome_time']
    time = timeClass.Time(nome_time)
    modulos_p_areas = {}

    labels = time.estatisticas.lista_demandas[0].keys()
    total_atendidos = time.estatisticas.lista_total_atendidos[0].values()
    procuraram_atendimento = time.estatisticas.lista_demandas[0].values()

    aux = []
    for i in procuraram_atendimento:
        aux.append(sum(i.values()))

    labels_tabela = time.estatisticas.get_estatisticas().keys()

    medicos = controlador.get_medicos()
    areas, modulos_p_areas = controlador.get_modulos()
    contexto = {
        "areas": areas,
        "mod_p_area": modulos_p_areas,
        "nome_time": time.nome,
        "medicos": medicos,
        "caixa": time.estatisticas.get_ultimo_caixa(),
        "labels": labels,
        "total_atendidos": total_atendidos,
        "procuraram_atendimento": aux,
        "labels_tabela": labels_tabela,
        "estatisticas": time.estatisticas.get_estatisticas(),
        "rodada_atual": controlador.jogo_atual.rodada_atual + 1,
        "rodadas_ate_atual":range(0,controlador.jogo_atual.rodada_atual),
        "rodadas": range(1,len(controlador.jogo_atual.rodadas)+2),
        }
    return render(request, TEMPLATE_JOGO_TELA_DE_JOGO, contexto)


def tela_de_jogo_hospital(request):
    if logica_jogo.JogoAtual is None:
        return HttpResponse("Jogo Não Iniciado")
    if 'nome_time' not in request.session:
        return HttpResponse("Usuário Não Logado")

    nome_time = request.session['nome_time']

    time = logica_jogo.JogoAtual.times[nome_time]
    # Separando modulos por area
    time_modulos_p_areas = {}
    medicos = []
    time = logica_jogo.JogoAtual.times[nome_time];
    for id_med in time.medicos:
        medico = Medico.objects.get(id=id_med)
        medicos.append(medico)
        medico.salario = "{:,.2f}".format(medico.salario)
        medico.expertise = range(0, medico.expertise)
        medico.atendimento = range(0, medico.atendimento)
        medico.pontualidade = range(0, medico.pontualidade)

    for id_mod in time.modulos:
        modulo = Modulo.objects.get(id=id_mod)
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
        "t_mod_p_area": time_modulos_p_areas,
        "medicos": medicos,
    }
    return render(request, TEMPLATE_JOGO_MEU_HOSPITAL, contexto)


def tela_de_jogo_dashboard(request):
    controlador = ctrler.InstanciaJogo()
    nome_time = request.session['nome_time']
    time = controlador.jogo_atual.times[nome_time]
    labels = time.estatisticas.lista_demandas[0].keys()
    total_atendidos = time.estatisticas.lista_total_atendidos[0].values()
    procuraram_atendimento = time.estatisticas.lista_demandas[0].values()

    aux = []
    for i in procuraram_atendimento:
        aux.append(sum(i.values()))

    labels_tabela = time.estatisticas.get_estatisticas().keys()

    contexto = {
        "nome_time": time.nome,
        "labels": labels,
        "total_atendidos": total_atendidos,
        "procuraram_atendimento": aux,
        "labels_tabela": labels_tabela,
        "estatisticas": time.estatisticas.get_estatisticas(),
        "rodadas": range(1,len(controlador.jogo_atual.rodadas)+2),
        }
    return render(request, TEMPLATE_JOGO_DASHBOARD, contexto)


def pre_jogo_1(request):
    return render(request, TEMPLATE_PREJOGO_1,{})


def pre_jogo_2(request):
    return render(request, TEMPLATE_PREJOGO_2,{})


def pre_jogo_3(request):
    return render(request, TEMPLATE_PREJOGO_3,{})


def pre_jogo_4(request):
    return render(request, TEMPLATE_PREJOGO_4,{})


def pre_jogo_5(request):
    return render(request, TEMPLATE_PREJOGO_5,{})


def logar(request):
    print(request.POST["senha"])
    controlador = ctrler.InstanciaJogo()
    if controlador.get_estado_jogo() == ctrler.JG_NAO_INICIADO:
        return HttpResponse("Login Falhou: jogo não inicializado")

    if controlador.get_estado_jogo() == ctrler.JG_NAO_INICIADO:
        return HttpResponse("Login Falhou: jogo não inicializado")
    logado = False
    for time in controlador.jogo_atual.times.values():
        print("Tenho codigo login: ", time.codigo_login)
        print("Tenho request senha: ", request.POST["senha"])
        if time.codigo_login == request.POST["senha"]:
            # request.session.clear()
            logado = True
            request.session['nome_time'] = time.nome
    if logado:
        return HttpResponseRedirect('/jogo/')
    else:
        return HttpResponse("Login Falhou: token inexistente")


def login_jogador(request):
    return render(request, TEMPLATE_JOGO_LOGIN_JOGADOR,{})


def jogo_ranking(request):
    controlador = ctrler.InstanciaJogo()
    if controlador.get_estado_jogo() != ctrler.JG_FINALIZADO:
        return HttpResponse("Não há jogo Finalizado")
    scores = controlador.pontuacao()
    return render(request, TEMPLATE_JOGO_RANKING, {"scores": scores})
