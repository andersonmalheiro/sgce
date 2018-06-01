from django.http import Http404, JsonResponse, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from .models import *
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from logica.functions import *
from django.views.generic import UpdateView
import json

# Objetos torneio e grupos
class Torneio(object):
    def __init__(self, nome, formato, grupos, pk, sorteado):
        self.nome = nome
        self.formato = formato
        self.grupos = grupos
        self.pk = pk
        self.sorteado = sorteado
    

class Group(object):
    def __init__(self, nome, times, pk):
        self.nome = nome
        self.times = times
        self.pk = pk


# Create your views here.

def index(request):
    camps = Campeonato.objects.all().order_by('nome')    
    grupos = []          
    torneios = []
    sorteado = False

    for c in camps:
        groups = Grupo.objects.filter(campeonato = c).order_by('nome')
        for g in groups:
            times = Equipe.objects.filter(grupo = g).order_by('-pontos')[:4]
            if len(times) > 0:
                sorteado = True
            grupo = Group(g.nome, times, g.pk)
            grupos.append(grupo)
        campeonato = Torneio(c.nome, c.formato, grupos, c.pk, sorteado)
        torneios.append(campeonato)
        grupos = []
        sorteado = False
    
    posts = Post.objects.all().order_by('-created_date')[2:5]
    posts2 = Post.objects.all( ).order_by('-created_date')[:2]
    
    context={
        'camps':camps,
        'torneios':torneios,
        'posts': posts,
        'posts2':posts2
    }
    
    return render(request, 'app/inicio.html', context)

def tabela(request, pk):
    camps = Campeonato.objects.all().order_by('nome')
    camp = get_object_or_404(Campeonato, pk=pk)
    jogadores = Jogador.objects.filter(campeonato = camp.pk).filter(total_gols__gt = 0).order_by('-total_gols')[:5]
        
    grupos = []              
    sorteado = False
    
    groups = Grupo.objects.filter(campeonato = camp).order_by('nome')
    for g in groups:
        times = Equipe.objects.filter(grupo = g).order_by('-pontos')[:4]
        if len(times) > 0:
            sorteado = True
        grupo = Group(g.nome, times, g.pk)
        grupos.append(grupo)
    
    campeonato = Torneio(camp.nome, camp.formato, grupos, camp.pk, sorteado)    
    
    context ={                
        'camps': camps,
        'campeonato':campeonato,
        'jogadores':jogadores
    }
    return render(request, 'app/tabela.html', context)

def post(request, pk):
    champs = Campeonato.objects.all().order_by('nome')
    post = get_object_or_404(Post, pk=pk)

    return render(request, 'app/post.html', {'post': post, 'camps':champs})

def noticias(request):
    camps = Campeonato.objects.all().order_by('nome')
    post_list = Post.objects.all().order_by('-created_date')
    paginator = Paginator(post_list, 5) # Show 5 contacts per page

    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'app/noticias.html', {'posts': posts, 'camps': camps})

def partidas(request):
    camps = Campeonato.objects.all().order_by('nome')
    partidas = Partida.objects.all().order_by('pk')
    context = {
        'camps':camps,
        'partidas':partidas
    }

    return render(request, 'app/partidas.html', context)

def partida(request, pk):
    camps = Campeonato.objects.all().order_by('nome')
    partida = get_object_or_404(Partida, pk=pk)
    lances = Lance.objects.filter(partida=partida).order_by('pk')
    #lances_mandante = Lance.objects.filter(partida=partida, equipe=partida.mandante)
    #lances_visitante = Lance.objects.filter(partida=partida, equipe=partida.visitante)
    context = {
        'partida': partida,
        'lances': lances,
        'camps':camps,
        }
    
    return render(request, 'app/partida.html', context)

def equipe(request, pk):
    camps = Campeonato.objects.all().order_by('nome')
    time = get_object_or_404(Equipe, pk=pk)
    tecnico = get_object_or_404(Tecnico, equipe=pk)
    jogadores = Jogador.objects.filter(equipe = pk).order_by('camisa')
    partidas = Partida.objects.filter(Q(mandante = pk) | Q(visitante = pk)).order_by('pk')
    paginator = Paginator(partidas, 8)

    page = request.GET.get('page')
    try:
        partida = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        partida = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        partida = paginator.page(paginator.num_pages)
    context = {
        'equipe': time,
        'tecnico': tecnico,
        'jogadores': jogadores,
        'camps': camps,
        'partida': partida
        }
    return render(request, 'app/equipe.html', context)

