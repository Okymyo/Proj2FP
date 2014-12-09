# Grupo 10
# Andre Mendes n.82047, Joao Genebra n.82007, Nuno Anselmo n.81900
from random import random
from copy import deepcopy
from inspect import stack

import time

filtros = {
    "coordenadas": 
        lambda x, y: isinstance(x, int) and isinstance(y,int) and x > 0 and x <= tamanho and y > 0 and y <= tamanho,
    "coordenada": 
        lambda x: isinstance(x, tuple) and len(x) == 2 and filtros["coordenadas"](x[0], x[1]) 
        and all(isinstance(num, int) for num in x),
    "bloco": 
        lambda x: isinstance(x, int) and ((x & (x - 1)) == 0),
    "pontuacao":
        lambda x: isinstance(x, int) and x>=0 and x%4==0,
    "tabuleiro": 
        lambda x: isinstance(x, list) and len(x) == 2 and isinstance(x[0], int) and isinstance(x[1], list) and len(
            x[1])==tamanho and all(isinstance(num, int) and len(linha) == tamanho for linha in x[1] for num in linha),
    "jogada": 
        lambda x: isinstance(x, str) and x in vetores,
    "vazios":
        lambda x: x == 0,
    "disponiveis":
        lambda x: x != 0,
    "vencedor":
        lambda x : x == blocoVencedor
}

vetores = {
    "N": {"x": -1, "y": 0},
    "S": {"x": 1, "y": 0},
    "E": {"x": 0, "y": 1},
    "W": {"x": 0, "y": -1}
}

tamanho = 4
blocosIniciais = 2
probabilidadeBlocoDois = 0.8
blocoVencedor = 2048

def erro():
    return ValueError(stack()[1][3]+": argumentos invalidos")

def cria_coordenada(x, y):
    '''
    Cria nova coordenada com os parametros dados
    :param x: Linha da coordenada a criar : int
    :param y: Coluna da coordenada a criar : int
    :return: Coordenada criada a partir dos parametros que foram dados : Coordenada
    '''
    if not filtros["coordenadas"](x, y):
        raise erro()
    return (x, y)
    
def e_coordenada(coordenada):
    '''
    Verifica se a coordenada dada respeita a definicao de coordenada
    :param coordenada: Coordenada a verificar : Coordenada
    :return: True se for uma coordenada, False se nao o for : boolean
    '''    
    return filtros["coordenada"](coordenada)
    
def coordenada_linha(coordenada):
    '''
    Retorna a linha da coordenada dada
    :param coordenada: Coordenada a qual se obtem a linha : Coordenada
    :return: Linha da coordenada dada como parametro : int
    '''    
    if not e_coordenada(coordenada):
        raise erro()
    return coordenada[0]
    
def coordenada_coluna(coordenada):
    '''
    Retorna a coluna da coordenada dada
    :param coordenada: Coordenada a qual se obtem a coluna : Coordenada
    :return: Coluna da coordenada dada como parametro : int
    '''
    if not e_coordenada(coordenada):
        raise erro()
    return coordenada[1]
    
def coordenadas_iguais(coordenada1, coordenada2):
    '''
    Verifica se ambas as coordenadas sao iguais
    :param coordenada1: Primeira coordenada a comparar : Coordenada
    :param coordenada2: Coordenada com a qual se compara a primeira : Coordenada
    :return: True se ambas as coordenadas foram de facto iguais, False se nao o forem : boolean
    '''    
    if not(e_coordenada(coordenada1) and e_coordenada(coordenada2)):
        raise erro()
    return coordenada1 == coordenada2

def cria_tabuleiro():
    '''
    Cria um tipo de abstracao de dados do tipo tabuleiro, vazio e com pontuacao a 0
    :return: Tabuleiro vazio com pontuacao a 0 : Tabuleiro
    '''
    tabuleiro = []
    for x in range(0, tamanho):
        tabuleiro.append([])
        for y in range(0, tamanho):
            tabuleiro[x].append(0)
    return [0, tabuleiro]

def tabuleiro_pontuacao(tabuleiro):
    '''
    Devolve a pontuacao do tabuleiro dado
    :param tabuleiro: Tabuleiro ao qual queremos ver a pontuacao : Tabuleiro
    :return: Pontuacao do tabuleiro dado : int
    '''
    if not e_tabuleiro(tabuleiro):
        raise erro()
    return tabuleiro[0]

def tabuleiro_posicao(tabuleiro, coordenada):
    '''
    Devolve o valor do bloco na posicao coordenada num dado tabuleiro
    :param tabuleiro: Tabuleiro cujo qual queremos saber o valor numa dada posicao : Tabuleiro
    :param coordenada: Posicao cuja qual queremos saber o valor num dado tabuleiro : Coordenada
    :return: Valor do bloco na posicao coordenada num dado tabuleiro : int
    '''
    if not e_tabuleiro(tabuleiro) or not e_coordenada(coordenada):
        raise erro()
    return tabuleiro[1][coordenada_linha(coordenada) - 1][coordenada_coluna(coordenada) - 1]

