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

    url(r'^emprestimo/$', views.emprestimo_index, name='emprestimo_index'),
    url(r'^emprestimo/edit/(?P<id>\d+)/$', views.emprestimo_edit, name='emprestimo_edit'),
    url(r'^emprestimo/delete/(?P<id>\d+)/$', views.emprestimo_delete, name='emprestimo_delete'),
    url(r'^emprestimo/new/$', views.emprestimo_new, name='emprestimo_new'),
]
