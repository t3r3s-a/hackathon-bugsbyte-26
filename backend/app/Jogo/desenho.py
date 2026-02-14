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
    self.display.fill(C_BG_DARK)
    for col in range(self.grid_cols):
        for row in range(self.grid_rows):
            x = self.grid_offset_x + col * self.tamanho_celula
            y = self.grid_offset_y + row * self.tamanho_celula
            pygame.draw.rect(self.display, C_GRID, (x, y, self.tamanho_celula, self.tamanho_celula), 1)
    pygame.draw.line(self.display, C_SNAKE_BODY, (0, HUD_ALTURA), (self.largura, HUD_ALTURA), 2)

def desenhar_cobra(self):
    for i, seg in enumerate(self.cobra):
        if i == 0:
            if self.img_cabeca_original:
                # Redimensiona e roda apenas se o tamanho da célula mudou
                if not hasattr(self, 'cabeca_cache') or self.cabeca_cache_tamanho != self.tamanho_celula:
                    img = pygame.transform.scale(self.img_cabeca_original, (self.tamanho_celula, self.tamanho_celula))
                    self.cabeca_cache = pygame.transform.rotate(img, -90)
                    self.cabeca_cache_tamanho = self.tamanho_celula
                self.display.blit(self.cabeca_cache, (seg[0], seg[1]))
            else:
                pygame.draw.rect(self.display, C_SNAKE_HEAD, (seg[0], seg[1], self.tamanho_celula, self.tamanho_celula), border_radius=6)
        else:
            pygame.draw.rect(self.display, C_SNAKE_BODY, (seg[0]+1, seg[1]+1, self.tamanho_celula-2, self.tamanho_celula-2), border_radius=4)

def desenhar_alimento(self):
    tradutor_cores = {
        "laranja": (255, 140, 0),
        "verde":   (34, 197, 94),
        "vermelho": (220, 38, 38),
        "amarelo": (253, 224, 71),
        "roxo":    (168, 85, 247),
        "castanho": (120, 53, 15),
        "branco":  (255, 255, 255)
    }
    nome_cor = self.alimento_atual.get('cor', 'laranja').lower()
    cor_rgb = tradutor_cores.get(nome_cor, (255, 140, 0))
    rect_fundo = (self.alimento_pos[0], self.alimento_pos[1], self.tamanho_celula, self.tamanho_celula)
    pygame.draw.rect(self.display, cor_rgb, rect_fundo, border_radius=4)
    
    if self.imagem_alimento_cache:
        self.display.blit(self.imagem_alimento_cache, (self.alimento_pos[0], self.alimento_pos[1]))
    else:
        pygame.draw.rect(self.display, (255, 255, 255), rect_fundo, 1, border_radius=4)

def desenhar_hud(self):
    pygame.draw.rect(self.display, C_CARD, (0, 0, self.largura, HUD_ALTURA))
    texto_energia = self.font_score.render(f'Energia: {self.pontuacao} kcal', True, C_TEXT)
    self.display.blit(texto_energia, (15, 10))
    largura_barra, altura_barra = 300, 14
    x_barra, y_barra = self.largura // 2 - largura_barra // 2, 15
    pygame.draw.rect(self.display, C_GRID, (x_barra, y_barra, largura_barra, altura_barra), border_radius=7)
    proporcao = max(0, min(1, self.calorias / CALORIAS_MAX))
    if proporcao > 0:
        pygame.draw.rect(self.display, C_SNAKE_GLOW, (x_barra, y_barra, int(largura_barra * proporcao), altura_barra), border_radius=7)
    txt_cal = self.font_calorias.render(f'{int(self.calorias)}/{CALORIAS_MAX} kcal', True, C_TEXT)
    self.display.blit(txt_cal, (self.largura // 2 - txt_cal.get_width() // 2, y_barra + 18))

def desenhar_menu(self):
    overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
    overlay.fill((24, 24, 27, 220))
    self.display.blit(overlay, (0, 0))
    
    card = pygame.Rect(self.largura//2 - 250, self.altura//2 - 200, 500, 350)
    pygame.draw.rect(self.display, C_CARD, card, border_radius=15)
    pygame.draw.rect(self.display, C_SNAKE_BODY, card, 2, border_radius=15)
    
    titulo = self.font_transicao.render("ESCOLHA SUA AÇÃO", True, C_SNAKE_GLOW)
    self.display.blit(titulo, (self.largura//2 - titulo.get_width()//2, self.altura//2 - 160))
    
    y = self.altura // 2 - 80
    for i, (texto, tipo, destino) in enumerate(self.opcoes_menu):
        cor = C_SNAKE_GLOW if i == self.opcao_selecionada else C_TEXT
        texto_render = self.font_fase.render(texto, True, cor)
        self.display.blit(texto_render, (self.largura//2 - texto_render.get_width()//2, y))
        y += 40
    
    instrucoes = self.font_fase.render("Setinhas para navegar, Enter para confirmar", True, C_TEXT)
    self.display.blit(instrucoes, (self.largura//2 - instrucoes.get_width()//2, self.altura//2 + 100))

def desenhar_dormir(self):
    overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
    overlay.fill((24, 24, 27, 220))
    self.display.blit(overlay, (0, 0))
    
    card = pygame.Rect(self.largura//2 - 250, self.altura//2 - 200, 500, 300)
    pygame.draw.rect(self.display, C_CARD, card, border_radius=15)
    pygame.draw.rect(self.display, C_SNAKE_BODY, card, 2, border_radius=15)
    
    titulo = self.font_transicao.render("FIM DO DIA", True, C_SNAKE_GLOW)
    self.display.blit(titulo, (self.largura//2 - titulo.get_width()//2, self.altura//2 - 160))
    
    y = self.altura // 2 - 80
    for i, (texto, tipo, destino) in enumerate(self.opcoes_menu):
        cor = C_SNAKE_GLOW if i == self.opcao_selecionada else C_TEXT
        texto_render = self.font_fase.render(texto, True, cor)
        self.display.blit(texto_render, (self.largura//2 - texto_render.get_width()//2, y))
        y += 60
    
    instrucoes = self.font_fase.render("Setinhas para navegar, Enter para confirmar", True, C_TEXT)
    self.display.blit(instrucoes, (self.largura//2 - instrucoes.get_width()//2, self.altura//2 + 200))
   

def desenhar_feedback(self):
    overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
    overlay.fill((24, 24, 27, 200))
    self.display.blit(overlay, (0, 0))
    
    card = pygame.Rect(self.largura//2 - 300, self.altura//2 - 80, 600, 160)
    pygame.draw.rect(self.display, C_CARD, card, border_radius=15)
    pygame.draw.rect(self.display, C_SNAKE_BODY, card, 2, border_radius=15)
    
    texto = self.font_transicao.render(self.mensagem_feedback, True, C_SNAKE_GLOW)
    self.display.blit(texto, (self.largura//2 - texto.get_width()//2, self.altura//2 - 20))