
"""
IA Heurística para o jogo Othello (Reversi)

Equipe:
- Anderson Alves Schinaid
- Jorge Filho
- Simone Britto

Esta inteligência artificial utiliza uma heurística posicional combinada com contagem de peças capturadas para escolher jogadas.
A estratégia favorece posições vantajosas no tabuleiro (como cantos e bordas) e maximiza o ganho imediato de peças.

Interface compatível com a competição Othello 2025.
"""

import numpy as np

# Mapeamento de prioridade de posições no tabuleiro
# Valores maiores representam posições mais estratégicas
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
    """IA baseada em heurística posicional para o jogo Othello."""

    def __init__(self):
        """Inicializa o jogador e armazena o lado que representará."""
        self.jogador = None
        self.id_oponente = None

    def nova_partida(self, jogo, jogador, id_oponente=None):
        """
        Notifica o jogador do início de uma nova partida.

        Parâmetros:
        - jogo: objeto da classe Othello representando o estado inicial do jogo.
        - jogador: inteiro (1 ou -1) representando a cor da IA.
        - id_oponente: identificador único do oponente (opcional).
        """
        self.jogador = jogador
        self.id_oponente = id_oponente

    def escolhe_jogada(self, jogo):
        """
        Escolhe a próxima jogada a ser feita com base na heurística.

        Parâmetros:
        - jogo: objeto da classe Othello com o estado atual da partida.

        Retorno:
        - jogada (tupla): posição escolhida (linha, coluna) ou None se não houver jogadas legais.
        """
        jogadas = jogo.jogadas_legais()
        if not jogadas:
            return None

        melhor_jogada = None
        melhor_valor = float('-inf')

        for jogada in jogadas:
            i, j = jogada
            valor_posicional = HEURISTICA_POSICIONAL[i][j]
            novo_jogo = jogo.joga(jogada)
            ganho_pecas = novo_jogo.placar(self.jogador) - jogo.placar(self.jogador)
            score = valor_posicional + ganho_pecas * 10  # pondera posição e peças
            if score > melhor_valor:
                melhor_valor = score
                melhor_jogada = jogada

        return melhor_jogada

    def informa_propria_jogada(self, tabuleiro_antes, jogada, tabuleiro_depois):
        """
        Notifica a IA da jogada que ela acabou de fazer.

        Parâmetros:
        - tabuleiro_antes: estado antes da jogada.
        - jogada: tupla da jogada realizada.
        - tabuleiro_depois: estado após a jogada.
        """
        pass

    def informa_jogada_oponente(self, tabuleiro_antes, jogada, tabuleiro_depois):
        """
        Notifica a IA da jogada feita pelo oponente.

        Parâmetros:
        - tabuleiro_antes: estado antes da jogada.
        - jogada: tupla da jogada do oponente.
        - tabuleiro_depois: estado após a jogada.
        """
        pass

    def informa_fim(self, jogo_final):
        """
        Notifica a IA do fim da partida.

        Parâmetros:
        - jogo_final: objeto da classe Othello representando o estado final do jogo.
        """
        pass

def cria_jogador():
    """
    Cria uma instância do JogadorHeuristico.

    Retorno:
    - objeto JogadorHeuristico
    """
    return JogadorHeuristico()
