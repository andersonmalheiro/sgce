from django.db import models
from django.db.models.base import Model
from django.utils import timezone

from .campeonato import Campeonato


class Grupo(models.Model):
    nome = models.CharField('Nome', max_length=30)

    campeonato = models.ForeignKey(Campeonato, on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
