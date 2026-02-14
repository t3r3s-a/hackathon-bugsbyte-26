import pygame
import os
from constantes import *

# --- PALETA DE CORES: DARK ORANGE ---
C_BG_DARK    = (24, 24, 27)       
C_CARD       = (39, 39, 42)       
C_GRID       = (45, 45, 48)       
C_TEXT       = (250, 250, 249)    
C_SNAKE_BODY = (160, 60, 0)       # Laranja Escuro
C_SNAKE_HEAD = (190, 75, 0)       
C_SNAKE_GLOW = (249, 115, 22)     

def desenhar_fundo(self):
    """Desenha o fundo escuro e a grelha de jogo."""
    self.display.fill(C_BG_DARK)
    for col in range(self.grid_cols):
        for row in range(self.grid_rows):
            x = self.grid_offset_x + col * self.tamanho_celula
            y = self.grid_offset_y + row * self.tamanho_celula
            pygame.draw.rect(self.display, C_GRID, (x, y, self.tamanho_celula, self.tamanho_celula), 1)
    pygame.draw.line(self.display, C_SNAKE_BODY, (0, HUD_ALTURA), (self.largura, HUD_ALTURA), 2)

def desenhar_cobra(self):
    """Desenha a cobra com cabeça rodada 90 graus para a direita."""
    for i, seg in enumerate(self.cobra):
        if i == 0:
            try:
                caminho = os.path.join(self.caminho_base, "assets", "cabeca_snake.png")
                img = pygame.image.load(caminho).convert_alpha()
                img = pygame.transform.scale(img, (self.tamanho_celula, self.tamanho_celula))
                
                # Roda 90 graus para a direita
                img = pygame.transform.rotate(img, -90)
                
                self.display.blit(img, (seg[0], seg[1]))
            except:
                pygame.draw.rect(self.display, C_SNAKE_HEAD, (seg[0], seg[1], self.tamanho_celula, self.tamanho_celula), border_radius=6)
        else:
            pygame.draw.rect(self.display, C_SNAKE_BODY, (seg[0]+1, seg[1]+1, self.tamanho_celula-2, self.tamanho_celula-2), border_radius=4)

def desenhar_alimento(self):
    """Desenha o quadrado de fundo com a cor traduzida do alimento."""
    
    # 1. Dicionário de tradução (Português -> RGB)
    tradutor_cores = {
        "laranja": (255, 140, 0),
        "verde":   (34, 197, 94),
        "vermelho": (220, 38, 38),
        "amarelo": (253, 224, 71),
        "roxo":    (168, 85, 247),
        "castanho": (120, 53, 15),
        "branco":  (255, 255, 255)
    }

    # 2. Busca o nome da cor que está no teu alimento.py (ex: "laranja")
    nome_cor = self.alimento_atual.get('cor', 'laranja').lower()
    
    # 3. Converte o nome para o tuplo RGB (usa Laranja se não encontrar no dicionário)
    cor_rgb = tradutor_cores.get(nome_cor, (255, 140, 0))
    
    # 4. Desenha o QUADRADO DE FUNDO SÓLIDO
    rect_fundo = (self.alimento_pos[0], self.alimento_pos[1], self.tamanho_celula, self.tamanho_celula)
    pygame.draw.rect(self.display, cor_rgb, rect_fundo, border_radius=4)

    # 5. Desenha a IMAGEM do alimento por cima
    try:
        img_orig = pygame.image.load(self.caminho_imagem_alimento).convert_alpha()
        img = pygame.transform.smoothscale(img_orig, (self.tamanho_celula, self.tamanho_celula))
        self.display.blit(img, (self.alimento_pos[0], self.alimento_pos[1]))
    except:
        # Se não houver imagem, faz um contorno para não ficar vazio
        pygame.draw.rect(self.display, (255, 255, 255), rect_fundo, 1, border_radius=4)

def desenhar_hud(self):
    """Desenha o HUD superior."""
    pygame.draw.rect(self.display, C_CARD, (0, 0, self.largura, HUD_ALTURA))
    
    # Texto Energia
    texto_energia = self.font_score.render(f'Energia: {self.pontuacao} kcal', True, C_TEXT)
    self.display.blit(texto_energia, (15, 10))
    
    # Barra de Calorias
    largura_barra, altura_barra = 300, 14
    x_barra, y_barra = self.largura // 2 - largura_barra // 2, 15
    pygame.draw.rect(self.display, C_GRID, (x_barra, y_barra, largura_barra, altura_barra), border_radius=7)
    
    proporcao = max(0, min(1, self.calorias / CALORIAS_MAX))
    if proporcao > 0:
        pygame.draw.rect(self.display, C_SNAKE_GLOW, (x_barra, y_barra, int(largura_barra * proporcao), altura_barra), border_radius=7)
    
    txt_cal = self.font_calorias.render(f'{int(self.calorias)}/{CALORIAS_MAX} kcal', True, C_TEXT)
    self.display.blit(txt_cal, (self.largura // 2 - txt_cal.get_width() // 2, y_barra + 18))

def desenhar_transicao(self):
    """Menu de transição/fases."""
    overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
    overlay.fill((24, 24, 27, 220)) 
    self.display.blit(overlay, (0, 0))
    
    card = pygame.Rect(self.largura//2 - 250, self.altura//2 - 200, 500, 380)
    pygame.draw.rect(self.display, C_CARD, card, border_radius=15)
    pygame.draw.rect(self.display, C_SNAKE_BODY, card, 2, border_radius=15)
    
    titulo = self.font_transicao.render("MENU DE FASES", True, C_SNAKE_GLOW)
    self.display.blit(titulo, (self.largura//2 - titulo.get_width()//2, self.altura//2 - 160))
    
    fases = list(FUNDOS.keys())
    y = self.altura // 2 - 60
    for i, fase_key in enumerate(fases):
        sel = i == self.fase_selecionada
        cor = C_SNAKE_GLOW if sel else C_TEXT
        txt = self.font_fase.render(f"{' > ' if sel else '   '}{i+1}. {FUNDOS[fase_key]['nome']}", True, cor)
        self.display.blit(txt, (self.largura//2 - 120, y))
        y += 45
    
    sel_mini = self.fase_selecionada == len(fases)
    txt_mini = self.font_fase.render(f"{' > ' if sel_mini else '   '}{len(fases)+1}. 🎲 Minijogo Aleatório", True, C_SNAKE_GLOW if sel_mini else C_TEXT)
    self.display.blit(txt_mini, (self.largura//2 - 120, y))