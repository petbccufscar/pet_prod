from django.conf.urls import url
from jogo import views

urlpatterns = [
    # URLs para home
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.index, name='home'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^base_configuracoes/$', views.base_configuracoes, name='base_configuracoes'),
    url(r'^base_aplicar_dinamica/$', views.base_aplicar_dinamica, name='base_aplicar_dinamica'),
    # Cuidado com as URLS!
    # Como estamos utilizando apenas um app, temos que colocar o class/xxx
    url(r'^medico/$', views.medico_index, name='medico_index'),
    url(r'^medico/edit/(?P<id>\d+)/$', views.medico_edit, name='medico_edit'),
    url(r'^medico/delete/(?P<id>\d+)/$', views.medico_delete, name='medico_delete'),
    url(r'^medico/new/$', views.medico_new, name='medico_new'),

    #URLs para Time
    url(r'^time/$', views.time_index, name='time_index'),
    url(r'^time/edit/(?P<id>\d+)/$', views.time_edit, name='time_edit'),
    url(r'^time/delete/(?P<id>\d+)/$', views.time_delete, name='time_delete'),
    url(r'^time/new/$', views.time_new, name='time_new'),

]
