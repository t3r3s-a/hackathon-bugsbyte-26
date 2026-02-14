import pygame
from enum import Enum
import pequeno_almoço          # lista de nomes do pequeno-almoço/lanches
from almoco import almoco_nomes # lista de nomes do almoço/jantar
from alimento import alimentos  # dados nutricionais completos

# ========================================
# CONFIGURAÇÕES DO JOGO
# ========================================

LARGURA_JANELA = 900
ALTURA_JANELA = 800
HUD_ALTURA = 80
VELOCIDADE = 7

CALORIAS_POR_SEGUNDO = 5   # calorias perdidas por segundo
CALORIAS_MIN = 0
CALORIAS_MAX = 2500
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
# DICIONÁRIO PARA ACESSO RÁPIDO AOS ALIMENTOS
# ========================================
ALIMENTOS_DICT = {alimento["nome"]: alimento for alimento in alimentos}

# ========================================
# FUNDOS COM DURAÇÕES, DIMENSÕES E LISTAS DE ALIMENTOS
# ========================================

# PROBLEMA: Quando a cobra é muito grande ao mudar de fase clipa fora da grid e dá game_over

FUNDOS = {
    'fase1': {
        'cor_principal': (70, 130, 180),
        'cor_grade': (60, 110, 160),
        'nome': 'Pequeno-Almoço',
        'duracao': 10,
        'cols': 20,
        'rows': 16,
        'alimentos_nomes': pequeno_almoço.pequeno_almoco_nomes   # lista do pequeno-almoço
    },
    'fase2': {
        'cor_principal': (75, 0, 130),
        'cor_grade': (60, 0, 110),
        'nome': 'Lanche da manhã',
        'duracao': 10,
        'cols': 15,
        'rows': 12,
        'alimentos_nomes': pequeno_almoço.pequeno_almoco_nomes   # também lanche
    },
    'fase3': {
        'cor_principal': (210, 180, 140),
        'cor_grade': (190, 160, 120),
        'nome': 'Almoço',
        'duracao': 20,
        'cols': 25,
        'rows': 20,
        'alimentos_nomes': almoco_nomes                          # almoço
    },
    'fase4': {
        'cor_principal': (34, 139, 34),
        'cor_grade': (28, 120, 28),
        'nome': 'Lanche da tarde',
        'duracao': 10,
        'cols': 30,
        'rows': 24,
        'alimentos_nomes': pequeno_almoço.pequeno_almoco_nomes   # lanche
    },
    'fase5': {
        'cor_principal': (34, 139, 34),
        'cor_grade': (28, 120, 28),
        'nome': 'Jantar',
        'duracao': 20,
        'cols': 30,
        'rows': 24,
        'alimentos_nomes': almoco_nomes                          # jantar
    }
}

# ========================================
# DIREÇÕES
# ========================================
class Direcao(Enum):
    DIREITA = 1
    ESQUERDA = 2
    CIMA = 3
    BAIXO = 4