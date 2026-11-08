from django.db import models
from django.db.models.base import Model
from django.utils import timezone

from .equipe import Equipe


class Partida(models.Model):
    FASE = (
        ('G', 'Grupos'),
        ('O', 'Oitavas'),
        ('Q', 'Quartas'),
        ('S', 'Semi-final'),
        ('F', 'Final')
    )

    mandante = models.ForeignKey(
        Equipe, verbose_name='Mandante', related_name='mandante', on_delete=models.CASCADE)

    visitante = models.ForeignKey(
        Equipe, verbose_name='Visitante', related_name='visitante', on_delete=models.CASCADE)

    rodada = models.PositiveIntegerField('Rodada', null=True, blank=True)

    campeonato = models.PositiveIntegerField('Campeonato', default=None)

    gols_mandante = models.PositiveIntegerField('Gols mandante', default=0)

    gols_visitante = models.PositiveIntegerField('Gols visitante', default=0)

    total_cart_amarelo = models.PositiveIntegerField(
        'Cartões amarelos', default=0)

    total_cart_vermelho = models.PositiveIntegerField(
        'Cartões vermelhos', default=0)

    data = models.DateTimeField('Data', null=True, blank=True)

    hora = models.CharField('Hora', default="--:--",
                            max_length=5, null=True, blank=True)
    finalizada = models.BooleanField(default=False)

    fase = models.CharField('Fase', max_length=1, choices=FASE, default='G')

    def __str__(self):
        return '%s x %s' % (self.mandante, self.visitante)

    def save(self, *args, **kwargs):
        if self.finalizada:
            if self.gols_mandante > self.gols_visitante:
                self.mandante.vitorias += 1
                self.visitante.derrotas += 1
                self.mandante.gols_marcados += self.gols_mandante
                self.mandante.gols_sofridos += self.gols_visitante
                self.visitante.gols_marcados += self.gols_visitante
                self.visitante.gols_sofridos += self.gols_mandante

            elif self.gols_mandante < self.gols_visitante:
                self.visitante.vitorias += 1
                self.mandante.derrotas += 1
                self.visitante.gols_marcados += self.gols_visitante
                self.visitante.gols_sofridos += self.gols_mandante
                self.mandante.gols_marcados += self.gols_mandante
                self.mandante.gols_sofridos += self.gols_visitante

            else:
                self.visitante.empates += 1
                self.mandante.empates += 1
                self.mandante.gols_marcados += self.gols_mandante
                self.mandante.gols_sofridos += self.gols_visitante
                self.visitante.gols_marcados += self.gols_visitante
                self.visitante.gols_sofridos += self.gols_mandante

            # Call the "real" save() method.
            super(Partida, self).save(*args, **kwargs)
            self.mandante.save(*args, **kwargs)
            self.visitante.save(*args, **kwargs)

        else:
            # Call the "real" save() method.
            super(Partida, self).save(*args, **kwargs)
