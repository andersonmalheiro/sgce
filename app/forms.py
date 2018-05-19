from django.forms import ModelForm
from .models import *
from django import forms

class CreateCampeonato(ModelForm):
    class Meta:
        model = Campeonato
        fields = ['nome', 'qtd_times', 'qtd_grupos', 'formato']


class UpdateCampeonato(ModelForm):
    class Meta:
        model = Campeonato
        fields = ['nome']

class CreateEquipe(ModelForm):
    class Meta:
        model = Equipe
        fields = ['nome', 'grupo', 'campeonato','emblema']

class UpdateEquipe(ModelForm):
    class Meta:
        model = Equipe
        fields = ['nome', 'emblema', 'grupo']

class CreateJogador(ModelForm):
    class Meta:
        model = Jogador
        fields = ['nome', 'sobrenome', 'apelido','idade', 'camisa', 'rua', 'bairro', 'cidade', 'equipe', 'foto', 'campeonato']

class UpdateJogador(ModelForm):
    class Meta:
        model = Jogador
        fields = ['nome', 'sobrenome', 'camisa', 'total_gols', 'total_cartoes_amarelos', 'total_cartoes_vermelhos', 'cartoes_acumulados', 'disponivel']

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'imagem']        


class CreatePartida(ModelForm):
    class Meta:
        model = Partida
        fields = ['mandante', 'visitante', 'rodada', 'campeonato', 'data']


class UpdatePartida(ModelForm):
    class Meta:
        model = Partida
        fields = ['gols_mandante', 'gols_visitante', 'total_cart_amarelo', 'total_cart_vermelho', 'finalizada']


class CreateGrupo(ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome', 'campeonato']

class UpdateGrupo(ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome']