from django.contrib import admin
from .models import *

# Register your models here.

class GrupoInline(admin.StackedInline):
    model = Grupo
    extra = 1
    max_num = 8


class TimeInline(admin.StackedInline):
    model = Equipe
    extra = 1    


class TecnicoInline(admin.StackedInline):
    model = Tecnico
    extra = 1
    max_num = 1


class CampeonatoAdmin(admin.ModelAdmin):
    inlines = [GrupoInline]


class GrupoAdmin(admin.ModelAdmin):
    inlines = [TimeInline]


class TimeAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['nome', 'grupo','campeonato', 'vitorias', 'empates', 'derrotas', 'gols_marcados', 'gols_sofridos', 'emblema']}),     
    ]
    inlines = [TecnicoInline]
    list_display = ('nome', 'grupo', 'pontos', 'vitorias', 'empates', 'derrotas', 'saldo_gols')
    list_filter = ['grupo']
    search_fields = ['nome']


class PartidaAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['grupo', 'data', 'rodada', 'mandante','gols_mandante', 'visitante','gols_visitante', 'finalizada']})        
    ]    
    
    list_filter = ['mandante', 'visitante', 'campeonato']

class PostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {'fields': ['titulo', 'conteudo', 'imagem', 'created_date']})
    ]

admin.site.register(Campeonato, CampeonatoAdmin)
admin.site.register(Equipe, TimeAdmin)
admin.site.register(Jogador)
admin.site.register(Partida, PartidaAdmin)
admin.site.register(Tecnico)
admin.site.register(Lance)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Post, PostAdmin)