from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse #utilizado apenas para teste
# NAO ESQUEÇAM DE ATUALIZAR OS IMPORTS
from .models import Medico, Modulo
from .models import Evento
from .forms import Medico_Form
from .forms import Evento_Form
from .models import Emprestimo
from .forms import Emprestimo_Form
from .models import Time
from .forms import Time_Form
from .models import Area, Area_Classe_Social
from .forms import Area_Form
from .models import Classe_Social
from .forms import Classe_Social_Form
from .models import Rodada
from .forms import Rodada_Form
from .forms import Modulo_Form
from .forms import Area_Classe_Social_Form

import jogo.logica.logica_de_jogo as logica_jogo
from jogo.logica.time import Time as LTime

# from django.core.exceptions import ObjectDoesNotExist

# views para home

@login_required(login_url='/login/')
def index(request):
    return render(request, 'jogo/index.html', {})


def base_configuracoes(request):
    return render(request, 'jogo/base_configuracoes.html', {})


def base_aplicar_dinamica(request):
    return render(request, 'jogo/base_aplicar_dinamica.html', {})


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

    return render(request, 'jogo/login.html', contexto)


def logout(request):
    if request.user.is_authenticated:
        django_logout(request)

    return HttpResponseRedirect('/login/')



# Views para médico:

def medico_index(request):
    medicos = Medico.objects.order_by('perfil')
    return render(request, 'medico/medico_index.html', {'medicos':medicos})

# TODO login_required
#@login_required(login_url='/adm/login/')
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
        form = Medico_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/medico')
        else:
            return render(request, 'medico/medico_new.html', {'form':form})
    else:
        form = Medico_Form()
        return render(request, 'medico/medico_new.html', {'form': form})

