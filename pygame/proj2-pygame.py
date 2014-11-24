import random
import copy
from random import random
import interface

import inspect

filtros = {
    "coordenadas": 
        lambda x, y: isinstance(x, int) and isinstance(y,int) and x > 0 and x <= tamanho and y > 0 and y <= tamanho,
    "coordenada": 
        lambda x: isinstance(x, tuple) and len(x) == 2 and all(isinstance(num, int) for num in x),
    "bloco": 
        lambda x: isinstance(x, int) and x >= 0 and ((x & (x - 1)) == 0),
    "tabuleiro": 
        lambda x: isinstance(x, list) and len(x) == 2 and isinstance(x[0], int) and isinstance(x[1], list) and len(
            x[1])==tamanho and all(isinstance(num, int) and len(linha) == tamanho for linha in x[1] for num in linha),
    "jogada": 
        lambda x: isinstance(x, str) and all(jogada in vetores for jogada in x.split(",")),
    "vazios":
        lambda x: x == 0,
    "disponiveis":
        lambda x: x != 0
}
vetores = {
    "N": {"x": -1, "y": 0},
    "S": {"x": 1, "y": 0},
    "E": {"x": 0, "y": 1},
    "W": {"x": 0, "y": -1}
}
tamanho = 4
blocosIniciais = 2

def erro():
    return ValueError(inspect.stack()[1][3]+": argumentos invalidos")

def cria_coordenada(x, y):
    if not filtros["coordenadas"](x, y):
        raise erro()
    return (x, y)

def e_coordenada(coordenada):
    return filtros["coordenada"](coordenada)

def coordenada_linha(coordenada):
    if not e_coordenada(coordenada):
        raise erro()
    return coordenada[0]

def coordenada_coluna(coordenada):
    if not e_coordenada(coordenada):
        raise erro()
    return coordenada[1]

def coordenada_igual(coordenada1, coordenada2):
    if not e_coordenada(coordenada1) or not e_coordenada(coordenada2):
        raise erro()
    return coordenada1 == coordenada2

def cria_tabuleiro():
    tabuleiro = []
    for x in range(0, tamanho):
        tabuleiro.append([])
        for y in range(0, tamanho):
            tabuleiro[x].append(0)
    return [0, tabuleiro]

def tabuleiro_pontuacao(tabuleiro):
    if not e_tabuleiro(tabuleiro):
        raise erro()
    return tabuleiro[0]

def tabuleiro_posicao(tabuleiro, coordenada):
    if not e_tabuleiro(tabuleiro) or not e_coordenada(coordenada):
        raise erro()
    return tabuleiro[1][coordenada_linha(coordenada) - 1][coordenada_coluna(coordenada) - 1]

def tabuleiro_posicoes_vazias(tabuleiro):
    return tabuleiro_filtra_blocos(tabuleiro, filtros["vazios"])

def tabuleiro_preenche_posicao(tabuleiro, coordenada, bloco):
    if not e_tabuleiro(tabuleiro) or not e_coordenada(coordenada) or not filtros["bloco"](bloco):
        raise erro()
    tabuleiro[1][coordenada_linha(coordenada) - 1][coordenada_coluna(coordenada) - 1] = bloco
    return tabuleiro

def tabuleiro_preenche_aleatorio(tabuleiro):
    if not e_tabuleiro(tabuleiro):
        raise erro()
    vazias = tabuleiro_posicoes_vazias(tabuleiro)
    coordenada = vazias[int(random() * len(vazias))]
    bloco = 2 if random() < 0.90 else 4
    return tabuleiro_preenche_posicao(tabuleiro, coordenada, bloco)

def tabuleiro_actualiza_pontuacao(tabuleiro, pontuacao):
    if not e_tabuleiro(tabuleiro) or not filtros["bloco"](pontuacao):
        raise erro()
    tabuleiro[0] = tabuleiro_pontuacao(tabuleiro) + pontuacao
    return tabuleiro

def e_tabuleiro(tabuleiro):
    return filtros["tabuleiro"](tabuleiro)

def tabuleiros_iguais(tabuleiro1, tabuleiro2):
    if not e_tabuleiro(tabuleiro1) or not e_tabuleiro(tabuleiro2):
        raise erro()
    return tabuleiro1 == tabuleiro2

def escreve_tabuleiro(tabuleiro):
    if not e_tabuleiro(tabuleiro):
        raise erro()
    for x in range(1, tamanho + 1):
        for y in range(1, tamanho + 1):
            print("[ " + str(tabuleiro_posicao(tabuleiro, cria_coordenada(x, y))) + " ]", end=" ")
        print()
    print("Pontuacao:", tabuleiro_pontuacao(tabuleiro))

def tabuleiro_jogada_possivel(tabuleiro, jogadas="N,S,E,W"):
    if not e_tabuleiro(tabuleiro) or not filtros["jogada"](jogadas):
        raise erro()
    disponiveis = tabuleiro_filtra_blocos(tabuleiro, filtros["disponiveis"])
    for atual in disponiveis:
        for jogada in jogadas.split(","):
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
    if not e_tabuleiro(tabuleiro):
        raise erro()
    coordenadas = []
    for x in range(1, tamanho + 1):
        for y in range(1, tamanho + 1):
            if filtro(tabuleiro_posicao(tabuleiro, cria_coordenada(x, y))):
                coordenadas.append(cria_coordenada(x, y))
    return coordenadas

