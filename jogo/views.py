from django.shortcuts import render, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
# NAO ESQUEÇAM DE ATUALIZAR OS IMPORTS
from .models import Medico
from .forms import Medico_Form
from .models import Area, Area_Classe_Social
from .forms import Area_Form
from .models import Medico, Classe_Social
from .forms import Medico_Form, Classe_Social_Form, Area_Classe_Social_Form

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

#@login_required(login_url='/adm/login/')
def medico_new(request):
    medico = None
    try:
        medico = Medico.objects.latest('id')
    except:
        pass
    if medico == None:
        id = 1
    else:
        id = medico.id + 1

    if request.method == 'POST':
        form = Medico_Form(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/medico')
        else:
            return render(request, 'medico/medico_new.html', {'form':form, 'id':id})
    else:
        form = Medico_Form()
        return render(request, 'medico/medico_new.html', {'form': form, 'id':id})

#@login_required(login_url='/adm/login/')
def medico_edit(request, id):
    medico = get_object_or_404(Medico,pk=id)
    form = Medico_Form(instance=medico)

    if request.method == 'POST':
        form = Medico_Form(request.POST, instance=medico)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/medico')

    return render(request, 'medico/medico_edit.html', {'form':form, 'id':id})

#@login_required(login_url='/adm/login/')
def medico_delete(request, id):
    get_object_or_404(Medico, pk=id).delete()
    return HttpResponseRedirect('/medico')

# Views para Area e Area Classe Social
# Preciso do Classe Social para testar TODO mudar ClasseSocial para Classe_Social

def area_index(request):
    areas = Area.objects.order_by('id')
    area_classe = Area_Classe_Social.objects.order_by('id')
    print (areas)
    print (area_classe)
    return render(request, 'area/area_index.html', {'area_classe':area_classe,'areas':areas})

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
    get_object_or_404(Area, pk=id).delete()
    ##get_object_or_404(Area_ClasseSocial, pk=id).delete()
    return HttpResponseRedirect('/area')

def area_new(request):
    area = None
    try:
        area = Area.objects.latest('id')
    except:
        pass
    if area == None:
        id = 1
    else:
        id = area.id+1

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


# Views para classe social:

def classe_social_index(request):
    classes = Classe_Social.objects.order_by('id')
    return render(request, 'classe_social/classe_social_index.html', {'classes':classes})

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

def classe_social_new(request):
    classe = None
    try:
        classe = Classe_Social.objects.latest('id')
    except:
        pass
    if classe == None:
        id = 1
    else:
        id = classe.id+1
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