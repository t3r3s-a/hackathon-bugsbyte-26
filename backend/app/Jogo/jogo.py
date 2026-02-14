import pygame
import random
import os
import sys
import importlib

from constantes import *
import desenho

class SnakeGame:
    def __init__(self):
        pygame.init()
        self.largura = LARGURA_JANELA
        self.altura = ALTURA_JANELA
        self.display = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Nutrium Snack-e')
        self.clock = pygame.time.Clock()
        
        # Fontes corrigidas e alinhadas
        self.font_score = pygame.font.SysFont("Arial", 26, bold=True)
        self.font_alimento = pygame.font.SysFont("Arial", 40)
        self.font_fase = pygame.font.SysFont("Arial", 18)
        self.font_calorias = pygame.font.SysFont("Arial", 18, bold=True)
        self.font_transicao = pygame.font.SysFont("Arial", 30, bold=True)

        self.caminho_base = os.path.dirname(__file__)
        
        # Pré-carrega a imagem da cabeça da cobra (rodada)
        try:
            caminho_cabeca = os.path.join(self.caminho_base, "assets", "cabeca_snake.png")
            img_cabeca = pygame.image.load(caminho_cabeca).convert_alpha()
            self.img_cabeca_original = img_cabeca
        except:
            self.img_cabeca_original = None

        # Para cache do alimento
        self.imagem_alimento_cache = None
        self.nome_alimento_cache = None

        # Lista ordenada das fases (refeições)
        self.ordem_refeicoes = ['fase1', 'fase2', 'fase3', 'fase4', 'fase5']
        self.indice_refeicao_atual = 0
        
        self.minijogos = ['corrida', 'equilibrio', 'dinossauro']
        
        self.tempo_ultima_queima = pygame.time.get_ticks()
        
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
        self.indice_refeicao_atual = 0
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
        self.estado = "jogando"  # "jogando", "menu", "dormir"
        self.opcoes_menu = []
        self.opcao_selecionada = 0
        self.colocar_alimento()
        
    def colocar_alimento(self):
        tentativas = 0
        max_tentativas = 1000
        nomes_fase = FUNDOS[self.fase_atual]['alimentos_nomes']
    
        while tentativas < max_tentativas:
            col = random.randint(0, self.grid_cols - 1)
            row = random.randint(0, self.grid_rows - 1)
            x = self.grid_offset_x + col * self.tamanho_celula
            y = self.grid_offset_y + row * self.tamanho_celula
            if [x, y] not in self.cobra:
                self.alimento_pos = [x, y]
                nome_escolhido = random.choice(nomes_fase)
                self.alimento_atual = ALIMENTOS_DICT[nome_escolhido]
    
                # --- Carregar a imagem ---
                nome_img = self.alimento_atual["nome"] + ".png"
                self.caminho_imagem_alimento = os.path.join(
                    self.caminho_base, "assets", nome_img
                )
                try:
                    img_orig = pygame.image.load(self.caminho_imagem_alimento).convert_alpha()
                    # Redimensiona para o tamanho da célula atual e guarda em cache
                    self.imagem_alimento_cache = pygame.transform.smoothscale(
                        img_orig, (self.tamanho_celula, self.tamanho_celula)
                    )
                    self.nome_alimento_cache = self.alimento_atual["nome"]
                except Exception as e:
                    print(f"Erro ao carregar imagem {self.caminho_imagem_alimento}: {e}")
                    self.imagem_alimento_cache = None
                # ---------------------------------
                return
            tentativas += 1
        self.game_over()
        
    def mudar_para_fase(self, indice):
        """Muda para a fase correspondente ao índice na ordem."""
        self.fase_atual = self.ordem_refeicoes[indice]
        self.indice_refeicao_atual = indice
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
        self.estado = "jogando"

    def preparar_menu_transicao(self):
        """Configura as opções do menu baseado na fase atual."""
        self.opcoes_menu = []
        if self.indice_refeicao_atual < len(self.ordem_refeicoes) - 1:
            proxima_refeicao = self.ordem_refeicoes[self.indice_refeicao_atual + 1]
            nome_proxima = FUNDOS[proxima_refeicao]['nome']
            self.opcoes_menu.append(("Treino", "treino", None))
            self.opcoes_menu.append((nome_proxima, "fase", self.indice_refeicao_atual + 1))
        else:
            self.opcoes_menu.append(("Dormir", "dormir", None))
        self.opcao_selecionada = 0
        self.estado = "menu"

    def executar_treino(self):
        minijogo = random.choice(self.minijogos)
        nome_funcao = f"minigame_{minijogo}"
        try:
            modulo = importlib.import_module(f"MiniJogos.{minijogo}")
            funcao = getattr(modulo, nome_funcao)
        except (ModuleNotFoundError, AttributeError) as e:
            print(f"Erro ao carregar minijogo {minijogo}: {e}")
            return False

        resultado = funcao(self.calorias)

        # Recria a superfície principal com as dimensões originais
        self.display = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Snake Game - Calorias')

        if resultado == -1:
            pygame.quit()
            sys.exit()

        if resultado == 0:
            # Perdeu: aplica penalidade e remove a opção de treino do menu
            self.calorias -= 50
            if self.calorias < CALORIAS_MIN:
                self.calorias = CALORIAS_MIN
            self.ajustar_tamanho()
            if self.calorias <= CALORIAS_MIN:
                if self.game_over():
                    self.reset_jogo()
                else:
                    pygame.quit()
                    sys.exit()

            # Remove a opção "Treino" do menu, deixando apenas a próxima refeição
            if len(self.opcoes_menu) > 1 and self.opcoes_menu[0][1] == "treino":
                self.opcoes_menu.pop(0)  # remove o treino
            return False
        else:
            # Ganhou: queima calorias e avança
            self.calorias -= resultado
            if self.calorias < CALORIAS_MIN:
                self.calorias = CALORIAS_MIN
            self.ajustar_tamanho()
            if self.calorias <= CALORIAS_MIN:
                if self.game_over():
                    self.reset_jogo()
                else:
                    #pygame.quit()
                    sys.exit()
            return True

    def mostrar_tela_dormir(self):
        self.estado = "dormir"
        self.opcoes_menu = [("Acordar", "acordar", None), ("Sair", "sair", None)]
        self.opcao_selecionada = 0

    def mover_cobra(self):
        if hasattr(self, 'proxima_direcao'):
            self.direcao = self.proxima_direcao
            del self.proxima_direcao
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
        # Cores atualizadas para o novo tema
        COR_BG = (24, 24, 27)
        COR_LARANJA = (249, 115, 22)
        COR_BRANCO = (250, 250, 249)

        self.display.fill(COR_BG)
        textos = [
            self.font_transicao.render('GAME OVER!', True, (239, 68, 68)), # Vermelho
            self.font_score.render(f'Pontuação Final: {self.pontuacao}', True, COR_LARANJA),
            self.font_score.render(f'Calorias: {int(self.calorias)}', True, COR_BRANCO),
            self.font_fase.render('Pressione ESPAÇO para jogar novamente', True, (148, 163, 184))
        ]
        y = self.altura // 2 - 80
        for texto in textos:
            self.display.blit(texto, (self.largura//2 - texto.get_width()//2, y))
            y += 50
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    return True
    
    def jogar(self):
        while True:
            agora = pygame.time.get_ticks()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    if self.estado in ("menu", "dormir"):
                        num_opcoes = len(self.opcoes_menu)
                        if event.key == pygame.K_UP:
                            self.opcao_selecionada = (self.opcao_selecionada - 1) % num_opcoes
                        elif event.key == pygame.K_DOWN:
                            self.opcao_selecionada = (self.opcao_selecionada + 1) % num_opcoes
                        elif event.key == pygame.K_RETURN:
                            texto, tipo, destino = self.opcoes_menu[self.opcao_selecionada]
                            if tipo == "fase":
                                self.mudar_para_fase(destino)
                            elif tipo == "treino":
                                venceu = self.executar_treino()
                                if venceu:
                                    if self.indice_refeicao_atual < len(self.ordem_refeicoes) - 1:
                                        self.mudar_para_fase(self.indice_refeicao_atual + 1)
                                    else:
                                        self.mostrar_tela_dormir()
                            elif tipo == "dormir":
                                self.mostrar_tela_dormir()
                            elif tipo == "acordar":
                                self.mudar_para_fase(0)
                            elif tipo == "sair":
                                pygame.quit()
                                return
                    else:  # estado "jogando"
                        if event.key == pygame.K_UP and self.direcao != Direcao.BAIXO:
                            self.proxima_direcao = Direcao.CIMA
                        elif event.key == pygame.K_DOWN and self.direcao != Direcao.CIMA:
                            self.proxima_direcao = Direcao.BAIXO
                        elif event.key == pygame.K_LEFT and self.direcao != Direcao.DIREITA:
                            self.proxima_direcao = Direcao.ESQUERDA
                        elif event.key == pygame.K_RIGHT and self.direcao != Direcao.ESQUERDA:
                            self.proxima_direcao = Direcao.DIREITA
            
            if self.estado == "jogando":
                self.mover_cobra()
                
                if agora - self.tempo_ultima_queima >= 1000:
                    self.calorias -= CALORIAS_POR_SEGUNDO
                    self.tempo_ultima_queima = agora
                    if self.calorias < CALORIAS_MIN:
                        self.calorias = CALORIAS_MIN
                    self.ajustar_tamanho()
                
                if self.verificar_colisao():
                    if self.game_over():
                        self.reset_jogo()
                    else:
                        pygame.quit()
                        return
                
                if self.verificar_alimento():
                    self.calorias += self.alimento_atual['energia_kcal']
                    self.pontuacao += self.alimento_atual['energia_kcal']
                    # Crescimento da cobra
                    desejado_antes = max(1, int((self.calorias - self.alimento_atual['energia_kcal']) // 100))
                    desejado_depois = max(1, int(self.calorias // 100))
                    for _ in range(desejado_depois - desejado_antes):
                        self.cobra.append(self.cobra[-1])  # adiciona um novo segmento na posição do último
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
                    self.preparar_menu_transicao()
            
            # Chamadas para o módulo desenho externo
            desenho.desenhar_fundo(self)
            desenho.desenhar_cobra(self)
            desenho.desenhar_alimento(self)
            desenho.desenhar_hud(self)
            
            if self.estado == "menu":
                desenho.desenhar_menu(self)
            elif self.estado == "dormir":
                desenho.desenhar_dormir(self)
            
            pygame.display.flip()
            self.clock.tick(VELOCIDADE)