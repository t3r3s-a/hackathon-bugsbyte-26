import pygame
from constantes import *    

def desenhar_fundo(self):
    fundo = FUNDOS[self.fase_atual]
    pygame.draw.rect(self.display, PRETO, (0, 0, self.largura, HUD_ALTURA))
    rect_jogo = pygame.Rect(0, HUD_ALTURA, self.largura, self.altura - HUD_ALTURA)
    pygame.draw.rect(self.display, fundo['cor_principal'], rect_jogo)
    
    for col in range(self.grid_cols):
        for row in range(self.grid_rows):
            x = self.grid_offset_x + col * self.tamanho_celula
            y = self.grid_offset_y + row * self.tamanho_celula
            pygame.draw.rect(self.display, fundo['cor_grade'],
                             (x, y, self.tamanho_celula, self.tamanho_celula), 1)
    
    pygame.draw.line(self.display, BRANCO, (0, HUD_ALTURA), (self.largura, HUD_ALTURA), 2)

def desenhar_cobra(self):
    for i, seg in enumerate(self.cobra):
        cor = VERDE_ESCURO if i == 0 else VERDE
        pygame.draw.rect(self.display, cor,
                         (seg[0], seg[1], self.tamanho_celula, self.tamanho_celula))
        if i != 0:
            pygame.draw.rect(self.display, cor,
                             (seg[0], seg[1], self.tamanho_celula, self.tamanho_celula), 2)

def desenhar_alimento(self):
    imagem_original = pygame.image.load(self.caminho_imagem_alimento).convert_alpha()
    imagem = pygame.transform.scale(
        imagem_original,
        (self.tamanho_celula, self.tamanho_celula)
    )
    self.display.blit(imagem, (self.alimento_pos[0], self.alimento_pos[1]))

def desenhar_hud(self):
    self.display.blit(self.font_score.render(f'energia_kcal: {self.pontuacao}', True, BRANCO), (10, 5))
    fase_info = FUNDOS[self.fase_atual]
    self.display.blit(self.font_fase.render(f'Fase: {fase_info["nome"]}', True, BRANCO), (10, 30))
    self.display.blit(self.font_fase.render(
        f'{self.alimento_atual["nome"]} (+{self.alimento_atual["energia_kcal"]})',
        True, BRANCO), (self.largura - 250, 5))
    
    frames_restantes = int(fase_info['duracao'] * VELOCIDADE) - self.contador_frames_fase
    segundos_restantes = max(0, frames_restantes // VELOCIDADE)
    texto_tempo = self.font_fase.render(f'Tempo: {segundos_restantes}s', True, BRANCO)
    self.display.blit(texto_tempo, (self.largura - 180, 30))
    
    texto_grid = self.font_fase.render(f'Grade: {self.grid_cols}x{self.grid_rows}', True, BRANCO)
    self.display.blit(texto_grid, (self.largura - 180, 55))
    
    texto_celula = self.font_fase.render(f'Célula: {self.tamanho_celula}px', True, BRANCO)
    self.display.blit(texto_celula, (self.largura - 180, 80))
    
    largura_barra = 300
    altura_barra = 20
    x_barra = self.largura // 2 - largura_barra // 2
    y_barra = 5
    pygame.draw.rect(self.display, CINZA, (x_barra, y_barra, largura_barra, altura_barra))
    proporcao = max(0, min(1, self.calorias / CALORIAS_MAX))
    largura_preenchida = int(largura_barra * proporcao)
    if largura_preenchida > 0:
        cor_barra = VERDE if self.calorias < CALORIAS_MAX * 0.8 else LARANJA
        pygame.draw.rect(self.display, cor_barra, (x_barra, y_barra, largura_preenchida, altura_barra))
    pygame.draw.rect(self.display, BRANCO, (x_barra, y_barra, largura_barra, altura_barra), 2)
    self.display.blit(self.font_calorias.render(f'{int(self.calorias)}/{CALORIAS_MAX}', True, BRANCO),
                     (x_barra + largura_barra + 10, y_barra))

def desenhar_menu(self):
    overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    self.display.blit(overlay, (0, 0))
    
    titulo = self.font_transicao.render("Escolha sua próxima ação:", True, BRANCO)
    self.display.blit(titulo, (self.largura//2 - titulo.get_width()//2, self.altura//2 - 150))
    
    y = self.altura // 2 - 50
    for i, (texto, tipo, destino) in enumerate(self.opcoes_menu):
        cor = VERDE if i == self.opcao_selecionada else BRANCO
        texto_render = self.font_fase.render(texto, True, cor)
        self.display.blit(texto_render, (self.largura//2 - texto_render.get_width()//2, y))
        y += 40
    
    instrucoes = self.font_fase.render("Use as setas ↑ ↓ para navegar, Enter para confirmar", True, BRANCO)
    self.display.blit(instrucoes, (self.largura//2 - instrucoes.get_width()//2, self.altura//2 + 100))

def desenhar_dormir(self):
    overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    self.display.blit(overlay, (0, 0))
    
    titulo = self.font_transicao.render("Você foi dormir. O que deseja?", True, BRANCO)
    self.display.blit(titulo, (self.largura//2 - titulo.get_width()//2, self.altura//2 - 150))
    
    y = self.altura // 2 - 50
    for i, (texto, tipo, destino) in enumerate(self.opcoes_menu):
        cor = VERDE if i == self.opcao_selecionada else BRANCO
        texto_render = self.font_fase.render(texto, True, cor)
        self.display.blit(texto_render, (self.largura//2 - texto_render.get_width()//2, y))
        y += 40
    
    instrucoes = self.font_fase.render("Use as setas ↑ ↓ para navegar, Enter para confirmar", True, BRANCO)
    self.display.blit(instrucoes, (self.largura//2 - instrucoes.get_width()//2, self.altura//2 + 100))