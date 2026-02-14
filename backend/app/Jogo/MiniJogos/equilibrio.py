import pygame
import math
import random
import constantes
import os

# Cores da paleta (igual ao desenho.py)
C_SNAKE_BODY = (249, 115, 22)       # Cor do corpo (laranja claro)
C_SNAKE_HEAD = (190, 75, 0)         # Cor da cabeça (caso a imagem falhe)
C_VERMELHO   = (220, 38, 38)

def minigame_equilibrio(calorias):
    pygame.init()
    TELA = pygame.display.set_mode((constantes.LARGURA_JANELA, constantes.ALTURA_JANELA))
    pygame.display.set_caption("Equilíbrio na Cobra")
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    # Carrega fundo e chão
    caminho_bg = os.path.join(BASE_DIR, "Fundos", "background_equilibrio.png")
    background = pygame.image.load(caminho_bg).convert()
    background = pygame.transform.scale(background, (constantes.LARGURA_JANELA, constantes.ALTURA_JANELA))

    ALTURA_CHAO = 100
    caminho_chao = os.path.join(BASE_DIR, "Fundos", "chao_equilibrio.png")
    chao_img = pygame.image.load(caminho_chao).convert_alpha()
    chao_img = pygame.transform.scale(chao_img, (constantes.LARGURA_JANELA, ALTURA_CHAO))

    # Carrega imagem da cabeça
    caminho_cabeca = os.path.join(BASE_DIR, "Fundos", "cabeca_snake.png")
    try:
        img_cabeca = pygame.image.load(caminho_cabeca).convert_alpha()
    except:
        img_cabeca = None

    clock = pygame.time.Clock()

    # Número de segmentos baseado nas calorias
    num_segmentos = max(1, calorias // 100)

    class CobraEquilibrio:
        def __init__(self, num_seg):
            self.tamanho_celula = 20
            self.num_segmentos = num_seg
            self.pivo = (constantes.LARGURA_JANELA // 2, constantes.ALTURA_JANELA - ALTURA_CHAO)

            # Posições relativas ao pivô: a cabeça é a mais distante (maior y negativo)
            # Vamos construir a lista da ponta (cabeça) até a base.
            # Assim, self.rel_pos[0] será a cabeça.
            self.rel_pos = [(0, -i * self.tamanho_celula) for i in range(self.num_segmentos-1, -1, -1)]

            self.angulo = 0.0
            self.vel_angular = 0.0
            self.forca_perturbacao = 0.02
            self.intervalo_perturbacao = 30
            self.tempo_perturbacao = 0
            self.direcao_perturbacao = 0

        def aplicar_rotacao(self, ponto, angulo):
            cos_a = math.cos(angulo)
            sin_a = math.sin(angulo)
            x, y = ponto
            return (x * cos_a - y * sin_a, x * sin_a + y * cos_a)

        def atualizar_equilibrio(self, teclas):
            if teclas[pygame.K_LEFT]:
                self.vel_angular -= 0.005
            if teclas[pygame.K_RIGHT]:
                self.vel_angular += 0.005

            self.tempo_perturbacao += 1
            if self.tempo_perturbacao >= self.intervalo_perturbacao:
                self.tempo_perturbacao = 0
                self.direcao_perturbacao = random.choice([-1, -1, 0, 1, 1])
                self.vel_angular += self.direcao_perturbacao * self.forca_perturbacao

            self.vel_angular *= 0.98
            self.angulo += self.vel_angular
            return abs(self.angulo) <= 0.9

        def desenhar(self, tela, img_cabeca):
            # Desenha os segmentos do último (base) para o primeiro (cabeça) para sobreposição correta
            for i in range(self.num_segmentos - 1, -1, -1):
                rel = self.rel_pos[i]
                rot = self.aplicar_rotacao(rel, self.angulo)
                x = self.pivo[0] + rot[0]
                y = self.pivo[1] + rot[1]

                if i == 0 and img_cabeca:  # i=0 é a cabeça (ponta)
                    cabeca_rot = pygame.transform.rotate(img_cabeca, -math.degrees(self.angulo))
                    rect_cabeca = cabeca_rot.get_rect(center=(x, y))
                    tela.blit(cabeca_rot, rect_cabeca)
                else:
                    cor = C_SNAKE_HEAD if i == 0 else C_SNAKE_BODY
                    pygame.draw.rect(tela, cor,
                                     (x - self.tamanho_celula // 2,
                                      y - self.tamanho_celula // 2,
                                      self.tamanho_celula,
                                      self.tamanho_celula))
                    if i != 0:
                        # Borda mais escura para os segmentos do corpo (opcional)
                        pygame.draw.rect(tela, (139, 69, 19),
                                         (x - self.tamanho_celula // 2,
                                          y - self.tamanho_celula // 2,
                                          self.tamanho_celula,
                                          self.tamanho_celula), 2)

            # Desenha seta de perturbação
            if self.direcao_perturbacao != 0:
                centro = (self.pivo[0] + self.direcao_perturbacao * 80, self.pivo[1] + 30)
                fim = (centro[0] + self.direcao_perturbacao * 75, centro[1])
                pygame.draw.line(tela, C_VERMELHO, centro, fim, 4)
                if self.direcao_perturbacao > 0:
                    pygame.draw.polygon(tela, C_VERMELHO,
                                        [(fim[0], fim[1]),
                                         (fim[0] - 10, fim[1] - 5),
                                         (fim[0] - 10, fim[1] + 5)])
                elif self.direcao_perturbacao < 0:
                    pygame.draw.polygon(tela, C_VERMELHO,
                                        [(fim[0], fim[1]),
                                         (fim[0] + 10, fim[1] - 5),
                                         (fim[0] + 10, fim[1] + 5)])

    cobra = CobraEquilibrio(num_segmentos)
    tempo_restante = 10.0
    rodando = True

    while rodando:
        dt = clock.tick(60) / 1000
        tempo_restante -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1

        teclas = pygame.key.get_pressed()

        if not cobra.atualizar_equilibrio(teclas):
            break
        if tempo_restante <= 0:
            break

        TELA.blit(background, (0, 0))
        TELA.blit(chao_img, (10, constantes.ALTURA_JANELA - ALTURA_CHAO))
        # Reduz o tamanho da cabeça da cobra e a rotaciona 45º
        if img_cabeca:
            img_cabeca_redimensionada = pygame.transform.scale(img_cabeca, (int(img_cabeca.get_width() * 0.8), int(img_cabeca.get_height() * 0.8)))
            img_cabeca_rotacionada = pygame.transform.rotate(img_cabeca_redimensionada, -90)
        else:
            img_cabeca_rotacionada = None

        cobra.desenhar(TELA, img_cabeca_rotacionada)

        fonte = pygame.font.Font(None, 30)
        texto_tempo = fonte.render(f"{tempo_restante:.1f}s", True, (0, 0, 0))
        TELA.blit(texto_tempo, (10, 10))

        pygame.display.flip()

    if tempo_restante <= 0:
        return random.randint(100, 200)
    else:
        return 0