from django.conf.urls import url
from .views import *

urlpatterns = [
    #SITE
    url(r'^$', index, name='index'),
    url(r'^tabela/(?P<pk>[0-9]+)/$', tabela, name='tabela'),
    url(r'^post/(?P<pk>[0-9]+)/$', post, name='post'),
    url(r'^noticias/$', noticias, name='noticias'),
    url(r'^equipe/(?P<pk>[0-9]+)/$', equipe, name='equipe'),
    url(r'^partida/(?P<pk>[0-9]+)/$', partida, name='partida'),
    url(r'^partidas/$', partidas, name='partidas'),
    url(r'^aplicativo/$', aplicativo, name='aplicativo'),


    #MANAGER
    url(r'^manager/$', manager, name='manager'),        

    #MANAGER-POST
    url(r'^manager/post/criar/$', post_create, name='post_create'),
    url(r'^manager/post/apagar/(?P<pk>[0-9]+)/$', post_remove, name='post_remove'),
    url(r'^manager/post/listar/$', post_list, name='post_list'),
    url(r'^manager/post/editar/(?P<pk>[0-9]+)/$', post_edit, name='post_edit'),

    #MANAGER-CAMPEONATO
    url(r'^manager/campeonatos/$', champ_list, name='champ_list'),
    url(r'^manager/campeonatos/criar/$', champ_create, name='champ_create'),
    url(r'^manager/campeonatos/apagar/(?P<pk>[0-9]+)/$', champ_remove, name='champ_remove'),    
    url(r'^manager/campeonatos/editar/(?P<pk>[0-9]+)/$', champ_edit, name='champ_edit'),
    url(r'^manager/campeonatos/(?P<pk>[0-9]+)/$', manage_campeonato, name='manage_campeonato'),

    #MANAGER-GRUPO
    url(r'^manager/campeonatos/(?P<pk>[0-9]+)/add_grupo/$', create_grupo, name='create_grupo'),
    url(r'^manager/campeonatos/(?P<c>[0-9]+)/del_grupo/(?P<pk>[0-9]+)/$', grupo_remove, name='grupo_remove'),
    url(r'^manager/campeonatos/(?P<pk>[0-9]+)/list_grupo/$', grupo_list, name='list_grupo'),
    url(r'^manager/campeonato/(?P<c>[0-9]+)/editar_grupo/(?P<pk>[0-9]+)/$', grupo_edit, name='grupo_edit'),

    #MANAGER-EQUIPE
    url(r'^manager/campeonatos/(?P<pk>[0-9]+)/add_equipe/$', create_equipe, name='create_equipe'),
    url(r'^manager/campeonatos/(?P<c>[0-9]+)/del_equipe/(?P<pk>[0-9]+)/$', equipe_remove, name='equipe_remove'),
    url(r'^manager/campeonatos/(?P<pk>[0-9]+)/list_equipe/$', equipe_list, name='list_equipe'),
    url(r'^manager/campeonatos/(?P<c>[0-9]+)/editar_equipe/(?P<pk>[0-9]+)/$', equipe_edit, name='equipe_edit'),

    #MANAGER-JOGADOR
    url(r'^manager/campeonatos/(?P<pk>[0-9]+)/add_jogador/$', create_jogador, name='create_jogador'),
    url(r'^manager/campeonatos/(?P<c>[0-9]+)/del_jogador/(?P<pk>[0-9]+)/$', jogador_remove, name='jogador_remove'),
    url(r'^manager/campeonatos/(?P<pk>[0-9]+)/list_jogador/$', jogador_list, name='list_jogador'),
    url(r'^manager/campeonato/(?P<c>[0-9]+)/editar_jogador/(?P<pk>[0-9]+)/$', jogador_edit, name='jogador_edit'),

    #MANAGER-PARTIDA
    url(r'^manager/campeonatos/add_partida/(?P<pk>[0-9]+)/$', create_partida, name='add_partida'),
    url(r'^manager/campeonatos/del_partida/(?P<pk>[0-9]+)/$', partida_remove, name='partida_remove'),
    url(r'^manager/campeonatos/list_partida/(?P<pk>[0-9]+)/$', partida_list, name='list_partida'),
    url(r'^manager/campeonato/editar_partida/(?P<pk>[0-9]+)/$', partida_edit, name='partida_edit'),

    # url(r'^manager/campeonatos/gerar/(?P<pk>[0-9]+)/$', gerar_partidas, name='gerar_partidas'),
    url(r'^manager/campeonatos/update_resultado/(?P<pk>[0-9]+)/$', update_resultado, name='update_resultado'),    
    url(r'^manager/campeonatos/criar_lance/$', criar_lance, name='criar_lance'),

]