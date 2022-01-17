from django import forms
from django.forms import ModelForm

from app.model.campeonato import Campeonato
from app.model.equipe import Equipe
from app.model.grupo import Grupo
from app.model.jogador import Jogador
from app.model.lance import Lance
from app.model.partida import Partida
from app.model.post import Post
from app.model.tecnico import Tecnico


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
        fields = ['nome', 'grupo', 'campeonato', 'emblema']


class UpdateEquipe(ModelForm):
    class Meta:
        model = Equipe
        fields = ['nome', 'emblema', 'grupo']


class CreateJogador(ModelForm):
    class Meta:
        model = Jogador
        fields = ['nome', 'sobrenome', 'apelido', 'idade', 'camisa',
                  'rua', 'bairro', 'cidade', 'equipe', 'foto', 'campeonato']


class UpdateJogador(ModelForm):
    class Meta:
        model = Jogador
        fields = ['nome', 'sobrenome', 'camisa', 'total_gols', 'total_cartoes_amarelos',
                  'total_cartoes_vermelhos', 'cartoes_acumulados', 'disponivel']


class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['titulo', 'conteudo', 'imagem']


class CreatePartida(ModelForm):
    class Meta:
        model = Partida
        fields = ['mandante', 'visitante', 'campeonato', 'data', 'hora']


class UpdatePartida(ModelForm):
    class Meta:
        model = Partida
        fields = ['gols_mandante', 'gols_visitante',
                  'total_cart_amarelo', 'total_cart_vermelho', 'finalizada']


class CreateGrupo(ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome', 'campeonato']


class UpdateGrupo(ModelForm):
    class Meta:
        model = Grupo
        fields = ['nome']
