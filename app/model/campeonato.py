from django.db import models
from django.db.models.base import Model
from django.utils import timezone


class Campeonato(models.Model):
    FORMATO = (
        ('C', 'Copa'),
        ('PC', 'Pontos corridos'),
    )

    nome = models.CharField('Nome', max_length=30)

    qtd_times = models.PositiveIntegerField('Quantidade de times')

    qtd_grupos = models.PositiveIntegerField('Quantidade de grupos', default=1)

    formato = models.CharField('Formato', max_length=2, choices=FORMATO)
    equipes_cadastradas = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

    def get_formato(self):
        return self.FORMATO