def aplicativo(request):
    camps = Campeonato.objects.all().order_by('nome')
    return render(request, 'app/aplicativo.html', {'camps': camps})

# Admin
######################################################################

@login_required(redirect_field_name='next',login_url='/manager/login/')
def manager(request):    
    return render(request, 'manager/home.html', {})

@login_required(login_url='/manager/login/')
def manage_campeonato(request, pk):    
    
    champ = get_object_or_404(Campeonato, pk = pk)
    formato = champ.formato

    if formato == 'PC':
        groups = get_object_or_404(Grupo, campeonato=pk)
        teams = Equipe.objects.filter(grupo = groups)
        players = Jogador.objects.filter(campeonato = pk)        
        tecnicos = []

        for t in teams:
            aux = list(Tecnico.objects.filter(equipe = t))
            tecnicos += aux
        
        partidas = len(Partida.objects.filter(campeonato = pk))

        context = {
            'groups':groups,
            'teams':teams,
            'players':players,
            'tecnicos':tecnicos,
            'formato':formato,                
            'champ':champ,
            'partidas': partidas
            }
        return render(request, 'manager/gerenciar_campeonatos.html', context)
    
    else:
        groups = list(Grupo.objects.filter(campeonato=pk))        
        teams = Equipe.objects.filter(campeonato=pk)                    

        players = Jogador.objects.filter(campeonato = pk)

        tecnicos = []
        for t in teams:
            aux = list(Tecnico.objects.filter(equipe = t))
            tecnicos += aux
            
        partidas = len(list(Partida.objects.filter(campeonato = pk)))

        context = {
            'groups':groups,
            'teams':teams,
            'players':players,  
            'tecnicos':tecnicos,              
            'formato':formato,                
            'champ':champ,
            'partidas': partidas
            }
        return render(request, 'manager/gerenciar_campeonatos.html', context)    


@login_required(login_url='/manager/login/')
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            titulo = request.POST["titulo"]
            conteudo = request.POST["conteudo"]
            imagem = form.cleaned_data["imagem"]
            post = Post(titulo=titulo, conteudo=conteudo, imagem=imagem)
            post.save()
            return redirect('post_list')

    return render(request, 'manager/create/add_posts.html', {})

@login_required(login_url='/manager/login/')
def champ_remove(request, pk):
    champ = Campeonato.objects.get(pk=pk)
    if request.method == "POST":
        champ.delete()
        return redirect('champ_list')
    return render(request, 'manager/delete/confirm_delete_campeonato.html', {'champ': champ})

@login_required(login_url='/manager/login/')
def post_remove(request, pk):
    post = Post.objects.get(pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect('post_list')
    return render(request, 'manager/delete/confirm_delete_post.html', {'post': post})

@login_required(login_url='/manager/login/')
def champ_create(request): 
    if request.method == "POST":
        form = CreateCampeonato(request.POST or None)        
        if form.is_valid():
            print("Chegou aqui")
            nome = request.POST["nome"]
            formato = request.POST["formato"]
            qtd_times = request.POST["qtd_times"]
            qtd_grupos = 0

            if formato == 'PC':                
                qtd_grupos = 1
            else:                
                qtd_grupos = request.POST["qtd_grupos"]
            
            campeonato = Campeonato(nome=nome, qtd_times=qtd_times, qtd_grupos=qtd_grupos, formato=formato)
            campeonato.save()

            if formato == 'PC':
                g = Grupo(nome=nome, campeonato=campeonato)
                g.save()

            return redirect('manage_campeonato', pk=campeonato.pk)
        else:
            print("erro")
    else:
        return render(request, 'manager/create/add_campeonato.html', {})

@login_required(login_url='/manager/login/')
def champ_edit(request, pk):
    champ = get_object_or_404(Campeonato, pk=pk)
    if request.method == 'POST':
        form = UpdateCampeonato(request.POST, instance = champ)
        if form.is_valid():
            champ.save()
            return redirect('champ_list')
    else:
        form = UpdateCampeonato(instance=champ)
    
    return render(request, 'manager/update/editar_campeonato.html', {'form':form})


@login_required(login_url='/manager/login/')
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)

    return render(request, 'manager/update/editar_post.html', {'form': form})

