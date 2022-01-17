class FaseDTO(object):
    def __init__(self, nome, partidas):
        self.nome = nome
        self.partidas = partidas


class FaseCampeonatoDTO(object):
    def __init__(self, nome, pk, fases):
        self.nome = nome
        self.pk = pk
        self.fases = fases

    def __str__(self):
        return self.nome
