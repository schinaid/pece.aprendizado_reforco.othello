"""
Jogador heurístico baseado em mobilidade.
"""

import numpy as np
from utils.avaliador import diferenca_mobilidade

class JogadorHeuristico:
    def __init__(self):
        pass

    def escolher_jogada(self, jogo, jogador):
        jogadas = jogo.movimentos_validos(jogador)
        melhor_jogada = None
        melhor_valor = -np.inf
        for jogada in jogadas:
            copia = jogo.clone()
            copia.aplica_jogada(jogada, jogador)
            valor = diferenca_mobilidade(copia, jogador)
            if valor > melhor_valor:
                melhor_valor = valor
                melhor_jogada = jogada
        return melhor_jogada

def cria_jogador():
    return JogadorHeuristico()
