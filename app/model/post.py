from django.db import models
from django.db.models.base import Model
from django.utils import timezone


class Post(models.Model):
    titulo = models.CharField('Titulo', max_length=200)
    conteudo = models.TextField('Conteudo')
    imagem = models.ImageField('Imagem', upload_to='imgPosts/', null=True)
    created_date = models.DateTimeField(
        'Data de criação', default=timezone.now)

    def __str__(self):
        return self.titulo
