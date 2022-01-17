from django.db import models
from django.db.models.base import Model
from django.utils import timezone

from .grupo import Grupo


class Equipe(models.Model):
    nome = models.CharField('Nome', max_length=50)

    pontos = models.PositiveIntegerField('Pts', default=0)

    vitorias = models.PositiveIntegerField('V', default=0)

    empates = models.PositiveIntegerField('E', default=0)

    derrotas = models.PositiveIntegerField('D', default=0)

    gols_marcados = models.PositiveIntegerField('GP', default=0)

    gols_sofridos = models.PositiveIntegerField('GC', default=0)

    saldo_gols = models.IntegerField('SG', default=0)

    grupo = models.ForeignKey(
        Grupo, verbose_name='Grupo', null=True, blank=True, on_delete=models.CASCADE)

    campeonato = models.PositiveIntegerField('Campeonato', default=0)

    emblema = models.ImageField(
        'Emblema', upload_to='emblemas/', null=True, blank=True)

    def pts(self):
        return (self.vitorias * 3) + self.empates

    def sg(self):
        return self.gols_marcados - self.gols_sofridos

    def save(self, *args, **kwargs):
        self.pontos = self.pts()
        self.saldo_gols = self.sg()

        # Call the "real" save() method.
        super(Equipe, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-pontos', '-vitorias',
                    '-empates', '-derrotas', '-saldo_gols']

    def __str__(self):
        return self.nome
