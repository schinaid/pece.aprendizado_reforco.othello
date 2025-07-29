"""
Jogador com Minimax e profundidade fixa.
"""

import numpy as np
from utils.avaliador import diferenca_mobilidade

class JogadorMinimax:
    def __init__(self, profundidade=3):
        self.profundidade = profundidade

    def escolher_jogada(self, jogo, jogador):
        _, jogada = self._minimax(jogo, jogador, self.profundidade, True)
        return jogada

    def _minimax(self, jogo, jogador, profundidade, maximizando):
        if profundidade == 0 or jogo.fim_de_jogo():
            return diferenca_mobilidade(jogo, jogador), None

        jogadas = jogo.movimentos_validos(jogador if maximizando else 1 - jogador)
        if not jogadas:
            return diferenca_mobilidade(jogo, jogador), None

        melhor_valor = -np.inf if maximizando else np.inf
        melhor_jogada = None
        for jogada in jogadas:
            copia = jogo.clone()
            copia.aplica_jogada(jogada, jogador if maximizando else 1 - jogador)
            valor, _ = self._minimax(copia, jogador, profundidade - 1, not maximizando)
            if (maximizando and valor > melhor_valor) or (not maximizando and valor < melhor_valor):
                melhor_valor = valor
                melhor_jogada = jogada
        return melhor_valor, melhor_jogada

def cria_jogador():
    return JogadorMinimax()