@login_required(login_url='/manager/login/')
def champ_list(request):
    champs = Campeonato.objects.all().order_by('nome')
    return render(request, 'manager/read/listar_campeonatos.html', {'champs':champs})

@login_required(login_url='/manager/login/')
def post_list(request):
    posts = Post.objects.all().order_by('-created_date')
    return render(request, 'manager/read/listar_posts.html', {'posts':posts})


@login_required(login_url='/manager/login/')
def create_equipe(request, pk):            
    grupos = Grupo.objects.filter(campeonato=pk)
    if request.method == "POST":
        form = CreateEquipe(request.POST or None, request.FILES or None)        
        if form.is_valid():
            nome = request.POST['nome']            
            if request.POST['grupo'] != '':
                grupo = get_object_or_404(Grupo, pk=request.POST['grupo'])
                campeonato = request.POST['campeonato']                        
                emblema = form.cleaned_data['emblema']
                equipe = Equipe(nome=nome, grupo=grupo, campeonato=campeonato, emblema=emblema)                            
                equipe.save()
                tecnico = request.POST['tecnico']
                t = Tecnico(nome=tecnico, equipe=equipe)
                t.save()            
            else:
                campeonato = request.POST['campeonato']                        
                emblema = form.cleaned_data['emblema']
                equipe = Equipe(nome=nome, campeonato=campeonato, emblema=emblema)                            
                equipe.save()
                tecnico = request.POST['tecnico']
                t = Tecnico(nome=tecnico, equipe=equipe)
                t.save()            
            return redirect('list_equipe', pk=equipe.campeonato)
        else:
            print('----------------------------------------------')
            print('Erro')
            print('----------------------------------------------')
            return render(request, 'manager/create/add_equipe.html', {'grupos':grupos, 'champ':pk, 'form':form})
    return render(request, 'manager/create/add_equipe.html', {'grupos':grupos, 'champ':pk})

@login_required(login_url='/manager/login/')
def equipe_list(request, pk):
    equipes = Equipe.objects.filter(campeonato=pk).order_by('pk')
    champ = get_object_or_404(Campeonato, pk=pk)
    return render(request, 'manager/read/listar_equipes.html', {'equipes':equipes, 'pk': pk, 'champ':champ})

@login_required(login_url='/manager/login/')
def equipe_edit(request, c, pk):
    equipe = get_object_or_404(Equipe, pk = pk)
    if request.method == 'POST':
        form = UpdateEquipe(request.POST, instance = equipe)
        if form.is_valid():
            equipe.save()
            return redirect('list_equipe', pk = c)
    else:
        form = UpdateEquipe(instance = equipe)

    return render(request, 'manager/update/editar_equipe.html', {'form': form})


@login_required(login_url = '/manager/login/')
def equipe_remove(request, c, pk):
    equipe = get_object_or_404(Equipe, pk = pk)
    if request.method == "POST":
        equipe.delete()
        return redirect('list_equipe', pk = c)
    return render(request, 'manager/delete/confirm_delete_equipe.html', {'equipe': equipe})

@login_required(login_url = '/manager/login/')
def create_jogador(request, pk):
    equipes = Equipe.objects.filter(campeonato = pk)
    if request.method == "POST":
        form = CreateJogador(request.POST or None, request.FILES or None)
        if form.is_valid():
            nome = request.POST['nome']
            sobrenome = request.POST['sobrenome']
            apelido = request.POST['apelido']            
            rua = request.POST['rua']
            bairro = request.POST['bairro']
            cidade = request.POST['cidade']
            foto = form.cleaned_data['foto']
            equipe = get_object_or_404(Equipe, pk=request.POST['equipe'])
            campeonato = int(request.POST['campeonato']) 
            
            idade = 0            
            try:
                idade = int(request.POST['idade'])                
                jogador = Jogador(nome=nome, sobrenome=sobrenome, apelido=apelido, idade=idade, foto=foto, equipe=equipe, campeonato=campeonato, rua=rua, bairro=bairro, cidade=cidade)
                jogador.save()            
                return redirect('list_jogador', pk=pk)
            except ValueError:
                jogador = Jogador(nome=nome, sobrenome=sobrenome, apelido=apelido, foto=foto, equipe=equipe, campeonato=campeonato, rua=rua, bairro=bairro, cidade=cidade)
                jogador.save()            
                return redirect('list_jogador', pk=pk)
        else:
            print('----------------------------------------------')
            print('Erro')
            print('----------------------------------------------')
            return render(request, 'manager/create/add_jogador.html', {'equipes': equipes, 'champ': pk, 'form': form})
    return render(request, 'manager/create/add_jogador.html', {'equipes': equipes, 'champ': pk})

