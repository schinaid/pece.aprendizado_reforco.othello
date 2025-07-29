
import numpy as np

def mobilidade(jogo, jogador):
    '''
    Calcula o número de jogadas legais do jogador.
    '''
    jogo_clone = jogo if jogo.jogador_atual() == jogador else jogo.joga(None)
    return len(jogo_clone.jogadas_legais())

def diferenca_mobilidade(jogo, jogador):
    '''
    Calcula a diferença entre jogadas legais do jogador e do oponente.
    '''
    return mobilidade(jogo, jogador) - mobilidade(jogo, -jogador)

def vantagem_posicional(tabuleiro, pesos):
    '''
    Aplica pesos a cada posição do tabuleiro e calcula soma total.

    Argumentos:
    - tabuleiro: numpy array 8x8
    - pesos: numpy array 8x8

    Retorno:
    - valor escalar da soma ponderada
    '''
    return np.sum(tabuleiro * pesos)