# TODO login_required
#@login_required(login_url='/adm/login/')
def medico_edit(request, id):
    medico = get_object_or_404(Medico,id=id)
    form = Medico_Form(instance=medico)

    if request.method == 'POST':
        form = Medico_Form(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/medico')

    return render(request, 'medico/medico_edit.html', {'form':form, 'id':id})

# TODO login_required
#@login_required(login_url='/adm/login/')
def medico_delete(request, id):
    get_object_or_404(Medico, pk=id).delete()
    return HttpResponseRedirect('/medico')


# VIEWS PARA EVENTO
def evento_index(request):
    eventos = Evento.objects.all()
    print(eventos)
    return render(request, 'evento/evento_index.html', {'eventos': eventos})

def evento_new(request):
    if request.method == 'POST':
        form = Evento_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/evento')
        else:
            return render(request, 'evento/evento_new.html', {'form': form})
    else:
        form = Evento_Form()
        return render(request, 'evento/evento_new.html', {'form': form})


def evento_edit(request, id):
    evento = get_object_or_404(Evento, pk=id)
    form = Evento_Form(instance=evento)

    if request.method == 'POST':
        form = Evento_Form(request.POST, instance=evento)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/evento')
    return render(request, 'evento/evento_edit.html', {'form': form})

def evento_delete(request, id):
    get_object_or_404(Evento, pk=id).delete()
    return HttpResponseRedirect('/evento')

# Views para Rodada
def rodada_index(request):
    rodadas = Rodada.objects.order_by('numeroRodada')
    return render(request, 'rodada/rodada_index.html', {'rodadas':rodadas})
# Views para Area e Area Classe Social
# Preciso do Classe Social para testar TODO mudar ClasseSocial para Classe_Social

def rodada_new(request):
    if request.method == 'POST':
        form = Rodada_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/rodada')
        else:
            return render(request, 'rodada/rodada_new.html', {'form': form})
    else:
        form = Rodada_Form()
        return render(request, 'rodada/rodada_new.html', {'form': form})

# TODO login_required
#@login_required(login_url='/adm/login/')
def rodada_edit(request, id):
    rodada = get_object_or_404(Rodada,pk=id)
    form = Rodada_Form(instance=rodada)

    if request.method == 'POST':
        form = Rodada_Form(request.POST, instance=rodada)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/rodada')
    return render(request, 'rodada/rodada_edit.html', {'form':form})


def rodada_delete(request, id):
    #TODO IMPLEMENTAR DELETE DE RODADA
    pass

def area_index(request):
    areas = Area.objects.order_by('id')
    area_classe = Area_Classe_Social.objects.order_by('id')
    print (areas)
    print (area_classe)
    return render(request, 'area/area_index.html', {'area_classe':area_classe,'areas':areas})

def area_new(request):
    if request.method == 'POST':

        form = Area_Form(request.POST)

        classes_sociais = Classe_Social.objects.order_by('id')


        list_entradas = request.POST.getlist('entrada')
        list_desvios =  request.POST.getlist('desvios')
        request.POST = request.POST.copy()
        form_ac = []
        nomes = []
        for i in range(0, len(list_entradas)):
            form_area_classesocial = Area_Classe_Social_Form(
                    initial={'entrada': list_entradas[i], 'desvios': list_desvios[i]})
            form_ac.append(form_area_classesocial)
        classes_sociais = Classe_Social.objects.order_by('id')
        for a in classes_sociais:
            nomes.append(a.nome)
        list = zip(form_ac, nomes)
        if form.is_valid():
            for entrada in list_entradas:
                request.POST['entrada'] = entrada
                form_area_classesocial = Area_Classe_Social_Form(request.POST)
                if not form_area_classesocial.is_valid():
                        #retorna o erro
                        return render(request, 'area/area_edit.html',
                                      {'form': form, 'id': id, 'classes_sociais': classes_sociais,
                                       'form_area_classesocial': form_area_classesocial,'list':list})
            for desvio in list_desvios:
                request.POST['desvios'] = desvio
                form_area_classesocial = Area_Classe_Social_Form(request.POST)
                if not form_area_classesocial.is_valid():
                    # retorna o erro
                    return render(request, 'area/area_edit.html',
                                  {'form': form, 'id': id, 'classes_sociais': classes_sociais,
                                   'form_area_classesocial': form_area_classesocial,'list':list})

            area = form.save()
            list_entradas = iter(list_entradas)
            list_desvios = iter(list_desvios)
            for classe in Classe_Social.objects.order_by('id'):
                area_classesocial = Area_Classe_Social(area=area,classe_social=classe,entrada=next(list_entradas),desvios=next(list_desvios))
                area_classesocial.save()

            return HttpResponseRedirect('/area')
        else:
            #form_area_classesocial = Area_ClasseSocial_Form(request.POST)
            return render(request, 'area/area_edit.html',
                          {'form': form, 'id': id, 'classes_sociais': classes_sociais,
                           'form_area_classesocial': form_area_classesocial,'list':list})
    else:
        form = Area_Form()
        classes_sociais = Classe_Social.objects.order_by('id')
        form_ac = []
        nomes = []
        for a in classes_sociais:
            form_area_classesocial = Area_Classe_Social_Form()
            form_ac.append(form_area_classesocial)
            nomes.append(a.nome)
        list = zip(form_ac, nomes)
        return render(request, 'area/area_new.html',
                      {'form': form, 'id': id, 'classes_sociais': classes_sociais, 'list':list})



# TODO entender essa parte do codigo
def area_edit(request, id):
    area = get_object_or_404(Area, pk=id)

    if request.method == 'POST':
        form = Area_Form(request.POST, instance=area)
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
            form_area_classesocial = Area_Classe_Social_Form(
                initial={'entrada': list_entradas[i], 'desvios': list_desvios[i]})
            form_ac.append(form_area_classesocial)
        if form.is_valid():

            for entrada in list_entradas:
                request.POST['entrada'] = entrada
                form_area_classesocial = Area_Classe_Social_Form(request.POST)

                if not form_area_classesocial.is_valid():
                    #form_ac[iterador-1] = Area_ClasseSocial_Form(initial={'desvios': list_desvios[iterador-1]})
                    # retorna o erro em form_area_classesocial e valores em form_ac
                    return render(request, 'area/area_edit.html',
                                  {'form': form, 'id': id, 'classes_sociais': classes_sociais, 'form_area_classesocial': form_area_classesocial,'list':list})


            for desvio in list_desvios:
                request.POST['desvios'] = desvio
                form_area_classesocial = Area_Classe_Social_Form(request.POST)

                if not form_area_classesocial.is_valid():
                    # retorna o erro
                    #form_ac[iterador - 1] = Area_ClasseSocial_Form(initial={'entrada': list_entradas[iterador - 1]})
                    return render(request, 'area/area_edit.html',
                                  {'form': form, 'id': id, 'classes_sociais': classes_sociais,
                                   'form_area_classesocial': form_area_classesocial,'list':list})

            get_object_or_404(Area, pk=id).delete()
            area = form.save()
            list_entradas = iter(list_entradas)
            list_desvios = iter(list_desvios)
            for classe in Classe_Social.objects.order_by('id'):
                area_classesocial = Area_Classe_Social(area = area, classe_social=classe, entrada=next(list_entradas), desvios=next(list_desvios))
                area_classesocial.save()

            return HttpResponseRedirect('/area')
        else:
            return render(request, 'area/area_edit.html',
                          {'form': form, 'id': id, 'classes_sociais': classes_sociais,
                           'form_area_classesocial': form_area_classesocial,'list':list})

    form = Area_Form(instance=area)
    area_classe = Area_Classe_Social.objects.order_by('id')
    form_ac = []
    nomes = []
    for a in area_classe:
        if a.area_id == int(id):
            form_area_classesocial =  Area_Classe_Social_Form(instance=a)
            form_ac.append(form_area_classesocial)


    classes_sociais = Classe_Social.objects.order_by('id')
    for a in classes_sociais:
        nomes.append(a.nome)
    list = zip(form_ac, nomes)
    return render(request, 'area/area_edit.html', {'form': form, 'id': id, 'classes_sociais':classes_sociais,'list':list})

def area_delete(request, id):
    get_object_or_404(Area, id = id).delete()
    ##get_object_or_404(Area_ClasseSocial, pk=id).delete()
    return HttpResponseRedirect('/area')



#VIEWS PARA TIME
def time_index(request):
    times = Time.objects.order_by('id')
    return render(request, 'time/time_index.html', {'times': times})

#@login_required(login_url='/adm/login')
def time_new(request):
    if request.method == 'POST':
        form = Time_Form(request.POST)
        if form.is_valid():
            repetesenha =  form.cleaned_data['repetesenha']
            senha = form.cleaned_data['senha']
            if(repetesenha == senha):
                form.save()
                return HttpResponseRedirect('/time')
            else:
                return render(request, 'time/time_new.html', {'form': form, 'id': id})
        else:
            return render(request, 'time/time_new.html', {'form': form, 'id': id})
    else:
        form = Time_Form()
        return render(request, 'time/time_new.html', {'form': form, 'id': id})

#@login_required(login_url='/adm/login/')
def time_edit(request, id):
    time = get_object_or_404(Time,pk=id)
    form = Time_Form(instance=time)

    if request.method == 'POST':
        form = Time_Form(request.POST, instance=time)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/time')

    return render(request, 'time/time_edit.html', {'form':form, 'id':id})

#@login_required(login_url='/adm/login/')
def time_delete(request, id):
    get_object_or_404(Time, pk=id).delete()
    return HttpResponseRedirect('/time')


# Views para empréstimo:
def emprestimo_index(request):
    emprestimos = Emprestimo.objects.order_by('valor')
    return render(request, 'emprestimo/emprestimo_index.html', {'emprestimos':emprestimos})

def emprestimo_new(request):
    if request.method == 'POST':
        form = Emprestimo_Form(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/emprestimo')
        else:
            return render(request, 'emprestimo/emprestimo_new.html', {'form': form})
    else:
        form = Emprestimo_Form()
        return render(request, 'emprestimo/emprestimo_new.html', {'form': form})
#@login_required(login_url='/adm/login/')

def emprestimo_edit(request, id):
    emprestimo = get_object_or_404(Emprestimo, pk=id)
    form = Emprestimo_Form(instance=emprestimo)

    if request.method == 'POST':
        form = Emprestimo_Form(request.POST, instance=emprestimo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/emprestimo')

    return render(request, 'emprestimo/emprestimo_edit.html', {'form': form})

def emprestimo_delete(request, id):
    get_object_or_404(Emprestimo, pk=id).delete()
    return HttpResponseRedirect('/emprestimo')


#Views para Classe Social
def classe_social_index(request):
    classes = Classe_Social.objects.order_by('id')
    return render(request, 'classe_social/classe_social_index.html', {'classes':classes})

def classe_social_new(request):
    if request.method == 'POST':
        print(request.POST)
        form = Classe_Social_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/classe_social')
        else:
            return render(request, 'classe_social/classe_social_new.html', {'form': form, 'id': id})
    else:
        form = Classe_Social_Form()
        return render(request, 'classe_social/classe_social_new.html', {'form': form, 'id': id})

def classe_social_edit(request, id):
    classe = get_object_or_404(Classe_Social, pk=id)
    form = Classe_Social_Form(instance=classe)

    if request.method == 'POST':
        form = Classe_Social_Form(request.POST, instance=classe)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/classe_social')

    return render(request, 'classe_social/classe_social_edit.html', {'form': form, 'id': id})

def classe_social_delete(request, id):
    get_object_or_404(Classe_Social, pk=id).delete()
    return HttpResponseRedirect('/classe_social')



def modulo_index(request):
    modulos = Modulo.objects.order_by('codigo')
    return render(request, 'modulo/modulo_index.html', {'modulos':modulos})

#@login_required(login_url='/adm/login/')
def modulo_new(request):
    if request.method == 'POST':
        form = Modulo_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/modulo')
        else:
            return render(request, 'modulo/modulo_new.html', {'form': form, 'id': id})
    else:
        form = Modulo_Form()
        return render(request, 'modulo/modulo_new.html', {'form': form, 'id': id})


#@login_required(login_url='/adm/login/')
def modulo_edit(request, id):
    modulo = get_object_or_404(Modulo, pk=id)
    form = Modulo_Form(instance=modulo)

    if request.method == 'POST':
        form = Modulo_Form(request.POST, instance=modulo)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/modulo')

    return render(request, 'modulo/modulo_edit.html', {'form': form, 'id': id})

#@login_required(login_url='/adm/login/')
def modulo_delete(request, id):
    #get_object_or_404(Modulo, pk=id).delete()
    Modulo.objects.get(id=id).delete()
    return HttpResponseRedirect('/modulo')

def iniciar_jogo(request):
    #TODO: codigo de inicialização de jogo
    rodadas = Rodada.objects.all()
    times = [] #TODO: inicializar times
    #times hardcoded para fins de teste
    times.append(LTime("time1"))
    times.append(LTime("time2"))
    times.append(LTime("time3"))
    logica_jogo.inicializa_jogo(rodadas, times)
    return HttpResponse("Iniciou")

def tela_de_jogo(request, nome_time):
    if logica_jogo.JogoAtual is None:
        return HttpResponse("Jogo Não Iniciado")
    time = logica_jogo.JogoAtual.times[nome_time]
    return render(request, 'jogo/tela_de_jogo.html', {"nome_time": time.nome})

def pre_jogo_1(request):
    return render(request, 'pre_jogo/tela_pre_jogo_1.html',{})

def pre_jogo_2(request):
    return render(request, 'pre_jogo/tela_pre_jogo_2.html',{})

def pre_jogo_3(request):
    return render(request, 'pre_jogo/tela_pre_jogo_3.html',{})

def pre_jogo_4(request):
    return render(request, 'pre_jogo/tela_pre_jogo_4.html',{})

def pre_jogo_5(request):
    return render(request, 'pre_jogo/tela_pre_jogo_5.html',{})
