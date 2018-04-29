import math

def gerarPartidas(times):
    n = len(times)
    h = math.ceil(n/2)
    fist = times[:1]

    print("Numero de times = %s" % (n))
    print("Numero de rodadas = %s" % ((n*2) - 2))
    print("Numero de partidas = %s" % (int(n * (n - 1) / 2)))

    # Monta as rodadas
    for i in range(0, n-1):
        print("\nRodada %s" % (i + 1))
        # Caso seja a primeira rodada
        if i == 0:
            # Divide a lista em duas partes
            lista1 = times[:int(h)]
            lista2 = times[int(h):]
            
            # Percorre a lista montando as partidas
            for x in range(0, h):
                print('%s vs %s' % (lista1[x], lista2[x]))

        else:            
            times = rotacionar(times[1:], 1)
            times = fist + times
            lista1 = times[:int(h)]               
            lista2 = times[int(h):]
            
             # Percorre a lista montando as partidas
            for x in range(0, h):
                print('%s vs %s' % (lista1[x], lista2[x]))

def rotacionar(lista, n):
    return lista[n:] + lista[:n]

times = [
    'Atl. Goianiense',
    'Atl. Mineiro',
    'Atl. Paranaense',
    'Avaí',
    'Bahia',
    'Botafogo',
    'Chapecoense',
    'Corinthians',
    'Coritiba',
    'Cruzeiro',
    'Flamengo',
    'Fluminense',
    'Gremio',
    'Palmeiras',
    'Ponte Preta',
    'Santos',
    'São Paulo',
    'Sport',
    'Vasco',
    'Vitoria'
    ]

gerarPartidas(times)

print('------------------------------------------\n')
times = [
    'Atl. Goianiense',
    'Atl. Mineiro',
    'Atl. Paranaense',
    'Avaí',
    'Bahia',
    'Botafogo',
    'Chapecoense',
    'Corinthians',
    'Coritiba',
    'Cruzeiro',
    'Flamengo',
    'Fluminense',
    'Gremio',
    'Palmeiras',
    'Ponte Preta',
    'Santos',
    'São Paulo',
    'Sport',
    'Vasco',
    'Vitoria'
    ]

gerarPartidas(list(reversed(times)))
