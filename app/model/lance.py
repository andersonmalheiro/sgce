from django.db import models
from django.db.models.base import Model
from django.utils import timezone

from .equipe import Equipe
from .jogador import Jogador
from .partida import Partida


class Lance(models.Model):
    TIPO = (
        ('G', 'Gol'),
        ('GC', 'Gol contra'),
        ('CA', 'Cartão amarelo'),
        ('CV', 'Cartão vermelho'),
    )

    jogador = models.ForeignKey(
        Jogador, verbose_name='Jogador', on_delete=models.CASCADE)

    partida = models.ForeignKey(
        Partida, verbose_name='Partida', on_delete=models.CASCADE)

    lance = models.CharField('Lance', max_length=2, choices=TIPO)

    equipe = models.ForeignKey(
        Equipe, verbose_name='Equipe', default=None, on_delete=models.CASCADE)

    descricao = models.CharField('Descrição', max_length=200, default='')

    tempo = models.PositiveIntegerField('Tempo', default=0)

    minuto = models.PositiveIntegerField('Minuto', default=0)

    def __str__(self):
        return self.lance

    def update(self):
        if self.lance == 'G':
            self.jogador.total_gols += 1

            if self.jogador.equipe == self.partida.mandante:
                self.partida.gols_mandante += 1

            else:
                self.partida.gols_visitante += 1

        if self.lance == 'GC':
            self.jogador.total_gols_contra += 1

            if self.jogador.equipe == self.partida.mandante:
                self.partida.gols_visitante += 1

            else:
                self.partida.gols_mandante += 1

        elif self.lance == 'CA':
            self.jogador.total_cartoes_amarelos += 1
            self.jogador.cartoes_acumulados += 1
            self.partida.total_cart_amarelo += 1

        elif self.lance == 'CV':
            self.jogador.total_cartoes_vermelhos += 1
            self.jogador.disponivel = False
            self.partida.total_cart_vermelho += 1

        self.jogador.save()
        self.partida.save()
