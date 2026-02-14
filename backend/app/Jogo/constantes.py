import pygame
from enum import Enum

# ========================================
# CONFIGURAÇÕES DO JOGO
# ========================================

LARGURA_JANELA = 900
ALTURA_JANELA = 800
HUD_ALTURA = 80
VELOCIDADE = 7

DECAIMENTO_CALORIAS = 1
CALORIAS_MIN = 0
CALORIAS_MAX = 2000
CALORIAS_INICIAL = 300

# ========================================
# CORES
# ========================================
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (213, 50, 80)
VERDE = (0, 255, 0)
VERDE_ESCURO = (0, 155, 0)
CINZA = (128, 128, 128)
LARANJA = (255, 165, 0)

# ========================================
# FUNDOS COM DURAÇÕES E DIMENSÕES DE GRADE
# ========================================

#PROBLEMA: Quando a cobra é muito grande ao mudar de fase clipa fora da grid e dá game_over

FUNDOS = {
    'fase1': {
        'cor_principal': (70, 130, 180),
        'cor_grade': (60, 110, 160),
        'nome': 'Oceano',
        'duracao': 10,
        'cols': 20,
        'rows': 16
    },
    'fase2': {
        'cor_principal': (75, 0, 130),
        'cor_grade': (60, 0, 110),
        'nome': 'Espaço',
        'duracao': 5,
        'cols': 15,
        'rows': 12
    },
    'fase3': {
        'cor_principal': (210, 180, 140),
        'cor_grade': (190, 160, 120),
        'nome': 'Deserto',
        'duracao': 20,
        'cols': 25,
        'rows': 20
    },
    'fase4': {
        'cor_principal': (34, 139, 34),
        'cor_grade': (28, 120, 28),
        'nome': 'Floresta',
        'duracao': 10,
        'cols': 30,
        'rows': 24
    }
}

# ========================================
# FRUTAS
# ========================================
FRUTAS = [
    {'emoji': '🍎', 'nome': 'Maçã', 'pontos': 100},
    {'emoji': '🍊', 'nome': 'Laranja', 'pontos': 100},
    {'emoji': '🍌', 'nome': 'Banana', 'pontos': 50},
    {'emoji': '🍇', 'nome': 'Uvas', 'pontos': 50},
    {'emoji': '🍓', 'nome': 'Morango', 'pontos': 50},
    {'emoji': '🍒', 'nome': 'Cerejas', 'pontos': 150},
    {'emoji': '🍑', 'nome': 'Pêssego', 'pontos': 100},
    {'emoji': '🥝', 'nome': 'Kiwi', 'pontos': 150},
    {'emoji': '🍍', 'nome': 'Ananás', 'pontos': 200},
    {'emoji': '🥭', 'nome': 'Manga', 'pontos': 150},
    {'emoji': '🍉', 'nome': 'Melancia', 'pontos': 250},
    {'emoji': '🍋', 'nome': 'Limão', 'pontos': 120},
    {'emoji': '🥥', 'nome': 'Coco', 'pontos': 300},
    {'emoji': '🍈', 'nome': 'Melão', 'pontos': 200},
    {'emoji': '🥑', 'nome': 'Abacate', 'pontos': 70}
]

# ========================================
# DIREÇÕES
# ========================================
class Direcao(Enum):
    DIREITA = 1
    ESQUERDA = 2
    CIMA = 3
    BAIXO = 4