@login_required(login_url='/manager/login/')
def jogador_list(request, pk):
    equipes = Equipe.objects.filter(campeonato=pk)
    if request.method == 'GET':
        if 'equipe' in request.GET:
            jogadores = Jogador.objects.filter(equipe = request.GET['equipe'])
            return render(request, 'manager/read/listar_jogadores.html', {'equipes': equipes, 'jogadores': jogadores, 'pk':pk})
        else:
            jogadores = Jogador.objects.filter(campeonato=pk).order_by('pk')
            return render(request, 'manager/read/listar_jogadores.html', {'equipes': equipes, 'jogadores':jogadores, 'pk':pk})

@login_required(login_url='/manager/login/')
def jogador_edit(request, c, pk):
    jogador = get_object_or_404(Jogador, pk = pk)
    if request.method == 'POST':
        form = UpdateJogador(request.POST, instance = jogador)
        if form.is_valid():
            jogador.save()
            return redirect('list_jogador', pk = c)
    else:
        form = UpdateJogador(instance = jogador)

    return render(request, 'manager/update/editar_jogador.html', {'form': form})

@login_required(login_url='/manager/login/')
def jogador_remove(request, c, pk):
    jogador = get_object_or_404(Jogador, pk = pk)
    if request.method == "POST":
        jogador.delete()
        return redirect('list_jogador', pk = c)
    return render(request, 'manager/delete/confirm_delete_jogador.html', {'jogador': jogador})

@login_required(login_url='/manager/login/')
def create_partida(request, pk):
    equipes = Equipe.objects.filter(campeonato = pk)
    # grupos = Grupo.objects.filter(campeonato = pk)
    if request.method == 'POST':
        form = CreatePartida(request.POST or None)        
        if form.is_valid():
            mandante = get_object_or_404(Equipe, pk=request.POST['mandante'])
            visitante = get_object_or_404(Equipe, pk=request.POST['visitante'])
            # grupo = get_object_or_404(Grupo, pk=request.POST['grupo'])
            # rodada = request.POST['rodada']
            fase = request.POST['fase']
            campeonato = request.POST['campeonato']
            data = request.POST['data']
            hora = request.POST['hora']
            partida = Partida(mandante=mandante, visitante=visitante, fase=fase, campeonato=campeonato, data=data, hora=hora)
            partida.save()
            return redirect('list_partida', pk=campeonato)
    context = {
        'equipes':equipes,        
        'pk':pk,
    }
    return render(request, 'manager/create/add_partida.html', context)


@login_required(login_url='/manager/login/')
def partida_list(request, pk):
    equipes = Equipe.objects.filter(campeonato=pk)
    if request.method == 'GET':
        if 'equipe' in request.GET:
            partidas = Partida.objects.filter(Q(mandante = request.GET['equipe']) | Q(visitante = request.GET['equipe'])).order_by('pk')
            return render(request, 'manager/read/listar_partidas.html', {'partidas':partidas, 'equipes':equipes, 'pk':pk})
        else:
            partidas = Partida.objects.filter(campeonato=pk).order_by('pk')
            return render(request, 'manager/read/listar_partidas.html', {'partidas':partidas, 'equipes':equipes, 'pk':pk})


@login_required(login_url='/manager/login/')
def partida_edit(request, pk):
    partida = get_object_or_404(Partida, pk=pk)
    if request.method == 'POST':
        form = UpdatePartida(request.POST, instance=partida)
        if form.is_valid():
            partida.save()
            return redirect('list_partida', pk=partida.campeonato)
    else:
        form = UpdatePartida(instance=partida)

    return render(request, 'manager/update/editar_partida.html', {'form': form})



