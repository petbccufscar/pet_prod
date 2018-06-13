from django.conf.urls import url
from jogo import views
from django.urls import path
from jogo import ajax
app_name = 'jogo'
urlpatterns = [
    # URLs para home
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.index, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^base_configuracoes/$', views.base_configuracoes, name='base_configuracoes'),
    url(r'^aplicar_dinamica/aplicar_acao/$', ajax.aplicar_acao, name='aplicar_acao'),
    url(r'^aplicar_dinamica/$', views.tela_aplicar_dinamica, name='base_aplicar_dinamica'),
    # Cuidado com as URLS!
    # Como estamos utilizando apenas um app, temos que colocar o class/xxx
    url(r'^medico/$', views.medico_index, name='medico_index'),
    url(r'^medico/edit/(?P<id>\d+)/$', views.medico_edit, name='medico_edit'),
    url(r'^medico/delete/(?P<id>\d+)/$', views.medico_delete, name='medico_delete'),
    url(r'^medico/new/$', views.medico_new, name='medico_new'),
    url(r'^evento/$', views.evento_index, name='evento_index'),
    url(r'^evento/edit/(?P<id>\d+)/$', views.evento_edit, name='evento_edit'),
    url(r'^evento/delete/(?P<id>\d+)/$', views.evento_delete, name='evento_delete'),
    url(r'^evento/new/$', views.evento_new, name='evento_new'),
    url(r'^rodada/$', views.rodada_index, name='rodada_index'),
    url(r'^rodada/edit/(?P<id>\d+)/$', views.rodada_edit, name='rodada_edit'),
    url(r'^rodada/delete/(?P<id>\d+)/$', views.rodada_delete, name='rodada_delete'),
    url(r'^rodada/new/$', views.rodada_new, name='rodada_new'),

    url(r'^emprestimo/$', views.emprestimo_index, name='emprestimo_index'),
    url(r'^emprestimo/edit/(?P<id>\d+)/$', views.emprestimo_edit, name='emprestimo_edit'),
    url(r'^emprestimo/delete/(?P<id>\d+)/$', views.emprestimo_delete, name='emprestimo_delete'),
    url(r'^emprestimo/new/$', views.emprestimo_new, name='emprestimo_new'),
    #URLs para Time
    url(r'^time/$', views.time_index, name='time_index'),
    url(r'^time/edit/(?P<id>\d+)/$', views.time_edit, name='time_edit'),
    url(r'^time/delete/(?P<id>\d+)/$', views.time_delete, name='time_delete'),
    url(r'^time/new/$', views.time_new, name='time_new'),
    # URLs para area
    url(r'^area/$', views.area_index, name='area_index'),
    url(r'^area/edit/(?P<id>\d+)/$', views.area_edit, name='area_edit'),
    url(r'^area/delete/(?P<id>\d+)/$', views.area_delete, name='area_delete'),
    url(r'^area/new/$', views.area_new, name='area_new'),

    url(r'^classe_social/$', views.classe_social_index, name='classe_social_index'),
    url(r'^classe_social/edit/(?P<id>\d+)/$', views.classe_social_edit, name='classe_social_edit'),
    url(r'^classe_social/delete/(?P<id>\d+)/$', views.classe_social_delete, name='classe_social_delete'),
    url(r'^classe_social/new/$', views.classe_social_new, name='classe_social_new'),

    url(r'^modulo/$', views.modulo_index, name='modulo_index'),
    url(r'^modulo/edit/(?P<id>\d+)/$', views.modulo_edit, name='modulo_edit'),
    url(r'^modulo/delete/(?P<id>\d+)/$', views.modulo_delete, name='modulo_delete'),
    url(r'^modulo/new/$', views.modulo_new, name='modulo_new'),

    #interações do jogador
    url(r'^irrelevante', views.iniciar_jogo, name='iniciar_jogo'),
    url(r'^jogo/comprar_modulo', ajax.comprar_modulo, name='comprar_modulo'),
    url(r'^jogo/vender_modulo', ajax.vender_modulo, name='vender_modulo'),
    url(r'^jogo/contratar_medico', ajax.contratar_medico, name='contratar_medico'),
    url(r'^jogo/despedir_medico', ajax.despedir_medico, name='despedir_medico'),
    url(r'^jogo/busca_modulo', ajax.busca_modulo, name='busca_modulo'),
    url(r'^jogo/busca_medico', ajax.busca_medico, name='busca_medico'),
    url(r'^jogo/hospital/medicos/$', ajax.tela_de_jogo_hospital_medicos, name='tela_de_jogo_hospital_med'),
    url(r'^jogo/hospital/modulos/$', ajax.tela_de_jogo_hospital_modulos, name='tela_de_jogo_hospital_mod'),
    url(r'^jogo/hospital/$', views.tela_de_jogo_hospital, name='tela_de_jogo_hospital'),
    url(r'^jogo/dashboard', views.tela_de_jogo_dashboard, name='tela_de_jogo_dashboard'),
    url(r'^jogo/dados_graficos', ajax.tela_de_jogo_graficos, name='tela_de_jogo_graficos'),

    url(r'^jogo/$', views.tela_de_jogo, name='tela_de_jogo'),

    #telas de pre jogo
    url(r'^pre_jogo_1/$', views.pre_jogo_1, name='pre_jogo_1'),
    url(r'^pre_jogo_2/$', views.pre_jogo_2, name='pre_jogo_2'),
    url(r'^pre_jogo_3/$', views.pre_jogo_3, name='pre_jogo_3'),
    url(r'^pre_jogo_4/$', views.pre_jogo_4, name='pre_jogo_4'),
    url(r'^pre_jogo_5/$', views.pre_jogo_5, name='pre_jogo_5'),

    #tela login do jogador
    url(r'^login_jogador/$', views.login_jogador, name='login_jogador'),
    url(r'^logar/$', views.logar, name='logar'),
]
