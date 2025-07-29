
"""
IA Minimax com Poda Alfa-Beta para Othello (Competição 2025)

Autores:
- Anderson Alves Schinaid
- Jorge Filho
- Simone Britto

Descrição:
IA que utiliza Minimax com profundidade 3 e poda alfa-beta para escolher jogadas,
com fallback para heurística tradicional.
"""

import numpy as np
import time
from .utils.avaliador import diferenca_mobilidade

# Tabela de pesos posicionais do tabuleiro (cantos e bordas favorecidos)
HEURISTICA_POSICIONAL = np.array([
    [100, -20, 10, 5, 5, 10, -20, 100],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [5, -2, -1, -1, -1, -1, -2, 5],
    [10, -2, -1, -1, -1, -1, -2, 10],
    [-20, -50, -2, -2, -2, -2, -50, -20],
    [100, -20, 10, 5, 5, 10, -20, 100]
])

class JogadorMinimax:
    """
    IA baseada em Minimax com fallback para heurística rápida.
    """

    def __init__(self):
        """Inicializa o jogador e define o tempo limite de busca."""
        self.jogador = None
        self.id_oponente = None
        self.limite_tempo = 0.1  # Tempo máximo para escolher jogada (100ms)
        self.inicio_busca = None

    def nova_partida(self, jogo, jogador, id_oponente=None):
        """
        Notifica a IA do início de uma nova partida.

        Parâmetros:
        - jogo: objeto da classe Othello com o estado inicial do jogo
        - jogador: inteiro (1 ou -1) representando o lado da IA
        - id_oponente: identificador opcional do oponente

        Retorno: None
        """
        self.jogador = jogador
        self.id_oponente = id_oponente

    def avalia(self, jogo):
        """
        Avalia o estado do jogo com base em:
        - Posição das peças
        - Quantidade de peças ganhas
        - Mobilidade relativa

        Parâmetros:
        - jogo: objeto da classe Othello representando o estado atual

        Retorno:
        - valor (float): escore heurístico do estado
        """
        tab = jogo.tabuleiro()
        valor_pos = np.sum(tab * HEURISTICA_POSICIONAL * self.jogador)
        ganho = jogo.placar(self.jogador) - jogo.placar(-self.jogador)
        mobil = diferenca_mobilidade(jogo, self.jogador)
        return valor_pos + ganho * 10 + mobil * 2

    def minimax(self, jogo, profundidade, alfa, beta, maximizando):
        """
        Algoritmo Minimax com poda alfa-beta.

        Parâmetros:
        - jogo: estado atual do jogo (classe Othello)
        - profundidade: profundidade máxima da busca
        - alfa: valor alfa para poda
        - beta: valor beta para poda
        - maximizando: booleano indicando se é o turno da IA

        Retorno:
        - (valor, jogada): tupla com valor da avaliação e melhor jogada encontrada
        """
        if time.time() - self.inicio_busca > self.limite_tempo or profundidade == 0 or jogo.terminou():
            return self.avalia(jogo), None

        melhor_valor = float('-inf') if maximizando else float('inf')
        melhor_jogada = None
        jogadas = jogo.jogadas_legais()

        for jogada in jogadas:
            filho = jogo.joga(jogada)
            valor, _ = self.minimax(filho, profundidade - 1, alfa, beta, not maximizando)

            if maximizando:
                if valor > melhor_valor:
                    melhor_valor = valor
                    melhor_jogada = jogada
                alfa = max(alfa, valor)
                if beta <= alfa:
                    break
            else:
                if valor < melhor_valor:
                    melhor_valor = valor
                    melhor_jogada = jogada
                beta = min(beta, valor)
                if beta <= alfa:
                    break

        return melhor_valor, melhor_jogada

    def escolhe_jogada(self, jogo):
        """
        Escolhe a melhor jogada usando Minimax com fallback heurístico.

        Parâmetros:
        - jogo: objeto Othello representando o estado atual

        Retorno:
        - jogada (tupla): coordenada da jogada escolhida (linha, coluna)
        """
        self.inicio_busca = time.time()
        _, jogada = self.minimax(jogo, profundidade=3, alfa=float('-inf'), beta=float('inf'), maximizando=True)

        if jogada is None:
            # Fallback heurístico se o tempo for insuficiente
            jogadas = jogo.jogadas_legais()
            melhor_valor = float('-inf')
            for j in jogadas:
                i, k = j
                valor = HEURISTICA_POSICIONAL[i][k]
                ganho = jogo.joga(j).placar(self.jogador) - jogo.placar(self.jogador)
                score = valor + ganho * 10
                if score > melhor_valor:
                    melhor_valor = score
                    jogada = j
        return jogada

    def informa_propria_jogada(self, tabuleiro_antes, jogada, tabuleiro_depois):
        """
        Notifica a IA sobre sua própria jogada.

        Parâmetros:
        - tabuleiro_antes: estado do jogo antes da jogada
        - jogada: tupla (linha, coluna) da jogada realizada
        - tabuleiro_depois: estado do jogo após a jogada

        Retorno: None
        """
        pass

    def informa_jogada_oponente(self, tabuleiro_antes, jogada, tabuleiro_depois):
        """
        Notifica a IA sobre a jogada do oponente.

        Parâmetros:
        - tabuleiro_antes: estado do jogo antes da jogada
        - jogada: jogada feita pelo oponente
        - tabuleiro_depois: estado após a jogada

        Retorno: None
        """
        pass

    def informa_fim(self, jogo_final):
        """
        Notifica a IA sobre o término da partida.

        Parâmetros:
        - jogo_final: estado final do jogo (objeto Othello)

        Retorno: None
        """
        pass

def cria_jogador():
    """
    Cria instância da IA baseada em Minimax.

    Retorno:
    - instância de JogadorMinimax
    """
    return JogadorMinimax()