def tabuleiro_posicoes_vazias(tabuleiro):
    '''
    Devolve uma lista das coordenadas de um dado tabuleiro que se encontram vazias
    :param tabuleiro: Tabuleiro cujo qual queremos saber as posicoes vazias : Tabuleiro
    :return: Lista das posicoes vazias de um dado tabuleiro : list
    '''
    return tabuleiro_filtra_blocos(tabuleiro, filtros["vazios"])

def tabuleiro_preenche_posicao(tabuleiro, coordenada, bloco):
    '''
    Preenche o tabuleiro com o valor do bloco dado, numa dada coordenada, num dado tabuleiro
    :param tabuleiro: Tabuleiro cujo qual queremos preencher uma posicao : Tabuleiro
    :param coordenada: Coordenada da posicao a preencher no tabuleiro : Coordenada
    :param bloco: Valor que queremos que o tabuleiro assuma numa dada coordenada : int
    :return: Tabuleiro atualizado com a posicao preenchida : Tabuleiro
    '''
    if not e_tabuleiro(tabuleiro) or not e_coordenada(coordenada) or not filtros["bloco"](bloco):
        raise erro()
    tabuleiro[1][coordenada_linha(coordenada) - 1][coordenada_coluna(coordenada) - 1] = bloco
    return tabuleiro

def tabuleiro_preenche_aleatorio(tabuleiro):
    '''
    Preenche o tabuleiro com um bloco aleatorio (2 ou 4), numa posicao vazia aleatoria
    :param tabuleiro: Tabuleiro a preencher aleatoriamente uma posicao : Tabuleiro
    :return: Tabuleiro atualizado com a posicao preencheda : Tabuleiro
    '''
    if not e_tabuleiro(tabuleiro):
        raise erro()
    vazias = tabuleiro_posicoes_vazias(tabuleiro)
    coordenada = vazias[int(random() * len(vazias))]
    bloco = 2 if random() < probabilidadeBlocoDois else 4
    return tabuleiro_preenche_posicao(tabuleiro, coordenada, bloco)

def tabuleiro_actualiza_pontuacao(tabuleiro, pontuacao):
    '''
    Atualiza a pontuacao de um dado tabuleiro, somando uma pontuacao dada a pontuacao atual do mesmo
    :param tabuleiro: Tabuleiro a atualizar a pontuaca : Tabuleiro
    :param pontuacao: Pontuacao a somar a posicao atual do tabuleiro : int
    :return: Tabuleiro atualizado com a nova pontuacao : Tabuleiro
    '''
    if not e_tabuleiro(tabuleiro) or not filtros["pontuacao"](pontuacao):
        raise erro()
    tabuleiro[0] = tabuleiro_pontuacao(tabuleiro) + pontuacao
    return tabuleiro

def e_tabuleiro(tabuleiro):
    '''
    Verifica se um dado tabuleiro e efetivamente um tabuleiro ou nao
    :param tabuleiro: Tabuleiro a verificar se realmente e ou nao um tabuleiro : Tabuleiro
    :return: True se o tabuleiro dado for efetivamente do tipo Tabuleiro caso contrario False : boolean
    '''
    return filtros["tabuleiro"](tabuleiro)

def tabuleiros_iguais(tabuleiro1, tabuleiro2):
    '''
    Verifica se 2 tabuleiros sao ou ao iguais
    :param tabuleiro1: Um dos tabuleiros a verificar a igualdade com o outro : Tabuleiro
    :param tabuleiro2: Um dos tabuleiros a verificar a igualdade com o outro : Tabuleiro
    :return: True se os tabuleiros forem iguais caso contrario False : boolean
    '''
    if not e_tabuleiro(tabuleiro1) or not e_tabuleiro(tabuleiro2):
        raise erro()
    return tabuleiro1 == tabuleiro2

def escreve_tabuleiro(tabuleiro):
    '''
    Escreve o tabuleiro de forma apresentavel aos olhos do ser humano
    :param tabuleiro: Tabuleiro a escrever : Tabuleiro
    :return: None
    '''
    if not e_tabuleiro(tabuleiro):
        raise erro()
    for x in range(1, tamanho + 1):
        for y in range(1, tamanho + 1):
            print("[ " + str(tabuleiro_posicao(tabuleiro, cria_coordenada(x, y))) + " ]", end=" ")
        print()
    print("Pontuacao:", tabuleiro_pontuacao(tabuleiro))

