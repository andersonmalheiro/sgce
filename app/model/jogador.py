from django.db import models
from django.db.models.base import Model
from django.utils import timezone

from .equipe import Equipe


class Jogador(models.Model):
    nome = models.CharField('Nome', max_length=50)

    sobrenome = models.CharField('Sobrenome', max_length=100)

    apelido = models.CharField('Apelido', max_length=30, null=True, blank=True)

    idade = models.PositiveIntegerField('Idade', null=True, blank=True)

    camisa = models.PositiveIntegerField('N° Camisa', null=True, blank=True)

    rua = models.CharField('Rua', max_length=50)

    bairro = models.CharField('Bairro', max_length=50)

    cidade = models.CharField('Cidade', max_length=50)

    total_gols = models.PositiveIntegerField('Gols', default=0)

    total_gols_contra = models.PositiveIntegerField('Gols contra', default=0)

    total_cartoes_amarelos = models.PositiveIntegerField(
        'Cartões amarelos', default=0)

    total_cartoes_vermelhos = models.PositiveIntegerField(
        'Cartões vermelhos', default=0)

    cartoes_acumulados = models.PositiveIntegerField(
        'Cartões acumulados', default=0)

    disponivel = models.BooleanField(default=True)

    equipe = models.ForeignKey(
        Equipe, verbose_name='Equipe', on_delete=models.CASCADE)

    foto = models.ImageField('Foto', upload_to='fotos/', null=True, blank=True)

    campeonato = models.PositiveIntegerField('Campeonato', default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Jogador'
        verbose_name_plural = 'Jogadores'

    def check_disponibilidade(self):
        if self.cartoes_acumulados == 2:
            self.disponivel = False
            self.cartoes_acumulados = 0

    def __str__(self):
        return '%s %s' % (self.nome, self.sobrenome)
