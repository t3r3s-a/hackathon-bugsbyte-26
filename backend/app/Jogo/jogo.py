import pygame
import random
from constantes import *

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.largura = LARGURA_JANELA
        self.altura = ALTURA_JANELA
        self.display = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Snake Game - Calorias')
        self.clock = pygame.time.Clock()
        
        self.font_score = pygame.font.Font(None, 30)
        self.font_fruta = pygame.font.Font(None, 50)
        self.font_fase = pygame.font.Font(None, 25)
        self.font_calorias = pygame.font.Font(None, 25)
        self.font_transicao = pygame.font.Font(None, 48)
        
        self.fase_selecionada = 0  # Índice da fase escolhida no menu de transição
        self.reset_jogo()
        
    def calcular_offset_grid(self):
        fase_info = FUNDOS[self.fase_atual]
        self.grid_cols = fase_info['cols']
        self.grid_rows = fase_info['rows']
        
        largura_disponivel = self.largura
        altura_disponivel = self.altura - HUD_ALTURA
        
        tamanho_por_col = largura_disponivel // self.grid_cols
        tamanho_por_row = altura_disponivel // self.grid_rows
        self.tamanho_celula = min(tamanho_por_col, tamanho_por_row)
        
        self.grid_largura = self.grid_cols * self.tamanho_celula
        self.grid_altura = self.grid_rows * self.tamanho_celula
        
        self.grid_offset_x = (largura_disponivel - self.grid_largura) // 2
        self.grid_offset_y = HUD_ALTURA + (altura_disponivel - self.grid_altura) // 2
        
    def reset_jogo(self):
        self.direcao = Direcao.DIREITA
        self.fase_atual = 'fase1'
        self.fase_selecionada = 0
        self.calcular_offset_grid()
        
        col_centro = self.grid_cols // 2
        row_centro = self.grid_rows // 2
        x = self.grid_offset_x + col_centro * self.tamanho_celula
        y = self.grid_offset_y + row_centro * self.tamanho_celula
        self.cobra = [
            [x, y],
            [x - self.tamanho_celula, y],
            [x - 2 * self.tamanho_celula, y]
        ]
        
        self.pontuacao = 0
        self.calorias = CALORIAS_INICIAL
        self.contador_frames_fase = 0
        self.em_transicao = False
        self.colocar_fruta()
        
    def colocar_fruta(self):
        """Posiciona a fruta em uma célula aleatória não ocupada pela cobra."""
        tentativas = 0
        max_tentativas = 1000
        while tentativas < max_tentativas:
            col = random.randint(0, self.grid_cols - 1)
            row = random.randint(0, self.grid_rows - 1)
            x = self.grid_offset_x + col * self.tamanho_celula
            y = self.grid_offset_y + row * self.tamanho_celula
            if [x, y] not in self.cobra:
                self.fruta_pos = [x, y]
                self.fruta_atual = random.choice(FRUTAS)
                return
            tentativas += 1
        # Se não encontrar posição livre, game over (improvável)
        self.game_over()
        
    def mudar_para_fase(self, indice):
        """Muda para a fase correspondente ao índice fornecido."""
        fases = list(FUNDOS.keys())
        self.fase_atual = fases[indice]
        self.calcular_offset_grid()
        self.contador_frames_fase = 0
        
        # Posiciona a cobra no centro com base nas calorias atuais
        col_centro = self.grid_cols // 2
        row_centro = self.grid_rows // 2
        x = self.grid_offset_x + col_centro * self.tamanho_celula
        y = self.grid_offset_y + row_centro * self.tamanho_celula
        tamanho_desejado = max(1, int(self.calorias // 100))
        self.cobra = []
        for i in range(tamanho_desejado):
            self.cobra.append([x - i * self.tamanho_celula, y])
        self.direcao = Direcao.DIREITA
        
        self.colocar_fruta()
        self.em_transicao = False
    
    # (Opcional) Manter o método antigo por compatibilidade, mas não será usado
    def mudar_fase(self):
        fases = list(FUNDOS.keys())
        indice_atual = fases.index(self.fase_atual)
        proximo_indice = (indice_atual + 1) % len(fases)
        self.mudar_para_fase(proximo_indice)
            
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
    
    def desenhar_fruta(self):
        tamanho_fonte = int(self.tamanho_celula * 1.5)
        fonte = pygame.font.Font(None, tamanho_fonte)
        texto = fonte.render(self.fruta_atual['emoji'], True, BRANCO)
        rect = texto.get_rect(center=(self.fruta_pos[0] + self.tamanho_celula//2,
                                       self.fruta_pos[1] + self.tamanho_celula//2))
        self.display.blit(texto, rect)
    
    def desenhar_hud(self):
        self.display.blit(self.font_score.render(f'Pontos: {self.pontuacao}', True, BRANCO), (10, 5))
        fase_info = FUNDOS[self.fase_atual]
        self.display.blit(self.font_fase.render(f'Fase: {fase_info["nome"]}', True, BRANCO), (10, 30))
        self.display.blit(self.font_fase.render(
            f'{self.fruta_atual["emoji"]} {self.fruta_atual["nome"]} (+{self.fruta_atual["pontos"]})',
            True, BRANCO), (self.largura - 180, 5))
        
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
    
    def desenhar_transicao(self):
        """Desenha o menu de escolha de fase."""
        overlay = pygame.Surface((self.largura, self.altura), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.display.blit(overlay, (0, 0))
        
        fases = list(FUNDOS.keys())
        titulo = self.font_transicao.render("Escolha a próxima fase:", True, BRANCO)
        self.display.blit(titulo, (self.largura//2 - titulo.get_width()//2, self.altura//2 - 150))
        
        # Desenha as opções
        y = self.altura // 2 - 50
        for i, fase_key in enumerate(fases):
            cor = VERDE if i == self.fase_selecionada else BRANCO
            texto = self.font_fase.render(f"{i+1}. {FUNDOS[fase_key]['nome']}", True, cor)
            self.display.blit(texto, (self.largura//2 - texto.get_width()//2, y))
            y += 40
        
        instrucoes = self.font_fase.render("Use as setas ↑ ↓ para navegar, Enter para confirmar", True, BRANCO)
        self.display.blit(instrucoes, (self.largura//2 - instrucoes.get_width()//2, self.altura//2 + 100))
    
    def mover_cobra(self):
        cabeca = self.cobra[0].copy()
        if self.direcao == Direcao.DIREITA:
            cabeca[0] += self.tamanho_celula
        elif self.direcao == Direcao.ESQUERDA:
            cabeca[0] -= self.tamanho_celula
        elif self.direcao == Direcao.CIMA:
            cabeca[1] -= self.tamanho_celula
        elif self.direcao == Direcao.BAIXO:
            cabeca[1] += self.tamanho_celula
        self.cobra.insert(0, cabeca)
    
    def verificar_colisao(self):
        cabeca = self.cobra[0]
        if (cabeca[0] < self.grid_offset_x or
            cabeca[0] >= self.grid_offset_x + self.grid_largura or
            cabeca[1] < self.grid_offset_y or
            cabeca[1] >= self.grid_offset_y + self.grid_altura):
            return True
        if cabeca in self.cobra[1:]:
            return True
        return False
    
    def verificar_fruta(self):
        return self.cobra[0] == self.fruta_pos
    
    def ajustar_tamanho(self):
        desejado = max(1, int(self.calorias // 100))
        while len(self.cobra) > desejado:
            self.cobra.pop()
    
    def game_over(self):
        self.display.fill(PRETO)
        textos = [
            self.font_score.render('GAME OVER!', True, VERMELHO),
            self.font_score.render(f'Pontuação Final: {self.pontuacao}', True, BRANCO),
            self.font_score.render(f'Calorias: {int(self.calorias)}', True, BRANCO),
            self.font_fase.render('Pressione ESPAÇO para jogar novamente', True, BRANCO)
        ]
        y = self.altura // 2 - 80
        for texto in textos:
            self.display.blit(texto, (self.largura//2 - texto.get_width()//2, y))
            y += 40
        pygame.display.flip()
        
        esperando = True
        while esperando:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    esperando = False
                    return True
        return True
    
    def jogar(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if self.em_transicao:
                        # Navegação no menu de fases
                        if event.key == pygame.K_UP:
                            self.fase_selecionada = (self.fase_selecionada - 1) % len(FUNDOS)
                        elif event.key == pygame.K_DOWN:
                            self.fase_selecionada = (self.fase_selecionada + 1) % len(FUNDOS)
                        elif event.key == pygame.K_RETURN:
                            self.mudar_para_fase(self.fase_selecionada)
                    else:
                        # Controles normais do jogo
                        if event.key == pygame.K_UP and self.direcao != Direcao.BAIXO:
                            self.direcao = Direcao.CIMA
                        elif event.key == pygame.K_DOWN and self.direcao != Direcao.CIMA:
                            self.direcao = Direcao.BAIXO
                        elif event.key == pygame.K_LEFT and self.direcao != Direcao.DIREITA:
                            self.direcao = Direcao.ESQUERDA
                        elif event.key == pygame.K_RIGHT and self.direcao != Direcao.ESQUERDA:
                            self.direcao = Direcao.DIREITA
            
            if not self.em_transicao:
                self.mover_cobra()
                
                if self.verificar_colisao():
                    if self.game_over():
                        self.reset_jogo()
                    else:
                        pygame.quit()
                        return
                
                comeu = self.verificar_fruta()
                if comeu:
                    self.calorias += self.fruta_atual['pontos']
                    self.pontuacao += self.fruta_atual['pontos']
                    desejado_antes = max(1, int((self.calorias - self.fruta_atual['pontos']) // 100))
                    desejado_depois = max(1, int(self.calorias // 100))
                    for _ in range(desejado_depois - desejado_antes):
                        self.cobra.append(self.cobra[-1])
                    self.colocar_fruta()
                
                self.calorias -= DECAIMENTO_CALORIAS
                
                if self.calorias <= CALORIAS_MIN or self.calorias >= CALORIAS_MAX:
                    if self.game_over():
                        self.reset_jogo()
                    else:
                        pygame.quit()
                        return
                
                self.ajustar_tamanho()
                
                self.contador_frames_fase += 1
                limite_frames = int(FUNDOS[self.fase_atual]['duracao'] * VELOCIDADE)
                if self.contador_frames_fase >= limite_frames:
                    self.em_transicao = True
                    self.fase_selecionada = list(FUNDOS.keys()).index(self.fase_atual)  # Opcional: manter seleção atual
            
            self.desenhar_fundo()
            self.desenhar_cobra()
            self.desenhar_fruta()
            self.desenhar_hud()
            
            if self.em_transicao:
                self.desenhar_transicao()
            
            pygame.display.flip()
            self.clock.tick(VELOCIDADE)