def tabuleiro_jogada_possivel(tabuleiro, jogadas="N,S,E,W"):
    '''
    Verifica se a(s) jogada(s) dada(s) e/sao ou nao possivel/possiveis dado um tabuleiro
    :param tabuleiro: Tabuleiro a verificar se a(s) jogada(s) dada(s) e/sao ou nao possivel/possiveis : Tabuleiro
    :param jogadas: Jogadas separadas por virgula a averiguar se sao ou nao possiveis num dado tabuleiro : string
    :return: True se qualquer uma das jogadas for possivel, caso contrario False : boolean
    '''
    if not e_tabuleiro(tabuleiro):
        raise erro()
    disponiveis = tabuleiro_filtra_blocos(tabuleiro, filtros["disponiveis"])
    for jogada in jogadas.split(","):
        if not filtros["jogada"](jogada):
            raise erro()
    for atual in disponiveis:
        blocoAtual = tabuleiro_posicao(tabuleiro, atual)
        try:
            x,y = coordenada_linha(atual), coordenada_coluna(atual)
            vizinho = cria_coordenada(x + vetores[jogada]["x"], y + vetores[jogada]["y"])
            blocoVizinho = tabuleiro_posicao(tabuleiro, vizinho)
            if blocoVizinho == 0 or (blocoAtual == blocoVizinho):
                return True
        except ValueError:
            continue
    return False

def tabuleiro_filtra_blocos(tabuleiro, filtro):
    '''
    Devolve uma lista das coordenadas que cumpram um dado filtro
    :param tabuleiro: Tabuleiro a filtrar as coordenadas : Tabuleiro
    :param filtro: Funcao do tipo (x) => boolean utilizada para filtrar os blocos do Tabuleiro que a cumpram : function
    :return: Lista com as coordenadas que cumpriram o filtro dado : list
    '''
    if not e_tabuleiro(tabuleiro):
        raise erro()
    coordenadas = []
    for x in range(1, tamanho + 1):
        for y in range(1, tamanho + 1):
            if filtro(tabuleiro_posicao(tabuleiro, cria_coordenada(x, y))):
                coordenadas.append(cria_coordenada(x, y))
    return coordenadas

def tabuleiro_terminado(tabuleiro):
    '''
    Verifica se um tabuleiro esta ou nao terminado, se acabou ou nao o jogo
    :param tabuleiro: Tabuleiro a verificar se esta ou nao terminado : Tabuleiro
    :return: True se nao for possivel jogada alguma e se nao existirem posicoes vazias caso contrario False : boolean
    '''
    if not e_tabuleiro(tabuleiro):
        raise erro()
    return len(tabuleiro_posicoes_vazias(tabuleiro)) == 0 and not tabuleiro_jogada_possivel(tabuleiro)

def tabuleiro_ganhou_jogo(tabuleiro):
    '''
    Verifica se um tabuleiro ganhou ou nao o jogo
    :param tabuleiro: Tabuleiro a veriicar se ganhou ou nao o jogo : Tabuleiro
    :return: True se ganhou o jogo caso contrario False : boolean
    '''
    return len(tabuleiro_filtra_blocos(tabuleiro, filtros["vencedor"])) > 0

def tabuleiro_adiciona_blocos_inicias(tabuleiro):
    '''
    Adiciona ao tabuleiro blocosInicias blocos inicias
    :param tabuleiro: Tabuleiro a adicionar os blocos adicionais : Tabuleiro
    :return: Tabuleiro atualizado com os blocos iniciais adicionados : Tabuleiro
    '''
    for i in range(0, blocosIniciais):
        tabuleiro_preenche_aleatorio(tabuleiro)
    return tabuleiro

