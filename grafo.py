"""Trabalho da Disciplina de Grafos."""
from pprint import pprint
from math import ceil


def buble(lst):
    """."""
    ok = False
    if all(list(map(lambda x: x.isnumeric(), lst))):
        lst = list(map(int, lst))
    while not ok:
        ok = True
        for i in range(len(lst)-1):
            if lst[i] > lst[i+1]:
                lst[i], lst[i+1] = lst[i+1], lst[i]
                ok = False
    lst = list(map(str, lst))
    return lst


def CriaGrafo() -> (int, int, dict):
    """Recebe e cria o Grafo."""
    v, e = [int(i) for i in input().split()]
    grafo = dict()
    ent = []
    for i in range(e):
        ent.append(input().split())
        grafo[ent[-1][0]] = []
        grafo[ent[-1][1]] = []
    for v1, v2 in ent:
        grafo[v1].append(v2)
    return v, e, grafo


def dfs(g: dict, vi=None, conexo=False) -> (list or dict):
    """Faz a Busca em Profundide.

    cor: 0=branco, 1=cinza, 2=preto
    """
    class vertice:
        """Estrura de Vertice usado na DFS."""

        def __init__(self, cor, ti, tf):
            """Inicia o Vertice."""
            self.cor = cor
            self.ti = ti
            self.tf = tf

        def __repr__(self):
            """Representação do Vertice."""
            return f"vertice(cor={self.cor}, ti={self.ti}, tf={self.tf})"
    tabela = {i: vertice(0, 0, 0) for i in g.keys()}
    if vi is None:
        grau = list(
            map(lambda x: x,
                map(lambda x: [x[0], len(x[1])], g.items())))
        for i in grau:
            for j in g.items():
                i[1] += len(list(filter(lambda x: x == i[0], j[1])))
        grau = sorted(grau, key=lambda x: x[1], reverse=True)
        g1 = [[grau[0]]]
        for i in grau[1:]:
            if i[-1] == g1[-1][-1][-1]:
                g1[-1].append(i)
            else:
                g1.append([i])
        for i in range(len(g1)):
            g1[i] = list(map(lambda x: x[0], g1[i]))
        for i in range(len(g1)):
            g1[i] = sorted(g1[i])
        g1 = [buble(k) for k in g1]
        grau = [j for i in g1 for j in i]
    else:
        grau = vi
    nomeAresta = {i: [[k] for k in j] for i, j in g.items()}
    r = grau.pop(0)
    t = 0
    while len(grau) > 0 or not (r is None):
        tabela[r].cor = 1
        tabela[r].ti = t = t+1
        p = [r]
        while len(p) > 0:
            u = p[-1]
            cont = 0
            verificaCinza = True
            for i in sorted(g[u]):
                if tabela[i].cor == 1:
                    for l in nomeAresta[u]:
                        if l[-1] == i:
                            l.append('Retorno')
                if tabela[i].cor == 2:
                    for l in nomeAresta[u]:
                        if l[-1] == i and tabela[u].ti < tabela[i].ti:
                            l.append('Avanco')
                        if l[-1] == i and tabela[u].ti > tabela[i].ti:
                            l.append('Cruzamento')
                if tabela[i].cor == 0 and verificaCinza:
                    tabela[i].cor = 1
                    p.append(i)
                    grau.pop(grau.index(i))
                    tabela[i].ti = t = t+1
                    cont += 1
                    verificaCinza = False
                    for l in nomeAresta[u]:
                        if l[-1] == i:
                            l.append('Árvore')
            if cont == 0:
                tabela[u].cor = 2
                tabela[u].tf = t = t+1
                p.pop()
        if len(grau) > 0:
            r = grau.pop(0)
        else:
            r = None
    if not conexo:
        print("DFS:")
        for i, j in sorted(nomeAresta.items(), key=lambda x: x[0]):
            for k in j:
                print(f"{i} {k[0]}: {k[1]}")
        ordTop = list(map(lambda x: x[0],
                          sorted(tabela.items(), key=lambda x: x[-1].tf, reverse=True)))
        ordTopRetorno = ordTop[::]
        print("Ordenação Topologica:", ' '.join(ordTop))
        conexos = dfs(gt(g), vi=ordTop, conexo=True)
        gr = list(sorted(map(lambda x: (x[0], x[1].ti), conexos.items()),
                         key=lambda x: x[1]))
        x = [[gr[0]]]
        for i in gr[1:]:
            if x[-1][-1][-1] == i[-1]-1:
                x[-1].append(i)
            else:
                x.append([])
                x[-1].append(i)
        x = list(map(lambda y: list(map(lambda z: z[0], y)), x))
        print(f'Componentes Conexas: {len(x)} componentes.', '; '.join([str(i) for i in x]))
        return ordTopRetorno
    else:
        return tabela


def bfs(g: dict, ordTop: list):
    """Faz a Busca em Largura.

    cor: 0=branco, 1=cinza, 2=preto
    """
    class vertice:
        """Estrura de Vertice usado na BFS."""

        def __init__(self, cor, d, p):
            """Inicia o Vertice."""
            self.cor = cor
            self.d = d
            self.p = p

        def __repr__(self):
            """Representação do Vertice."""
            return f"vertice(cor={self.cor}, d={self.d}, p={self.p})"
    print("BFS:")
    tabela = {i: vertice(0, None, None) for i in g.keys()}
    s = ordTop[ceil(len(ordTop)/2)-1]
    tabela[s].cor = 1
    tabela[s].d = 0
    q = [s]
    while len(q) > 0:
        u = q.pop(0)
        for v in g[u]:
            if tabela[v].cor == 0:
                tabela[v].cor = 1
                tabela[v].d = tabela[u].d+1
                tabela[v].p = u
                q.append(v)
        tabela[u].cor = 2
    c = 'inf'
    for i in sorted(tabela.items(), key=lambda x: x[0]):
        print(f"{i[0]}: {i[1].d if not (i[1].d is None) else c} -> ", end='')
        if i[1].p is None:
            print('null', end='')
        else:
            l = [i[0]]
            while not (l[-1] is None):
                l.append(tabela[l[-1]].p)
            print('-'.join(filter(lambda x: not (x is None), l[::-1])), end='')
        print()
    print()


def gt(g: dict) -> dict:
    """Retorna o Transposto do Grafo."""
    gt = {i: [] for i in g.keys()}
    for i, j in g.items():
        for k in j:
            gt[k].append(i)
    return gt

v, e, g = CriaGrafo()
ordTop = dfs(g)
bfs(g, ordTop)
