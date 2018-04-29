import math
import random
from app.models import *

# Função para rotacionar a lista em sentido horário
def rotacionar(lista, n):
    return lista[n:] + lista[:n]

# Gerar partidas entre times de um campeonato do tipo Todos contra Todos
def gerarP(lista, g, c):
    """
    Gera partidas entre times de um campeonato do tipo Todos contra Todos.    
    """
    aux = []
    times = lista
    #random.shuffle(times)
    n = len(times)
    h = math.ceil(n/2)
    fist = times[:1]    
    # Monta as rodadas
    for i in range(0, n-1):        
        # Caso seja a primeira rodada
        if i == 0:
            # Divide a lista em duas partes
            lista1 = times[:int(h)]
            lista2 = times[int(h):]
            lista2.reverse()
            
            # Percorre a lista montando as partidas
            for x in range(0, h):
                #print('%s vs %s' % (lista1[x], lista2[x]))                
                if i % 2 == 0:
                    p = Partida(mandante=lista2[x], visitante=lista1[x], rodada=(i+1), grupo=g, campeonato=c)
                    aux.append(p)
                else:
                    p = Partida(mandante=lista1[x], visitante=lista2[x], rodada=(i+1), grupo=g,campeonato=c)
                    aux.append(p)                
        else:            
            times = rotacionar(times[1:], 1)
            times = fist + times
            lista1 = times[:int(h)]               
            lista2 = times[int(h):]
            lista2.reverse()
            
             # Percorre a lista montando as partidas
            for x in range(0, h):                                        
                if x == 1:
                    p = Partida(mandante=lista2[x], visitante=lista1[x], rodada=(i+1), grupo=g,campeonato=c)
                    aux.append(p)
                elif i % 2 == 0:
                    p = Partida(mandante=lista2[x], visitante=lista1[x], rodada=(i+1), grupo=g,campeonato=c)
                    aux.append(p)
                else:
                    p = Partida(mandante=lista1[x], visitante=lista2[x], rodada=(i+1), grupo=g,campeonato=c)
                    aux.append(p)
        
    return aux

# Gerar partidas para a fase de grupos de um campeonato do tipo Copa
def gerarC(lista, g, c):
    """
    Gera partidas para a fase de grupos de um campeonato do tipo Copa.
    """
    aux = []    
    times = lista

    for grupo in g:
        timesG = []
        for t in times:
            if t.grupo == grupo:
                timesG.append(t)
        print(timesG)
        n = len(timesG)
        h = math.ceil(n/2)
        fist = timesG[:1]    
        # Monta as rodadas
        for i in range(0, n-1):            
            # Caso seja a primeira rodada
            lista1 = []
            lista2 = []
            if i == 0:
                # Divide a lista em duas partes
                lista1 = timesG[:int(h)]                
                lista2 = timesG[int(h):]
                lista2.reverse()                
                # Percorre a lista montando as partidas
                for x in range(0, h):                                   
                    p = Partida(mandante=lista1[x], visitante=lista2[x], rodada=(i+1), grupo=grupo,campeonato=c)                                
                    aux.append(p)                
            else:            
                timesG = rotacionar(timesG[1:], 1)                
                timesG = fist + timesG                
                lista1 = timesG[:int(h)]               
                lista2 = timesG[int(h):]
                lista2.reverse()
                
                # Percorre a lista montando as partidas
                for x in range(0, h):                                           
                    p = Partida(mandante=lista1[x], visitante=lista2[x], rodada=(i+1), grupo=grupo,campeonato=c)                                
                    aux.append(p)
        
    return aux