def tabuleiro_reduz(tabuleiro, jogada):
    '''
    Reduz um tabuleiro dado consoante uma jogada dada, seguindo as regras do jogo 2048
    :param tabuleiro: Tabuleiro cujo qual queremos aplicar a reducao : Tabuleiro
    :param jogada: Jogada cuja qual queremos utilizar para reduzir o tabuleiro : string
    :return: Tabuleiro reduzido consoante a jogada dada : Tabuleiro
    '''
    def empurra():
        '''
        Empurra todos os blocos consoante uma jogada, trocando entre si sempre que encontrarem um bloco vazio vizinho
        :return: Tabuleiro atualizado com todos os blocos vazios substituidos consoante a jogada dada : Tabuleiro
        '''
        trocaColuna = True
        while trocaColuna:
            trocaColuna = False
            for x in range(1,tamanho+1):
                trocaLinha = True
                while trocaLinha:
                    trocaLinha = False
                    for y in range(tamanho, 0, -1):
                        atual = cria_coordenada(x, y)
                        blocoAtual = tabuleiro_posicao(tabuleiro, atual)
                        try:
                            vizinho = cria_coordenada(x+vetores[jogada]["x"], y+vetores[jogada]["y"])
                            blocoVizinho = tabuleiro_posicao(tabuleiro, vizinho)
                            if blocoVizinho == 0 and blocoAtual != 0:
                                tabuleiro_preenche_posicao(tabuleiro, vizinho, blocoAtual)
                                tabuleiro_preenche_posicao(tabuleiro, atual, 0)
                                if coordenada_linha(atual) != coordenada_linha(vizinho):trocaColuna = True
                                else: trocaLinha = True
                        except ValueError:
                            continue
        return tabuleiro

    def junta():
        '''
        Junta todos os blocos vizinhos iguais por uma ordem especifica consoante a jogada dada
        :return: Tabuleiro atualizado com todos os blocos vizinhos somados, e com pontuacao atualizada : Tabuleiro
        '''
        iterador = range(1, tamanho+1) if vetores[jogada]["x"]+vetores[jogada]["y"] < 0 else range(tamanho, 0, -1)
        for x in iterador:
            for y in iterador:
                atual = cria_coordenada(x, y)
                blocoAtual = tabuleiro_posicao(tabuleiro, atual)
                try:
                    vizinho = cria_coordenada(x+vetores[jogada]["x"], y+vetores[jogada]["y"])
                    blocoVizinho = tabuleiro_posicao(tabuleiro, vizinho)
                    if blocoVizinho == blocoAtual:
                        novoBloco = blocoAtual+blocoVizinho
                        tabuleiro_preenche_posicao(tabuleiro, vizinho, novoBloco)
                        tabuleiro_preenche_posicao(tabuleiro, atual, 0)
                        tabuleiro_actualiza_pontuacao(tabuleiro, novoBloco)
                except ValueError:
                    continue
        return tabuleiro

    if not e_tabuleiro(tabuleiro) or not filtros["jogada"](jogada):
        raise erro()
    empurra()
    junta()
    empurra()
    return tabuleiro

def pede_jogada():
    '''
    Pede uma jogada ao jogador
    :return: Jogada dada se esta for valida : string
    '''
    jogada = input("Introduza uma jogada (N, S, E, W): ")
    if not filtros["jogada"](jogada):
        print("Jogada invalida.")
        return pede_jogada()
    return jogada

def nextMove(board,recursion_depth=3):
    '''
    Avalia a proxima jogada a executar consoante o tabuleiro atual e uma previsao do futuro
    :param board: Tabuleiro a avaliar : Tabuleiro
    :param recursion_depth: Depth do algoritmo, quantos tabuleiros tentamos prever : int
    :return: Melhor jogada, a que avalia qual da o melhor score depois de feita : string
    '''
    def nextMoveRecur(board,depth,maxDepth,base=probabilidadeBlocoDois):
        bestScore = -1.
        bestMove = 0
        for m in vetores:
            if(tabuleiro_jogada_possivel(board, m)):
                newBoard = deepcopy(board)
                tabuleiro_reduz(newBoard, m)
                tabuleiro_preenche_aleatorio(newBoard)

                score = tabuleiro_pontuacao(newBoard)
                if depth != 0:
                    my_m,my_s = nextMoveRecur(newBoard,depth-1,maxDepth)
                    score += my_s*pow(base,maxDepth-depth+1)

                if(score > bestScore):
                    bestMove = m
                    bestScore = score
        return (bestMove,bestScore)
    m,s = nextMoveRecur(board,recursion_depth,recursion_depth)
    return m

def jogo_2048():
    '''
    Jogo 2048
    :return: None
    '''
    t = cria_tabuleiro()
    tabuleiro_adiciona_blocos_inicias(t)
    while not(tabuleiro_terminado(t)):
        escreve_tabuleiro(t)
        j = pede_jogada() #Para a utilizacao de inteligencia artificial escrever "j = nextMove(t, recursionDepth)"
        if tabuleiro_jogada_possivel(t, j):
            tabuleiro_reduz(t, j)
            tabuleiro_preenche_aleatorio(t)
            
def benchmark(repeticoes, testes, funcao, *parametros):
    # Repeticoes: Numero de vezes que mede o tempo
    # Testes: Numero de vezes que corre a funcao por cada repeticao
    # Funcao: Nome da funcao a executar
    # Parametros: Todos os parametros
    # EX: benchmark(4, 100, tabuleiro_reduz, tab, "S")
    start_all = time.time()
    for i in range(0, repeticoes):
        start = time.time()
        for i in range(0, testes):
            funcao(*parametros)
        print(time.time() - start)
    return 'Corridos ' + str(repeticoes * testes) + ' testes, com total de ' + str(time.time() - start_all) + ' segundos'