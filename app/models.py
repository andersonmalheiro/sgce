from django.db import models
from django.utils import timezone
from django.db.models.base import Model


class Campeonato(models.Model):
    FORMATO = (
        ('C','Copa'),
        ('PC','Pontos corridos'),
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

class Grupo(models.Model):
    nome = models.CharField('Nome', max_length=30)
    campeonato = models.ForeignKey(Campeonato)

    def __str__(self):
        return self.nome


# Metodos para calcular total de pontos e saldo de gols
def pts(self):
        return (self.vitorias * 3) + self.empates

def sg(self):
        return self.gols_marcados - self.gols_sofridos


class Equipe(models.Model):
    nome = models.CharField('Nome', max_length=50)
    pontos = models.PositiveIntegerField('Pts', default=0)
    vitorias = models.PositiveIntegerField('V', default=0)
    empates = models.PositiveIntegerField('E', default=0)
    derrotas = models.PositiveIntegerField('D', default=0)
    gols_marcados = models.PositiveIntegerField('GP', default=0)
    gols_sofridos = models.PositiveIntegerField('GC', default=0)
    saldo_gols = models.PositiveIntegerField('SG', default=0)
    grupo = models.ForeignKey(Grupo, verbose_name='Grupo', null=True, blank=True)
    campeonato = models.PositiveIntegerField('Campeonato', default=0)
    emblema = models.ImageField('Emblema', upload_to='emblemas/', null=True, blank=True)


    def save(self, *args, **kwargs):
        self.pontos = pts(self)
        self.saldo_gols = sg(self)
        super(Equipe, self).save(*args, **kwargs) # Call the "real" save() method.

    class Meta:
        ordering = ['-pontos', '-vitorias', '-empates', '-derrotas','-saldo_gols']

    def __str__(self):
        return self.nome


class Tecnico(models.Model):
    nome = models.CharField('Nome', max_length=100)
    equipe = models.ForeignKey(Equipe, verbose_name='Equipe')

    def __str__(self):
        return self.nome


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
    total_cartoes_amarelos = models.PositiveIntegerField('Cartões amarelos', default=0)
    total_cartoes_vermelhos = models.PositiveIntegerField('Cartões vermelhos', default=0)
    cartoes_acumulados = models.PositiveIntegerField('Cartões acumulados', default=0)
    disponivel = models.BooleanField(default=True)
    equipe = models.ForeignKey(Equipe, verbose_name='Equipe')
    foto = models.ImageField('Foto', upload_to='fotos/', null=True, blank=True)
    campeonato = models.PositiveIntegerField('Campeonato', default=0)

    created_at = models.DateTimeField(auto_now_add=True)    

    class Meta:
        verbose_name='Jogador'
        verbose_name_plural = 'Jogadores'
    

    def check_disponibilidade(self):
        if self.cartoes_acumulados == 2:
            self.disponivel = False
            self.cartoes_acumulados = 0

    def __str__(self):
        return '%s %s' % (self.nome, self.sobrenome)


class Partida(models.Model):
    mandante = models.ForeignKey(Equipe, verbose_name='Mandante', related_name='mandante')
    visitante = models.ForeignKey(Equipe, verbose_name='Visitante', related_name='visitante')
    rodada = models.PositiveIntegerField('Rodada')
    # grupo = models.ForeignKey(Grupo, verbose_name='Grupo')
    campeonato = models.PositiveIntegerField('Campeonato', default=None)
    gols_mandante = models.PositiveIntegerField('Gols mandante', default=0)
    gols_visitante = models.PositiveIntegerField('Gols visitante', default=0)
    total_cart_amarelo = models.PositiveIntegerField('Cartões amarelos', default=0)
    total_cart_vermelho = models.PositiveIntegerField('Cartões vermelhos', default=0)
    data = models.DateTimeField('Data', null=True, blank=True)
    finalizada = models.BooleanField(default=False)

    def __str__(self):
        return '%s x %s' % (self.mandante, self.visitante)

    def save(self, *args, **kwargs):
        if self.finalizada:
            if self.gols_mandante > self.gols_visitante:
                self.mandante.vitorias += 1
                self.visitante.derrotas += 1
                self.mandante.gols_marcados += self.gols_mandante
                self.mandante.gols_sofridos += self.gols_visitante
            elif self.gols_mandante < self.gols_visitante:            
                self.visitante.vitorias += 1
                self.mandante.derrotas += 1
                self.visitante.gols_marcados += self.gols_visitante
                self.visitante.gols_sofridos += self.gols_mandante
            else:
                self.visitante.empates += 1
                self.mandante.empates += 1
                self.mandante.gols_marcados += self.gols_mandante
                self.mandante.gols_sofridos += self.gols_visitante
                self.visitante.gols_marcados += self.gols_visitante
                self.visitante.gols_sofridos += self.gols_mandante
            
            super(Partida, self).save(*args, **kwargs) # Call the "real" save() method.
            self.mandante.save(*args, **kwargs)
            self.visitante.save(*args, **kwargs)
        else:
            super(Partida, self).save(*args, **kwargs) # Call the "real" save() method.        

class Lance(models.Model):    
    TIPO = (
        ('G','Gol'),
        ('GC','Gol contra'),
        ('CA','Cartão amarelo'),
        ('CV','Cartão vermelho'),
    )
    jogador = models.ForeignKey(Jogador, verbose_name='Jogador')
    partida = models.ForeignKey(Partida, verbose_name='Partida')
    lance = models.CharField('Lance', max_length=2, choices=TIPO)
    equipe = models.ForeignKey(Equipe, verbose_name='Equipe', default=None)
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


class Post(models.Model):
    titulo = models.CharField('Titulo', max_length=200)
    conteudo = models.TextField('Conteudo')
    imagem = models.ImageField('Imagem', upload_to='imgPosts/', null=True)
    created_date = models.DateTimeField('Data de criação', default=timezone.now)

    def __str__(self):
        return self.titulo