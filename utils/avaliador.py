"""
Funções auxiliares de avaliação para o agente de Othello.
Equipe: Anderson Alves Schinaid, Jorge Filho e Simone Britto.
"""

def diferenca_mobilidade(jogo, jogador):
    movimentos_jogador = len(jogo.movimentos_validos(jogador))
    movimentos_oponente = len(jogo.movimentos_validos(1 - jogador))
    return movimentos_jogador - movimentos_oponente
