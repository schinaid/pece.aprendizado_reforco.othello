"""
IA Minimax com Poda Alfa-Beta para Othello (Competição 2025)

Autores:
- Anderson Alves Schinaid
- Jorge Filho
- Simone Britto

Descrição:
IA que utiliza o algoritmo Minimax com profundidade 3 e poda alfa-beta
para escolher a melhor jogada no Othello. Em casos em que a busca
excede o tempo limite (segundo as regras da competição), o agente
faz uso de uma heurística posicional + ganho de peças como fallback.
"""

import numpy as np
import time
from .utils.avaliador import diferenca_mobilidade

# Tabela de pesos posicionais (valores estratégicos no tabuleiro)
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
    IA baseada no algoritmo Minimax com poda alfa-beta e fallback heurístico.
    """

    def __init__(self):
        """
        Inicializa o jogador com limite de tempo e contadores auxiliares.
        """
        self.jogador = None
        self.id_oponente = None
        self.limite_tempo = 0.13  # 130ms - seguro dentro dos 150ms da competição
        self.inicio_busca = None
        self.fallback_usado = 0

    def nova_partida(self, jogo, jogador, id_oponente=None):
        """
        Notifica a IA do início de uma nova partida.

        Parâmetros:
        - jogo: estado inicial da partida (objeto Othello)
        - jogador: inteiro representando o lado da IA (1 ou -1)
        - id_oponente: identificador opcional do adversário

        Retorno: None
        """
        self.jogador = jogador
        self.id_oponente = id_oponente

    def avalia(self, jogo):
        """
        Avalia o estado do jogo com base em:
        - Valor posicional das peças
        - Diferença de peças no placar
        - Mobilidade relativa

        Parâmetros:
        - jogo: objeto Othello representando o estado atual

        Retorno:
        - valor (float): escore heurístico da posição
        """
        tab = jogo.tabuleiro()
        valor_pos = np.sum(tab * HEURISTICA_POSICIONAL * self.jogador)
        ganho = jogo.placar(self.jogador) - jogo.placar(-self.jogador)
        mobil = diferenca_mobilidade(jogo, self.jogador)
        return valor_pos + ganho * 15 + mobil * 1

    def minimax(self, jogo, profundidade, alfa, beta, maximizando):
        """
        Algoritmo Minimax com poda alfa-beta.

        Parâmetros:
        - jogo: estado atual do jogo
        - profundidade: limite de profundidade restante
        - alfa: valor alfa para poda
        - beta: valor beta para poda
        - maximizando: True se for turno da IA, False se do oponente

        Retorno:
        - (valor, jogada): tupla com escore e melhor jogada
        """
        if time.time() - self.inicio_busca > self.limite_tempo or profundidade == 0 or jogo.terminou():
            return self.avalia(jogo), None

        jogadas = jogo.jogadas_legais()
        if not jogadas:
            return self.avalia(jogo), None

        melhor_valor = float('-inf') if maximizando else float('inf')
        melhor_jogada = None

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

    def fallback_heuristico(self, jogo):
        """
        Estratégia alternativa usada quando Minimax excede o tempo.

        Parâmetros:
        - jogo: estado atual do jogo

        Retorno:
        - jogada (tupla): coordenadas da melhor jogada disponível
        """
        jogadas = jogo.jogadas_legais()
        if not jogadas:
            return None

        melhor_valor = float('-inf')
        melhores = []

        for j in jogadas:
            i, k = j
            valor = HEURISTICA_POSICIONAL[i][k]
            ganho = jogo.joga(j).placar(self.jogador) - jogo.placar(self.jogador)
            score = valor + ganho * 10
            if score > melhor_valor:
                melhor_valor = score
                melhores = [j]
            elif score == melhor_valor:
                melhores.append(j)

        return np.random.choice(melhores)

    def escolhe_jogada(self, jogo):
        """
        Escolhe a melhor jogada no turno atual.

        Retorno:
        - jogada (tupla): coordenada da jogada escolhida
        """
        try:
            self.inicio_busca = time.time()
            _, jogada = self.minimax(jogo, profundidade=3, alfa=float('-inf'), beta=float('inf'), maximizando=True)

            if jogada is None:
                self.fallback_usado += 1
                return self.fallback_heuristico(jogo)

            return jogada
        except Exception as e:
            print(f"[ERRO EM escolhe_jogada] {e}")
            self.fallback_usado += 1
            return self.fallback_heuristico(jogo)

    def informa_propria_jogada(self, tabuleiro_antes, jogada, tabuleiro_depois):
        """
        Notifica a IA sobre a jogada realizada por ela mesma.
        """
        pass

    def informa_jogada_oponente(self, tabuleiro_antes, jogada, tabuleiro_depois):
        """
        Notifica a IA sobre a jogada do adversário.
        """
        pass

    def informa_fim(self, jogo_final):
        """
        Notifica o fim da partida.

        Parâmetros:
        - jogo_final: objeto Othello representando o estado final

        Retorno: None
        """
        print(f"Fallbacks usados nesta partida: {self.fallback_usado}")
        self.fallback_usado = 0

def cria_jogador():
    """
    Cria instância da IA baseada em Minimax.

    Retorno:
    - instância de JogadorMinimax
    """
    return JogadorMinimax()