@login_required(login_url='/manager/login/')
def partida_remove(request, pk):
    partida = Partida.objects.get(pk=pk)
    if request.method == "POST":
        partida.delete()
        return redirect('list_partida', pk=partida.campeonato)
    return render(request, 'manager/delete/confirm_delete_partida.html', {'partida': partida})

@csrf_exempt
@login_required(login_url='/manager/login/')
def update_resultado(request, pk):    
    partida = get_object_or_404(Partida, pk=pk)
    if request.method == 'POST':
        if 'finaliza' in request.POST:
            partida.finalizada = True
            partida.save()
            return redirect('list_partida', pk=partida.campeonato)

    lances_mandante = Lance.objects.filter(partida=partida, equipe=partida.mandante)
    lances_visitante = Lance.objects.filter(partida=partida, equipe=partida.visitante)
    jogadores = Jogador.objects.filter(Q(equipe =partida.mandante) | Q(equipe = partida.visitante))    
    context = {
        'partida':partida,
        'jogadores': jogadores,        
        'lances_mandante': lances_mandante,
        'lances_visitante': lances_visitante,
    }
    return render(request, 'manager/update/update_resultado.html', context)

def criar_lance(request):
    if request.method == 'POST':
        jogador = get_object_or_404(Jogador, pk=request.POST['jogador'])
        partida = get_object_or_404(Partida, pk=request.POST['partida'])
        equipe = get_object_or_404(Equipe, pk=jogador.equipe.pk)
        lance = request.POST['lance']
        desc = request.POST['desc']
        tempo = request.POST['tempo']
        minuto = request.POST['minuto']
        l = Lance(jogador=jogador, partida=partida, lance=lance, equipe=equipe, descricao=desc, tempo=tempo, minuto=minuto)
        l.save()
        l.update()        
        return HttpResponse('')

# @login_required(login_url='/manager/login/')
# def gerar_partidas(request, pk):  
#     teams = []
#     partidas = []
#     grupos = list(Grupo.objects.filter(campeonato=pk))
#     equipes = Equipe.objects.all()
#     if len(grupos) == 1:
#         grupos = get_object_or_404(Grupo, campeonato=pk)
#         teams = list(Equipe.objects.filter(grupo=grupos))
#         partidas = gerarP(teams, grupos, pk)
#         #tmp = gerarP(list(reversed(teams)), grupos, pk)
#         #partidas += tmp
#     else:        
#         for g in grupos:
#             aux = list(Equipe.objects.filter(grupo=g))
#             teams += aux
#         partidas = gerarC(teams, grupos, pk)            

#     if request.method == 'POST':        
#         for p in partidas:
#             p.save()
#         return redirect('list_partida', pk=pk)
#     return render(request, 'manager/create/gerar_partidas.html', {'partidas':partidas})

@login_required(login_url='/manager/login/')
def create_grupo(request, pk):
    if request.method == 'POST':
        form = CreateGrupo(request.POST or None)
        if form.is_valid():
            nome = request.POST['nome']
            campeonato = get_object_or_404(Campeonato,pk=request.POST['campeonato'])
            g = Grupo(nome=nome, campeonato=campeonato)
            g.save()
            return redirect('list_grupo', pk=pk)

    return render(request, 'manager/create/add_grupo.html', {'pk':pk})

@login_required(login_url='/manager/login/')
def grupo_list(request, pk):
    champ = get_object_or_404(Campeonato, pk=pk)
    grupos = Grupo.objects.filter(campeonato=pk).order_by('nome')
    return render(request, 'manager/read/listar_grupos.html', {'grupos':grupos, 'pk':pk, 'champ':champ})

@login_required(login_url='/manager/login/')
def grupo_remove(request, c, pk):
    grupo = get_object_or_404(Grupo, pk=pk)
    if request.method == "POST":
        grupo.delete()
        return redirect('list_grupo', pk=c)
    return render(request, 'manager/delete/confirm_delete_grupo.html', {'grupo': grupo})

@login_required(login_url = '/manager/login/')
def grupo_edit(request, c, pk):
    grupo = get_object_or_404(Grupo, pk = pk)
    if request.method == 'POST':
        form = UpdateGrupo(request.POST, instance = grupo)
        if form.is_valid():
            grupo.save()
            return redirect('list_grupo', pk = c)
    else:
        form = UpdateGrupo(instance = grupo)

    return render(request, 'manager/update/editar_grupo.html', {'form': form})