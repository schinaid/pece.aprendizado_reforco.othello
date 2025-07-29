
"""
IA Heurística para Othello (Competição 2025)

Autores:
- Anderson Alves Schinaid
- Jorge Filho
- Simone Britto

Descrição:
IA baseada em uma heurística posicional + ganho de peças + mobilidade.
Estrutura em pacote, pronta para expansão com minimax ou aprendizado por reforço.
"""

import numpy as np
from utils.avaliador import diferenca_mobilidade

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

class JogadorHeuristico:
    """
    IA que escolhe a jogada baseada em:
    - Valor posicional da casa
    - Ganho imediato de peças
    - Mobilidade relativa
    """

    def __init__(self):
        self.jogador = None
        self.id_oponente = None

    def nova_partida(self, jogo, jogador, id_oponente=None):
        """
        Notifica início de nova partida.
        """
        self.jogador = jogador
        self.id_oponente = id_oponente

    def escolhe_jogada(self, jogo):
        """
        Escolhe a jogada baseada em heurística.

        Retorna:
        - jogada (linha, coluna)
        """
        jogadas = jogo.jogadas_legais()
        if not jogadas:
            return None

        melhor_valor = float('-inf')
        melhor_jogada = None

        for jogada in jogadas:
            i, j = jogada
            valor_posicional = HEURISTICA_POSICIONAL[i][j]
            novo_jogo = jogo.joga(jogada)
            ganho = novo_jogo.placar(self.jogador) - jogo.placar(self.jogador)
            mobil = diferenca_mobilidade(novo_jogo, self.jogador)
            score = valor_posicional + ganho * 10 + mobil * 2
            if score > melhor_valor:
                melhor_valor = score
                melhor_jogada = jogada

        return melhor_jogada

    def informa_propria_jogada(self, tabuleiro_antes, jogada, tabuleiro_depois):
        pass

    def informa_jogada_oponente(self, tabuleiro_antes, jogada, tabuleiro_depois):
        pass

    def informa_fim(self, jogo_final):
        pass

def cria_jogador():
    """
    Função obrigatória de criação de jogador.

    Retorno:
    - instância de JogadorHeuristico
    """
    return JogadorHeuristico()
