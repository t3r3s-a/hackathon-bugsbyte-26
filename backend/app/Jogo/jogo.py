import pygame
import random
import os
import sys
import importlib

from constantes import *
from alimento import alimentos
import desenho

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.largura = LARGURA_JANELA
        self.altura = ALTURA_JANELA
        self.display = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Snake Game - Calorias')
        self.clock = pygame.time.Clock()
        
        self.font_score = pygame.font.Font(None, 30)
        self.font_alimento = pygame.font.Font(None, 50)
        self.font_fase = pygame.font.Font(None, 25)
        self.font_calorias = pygame.font.Font(None, 25)
        self.font_transicao = pygame.font.Font(None, 48)

        self.caminho_base = os.path.dirname(__file__)
        
        self.fase_selecionada = 0
        self.minijogos = ['corrida', 'equilibrio', 'dinossauro']
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
        self.colocar_alimento()
        
    def colocar_alimento(self):
        tentativas = 0
        max_tentativas = 1000
        while tentativas < max_tentativas:
            col = random.randint(0, self.grid_cols - 1)
            row = random.randint(0, self.grid_rows - 1)
            x = self.grid_offset_x + col * self.tamanho_celula
            y = self.grid_offset_y + row * self.tamanho_celula
            if [x, y] not in self.cobra:
                self.alimento_pos = [x, y]
                self.alimento_atual = random.choice(alimentos)

                nome_img = self.alimento_atual["nome"] + ".png"
                self.caminho_imagem_alimento = os.path.join(
                    self.caminho_base, "assets", nome_img
                )

                return
            tentativas += 1
        self.game_over()
        
    def mudar_para_fase(self, indice):
        fases = list(FUNDOS.keys())
        self.fase_atual = fases[indice]
        self.calcular_offset_grid()
        self.contador_frames_fase = 0
        
        col_centro = self.grid_cols // 2
        row_centro = self.grid_rows // 2
        x = self.grid_offset_x + col_centro * self.tamanho_celula
        y = self.grid_offset_y + row_centro * self.tamanho_celula
        tamanho_desejado = max(1, int(self.calorias // 100))
        self.cobra = []
        for i in range(tamanho_desejado):
            self.cobra.append([x - i * self.tamanho_celula, y])
        self.direcao = Direcao.DIREITA
        
        self.colocar_alimento()
        self.em_transicao = False

    def executar_minijogo_aleatorio(self):
        minijogo = random.choice(self.minijogos)
        nome_funcao = f"minigame_{minijogo}"
        try:
            modulo = importlib.import_module(f"MiniJogos.{minijogo}")
            funcao = getattr(modulo, nome_funcao)
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Erro ao carregar minijogo {minijogo}: {e}")
            return True

        resultado = funcao(self.calorias)

        if resultado == -1:  # usuário fechou a janela
            pygame.quit()
            sys.exit()

        if resultado == 0:
            # Perdeu no minijogo: aplica penalidade
            self.calorias -= 50
            if self.calorias < CALORIAS_MIN:
                self.calorias = CALORIAS_MIN
        else:
            # Ganhou: subtrai as calorias queimadas
            self.calorias -= resultado
            if self.calorias < CALORIAS_MIN:
                self.calorias = CALORIAS_MIN

        self.ajustar_tamanho()

        if self.calorias <= CALORIAS_MIN:
            if self.game_over():
                self.reset_jogo()
            else:
                pygame.quit()
                sys.exit()
            return False

        return True

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
    
    def verificar_alimento(self):
        return self.cobra[0] == self.alimento_pos
    
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
                        num_opcoes = len(FUNDOS) + 1
                        if event.key == pygame.K_UP:
                            self.fase_selecionada = (self.fase_selecionada - 1) % num_opcoes
                        elif event.key == pygame.K_DOWN:
                            self.fase_selecionada = (self.fase_selecionada + 1) % num_opcoes
                        elif event.key == pygame.K_RETURN:
                            if self.fase_selecionada < len(FUNDOS):
                                self.mudar_para_fase(self.fase_selecionada)
                            else:
                                self.executar_minijogo_aleatorio()
                    else:
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
                
                comeu = self.verificar_alimento()
                if comeu:
                    self.calorias += self.alimento_atual['energia_kcal']
                    self.pontuacao += self.alimento_atual['energia_kcal']
                    desejado_antes = max(1, int((self.calorias - self.alimento_atual['energia_kcal']) // 100))
                    desejado_depois = max(1, int(self.calorias // 100))
                    for _ in range(desejado_depois - desejado_antes):
                        self.cobra.append(self.cobra[-1])
                    self.colocar_alimento()
                
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
                    self.fase_selecionada = list(FUNDOS.keys()).index(self.fase_atual)
            
            desenho.desenhar_fundo(self)
            desenho.desenhar_cobra(self)
            desenho.desenhar_alimento(self)
            desenho.desenhar_hud(self)
            
            if self.em_transicao:
                desenho.desenhar_transicao(self)
            
            pygame.display.flip()
            self.clock.tick(VELOCIDADE)