def tabuleiro_terminado(tabuleiro):
    if not e_tabuleiro(tabuleiro):
        raise erro()
    return len(tabuleiro_posicoes_vazias(tabuleiro)) == 0 and not tabuleiro_jogada_possivel(tabuleiro)

def tabuleiro_adiciona_blocos_inicias(tabuleiro):
    for i in range(0, blocosIniciais):
        tabuleiro_preenche_aleatorio(tabuleiro)
    return tabuleiro

def pede_jogada():
    jogada = input("Introduza uma jogada (N, S, E, W): ")
    if not filtros["jogada"](jogada):
        print("Jogada invalida.")
        return pede_jogada()
    return jogada

def tabuleiro_reduz(tabuleiro, jogada, junta=True):
    if not e_tabuleiro(tabuleiro) or not filtros["jogada"](jogada):
        raise erro()
    if tabuleiro_jogada_possivel(tabuleiro, jogada):
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

        if junta:
            # Se tivermos da da direita para a esquerda ou de cima para baixo temos que usar outro iterador
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
            return tabuleiro_reduz(tabuleiro, jogada, False)
    return tabuleiro

def desenha_tabuleiro(w, t):
    ''' desenha_tabuleiro : janela x tabuleiro -> {}
        desenha_tabuleiro(t) desenha na janela de jogo o tabuleiro de 2048 t.'''
    
    if not e_tabuleiro(t):
        raise ValueError ('escreve_tabuleiro: argumentos invalidos')

    for x in range(1, tamanho+1):
        for y in range(1, tamanho+1):
            w.draw_tile(tabuleiro_posicao(t, cria_coordenada(x, y)), x, y)

def desenha_score(w, t):
    w.draw_score(tabuleiro_pontuacao(t), 245, 165)
        
def bot(t):
    if not tabuleiro_jogada_possivel(t, "N"):
        if tabuleiro_jogada_possivel(t, "E") and tabuleiro_jogada_possivel(t, "W"):
            leftUp = copy.deepcopy(t)
            rightUp = copy.deepcopy(t)
            tabuleiro_reduz(leftUp, "W")
            tabuleiro_reduz(leftUp, "N")
            tabuleiro_reduz(rightUp, "E")
            tabuleiro_reduz(rightUp, "N")
            if len(tabuleiro_posicoes_vazias(leftUp)) > len(tabuleiro_posicoes_vazias(rightUp)):
                return "W"
            return "E"
        elif tabuleiro_jogada_possivel(t, "W"):
            return "W"
        elif tabuleiro_jogada_possivel(t, "E"):
            return "E"
        else:
            return "S"
    return "N"

def nextMove(board,recursion_depth=3):
    def nextMoveRecur(board,depth,maxDepth,base=0.9):
        bestScore = -1.
        bestMove = 0
        for m in vetores:
            if(tabuleiro_jogada_possivel(board, m)):
                newBoard = copy.deepcopy(board)
                tabuleiro_reduz(newBoard, m)
                tabuleiro_preenche_aleatorio(newBoard)
                 
                score = tabuleiro_pontuacao(newBoard)
                if depth != 0:
                    my_m,my_s = nextMoveRecur(newBoard,depth-1,maxDepth)
                    score += my_s*pow(base,maxDepth-depth+1)
                     
                if(score > bestScore):
                    bestMove = m
                    bestScore = score
        return (bestMove,bestScore);
    m,s = nextMoveRecur(board,recursion_depth,recursion_depth)
    return m

def tabuleiro_ganhou_jogo(t):
    return any(2048==tabuleiro_posicao(t, c) for c in tabuleiro_filtra_blocos(t, filtros["disponiveis"]))


def joga_2048():
    '''...'''
     
    def loop():
        t = cria_tabuleiro()
        tabuleiro_adiciona_blocos_inicias(t)
        quit = False
        while not quit:
            jogada = w.get_play()
            if jogada == "Q":
                return "Q"

            desenha_tabuleiro(w, t)

            while not quit and not tabuleiro_ganhou_jogo(t):
                desenha_tabuleiro(w, t)
                desenha_score(w, t)

                jogada = w.get_play()
                if jogada == "Q":
                    return "Q"

                play = nextMove(t,2)
                if filtros["jogada"](play):
                    if tabuleiro_jogada_possivel(t, play):
                        tabuleiro_reduz(t, play)
                        tabuleiro_preenche_aleatorio(t)

                if tabuleiro_terminado(t):
                    break

                w.step()

            if tabuleiro_terminado(t):
                break
        return None

    times = 1
    w = interface.window_2048()
    quit = False
    while not quit:
        state = loop()
        if state == None:
            times+=1
        if state == "Q":
            quit = True

    print('Jogo terminado. Foi executado', times, "vez(es)!")
    
if __name__ == "__main__":
    joga_2048()
