from django.db import models
from django.db.models.base import Model
from django.utils import timezone

from .equipe import Equipe


class Tecnico(models.Model):
    nome = models.CharField('Nome', max_length=100)
    
    equipe = models.ForeignKey(
        Equipe, verbose_name='Equipe', on_delete=models.CASCADE)

    def __str__(self):
        return self.nome
