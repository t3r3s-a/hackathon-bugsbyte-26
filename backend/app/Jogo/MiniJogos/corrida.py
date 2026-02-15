import pygame
import random
import sys
import constantes
import os

# Cores da paleta (igual ao desenho.py)
C_SNAKE_BODY = (249, 115, 22)       # Laranja claro para o corpo
C_SNAKE_HEAD = (190, 75, 0)         # Laranja escuro (fallback)
C_VERMELHO   = (220, 38, 38)
C_BRANCO     = (255, 255, 255)
C_VERDE      = (34, 197, 94)        # Usado para a relva (opcional)

def minigame_corrida(calorias):
    pygame.init()
    janela = pygame.display.set_mode((constantes.LARGURA_JANELA, constantes.ALTURA_JANELA))
    pygame.display.set_caption("Running Minigame")
    clock = pygame.time.Clock()

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # Carregar imagem da cabeça
    caminho_cabeca = os.path.join(BASE_DIR, "Fundos", "cabeca_snake.png")
    try:
        img_cabeca = pygame.image.load(caminho_cabeca).convert_alpha()
    except:
        img_cabeca = None

    # Número de segmentos da cobra (incluindo cabeça)
    num_segmentos = max(3, calorias // 100)  # pelo menos 3 para ter corpo

    # Posições iniciais (todos no mesmo y)
    y_fixo = constantes.ALTURA_JANELA // 2 - 25
    segmentos = []
    espacamento = 40  # Aumentado de 30 para 40
    for i in range(num_segmentos):
        segmentos.append([50 - i * espacamento, y_fixo])

    # Velocidade de avanço
    player_speed = 10
    goal_x = constantes.LARGURA_JANELA - 100
    last_key = None
    total_time = 10
    running = True

    while running:
        dt = clock.tick(60) / 1000
        total_time -= dt

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if total_time > 0:
                    # Movimento para a direita (alternando teclas)
                    if event.key == pygame.K_LEFT and last_key != 'q':
                        # Avança a cobra
                        # Move a cabeça
                        nova_cabeca = [segmentos[0][0] + player_speed, segmentos[0][1]]
                        # Insere nova cabeça
                        segmentos.insert(0, nova_cabeca)
                        # Remove a cauda (mantém o mesmo comprimento)
                        segmentos.pop()
                        last_key = 'q'
                    if event.key == pygame.K_RIGHT and last_key != 'e':
                        nova_cabeca = [segmentos[0][0] + player_speed, segmentos[0][1]]
                        segmentos.insert(0, nova_cabeca)
                        segmentos.pop()
                        last_key = 'e'

        # Verifica se a cabeça chegou à meta
        if segmentos[0][0] >= goal_x:
            return random.randint(200, 600)

        if total_time <= 0:
            return 0

        # Desenho
        janela.fill((221, 90, 17))  # cor de fundo laranja

        # Linhas da pista
        for offset in [-140, -75, -10, 55, 120, 185]:
            pygame.draw.rect(janela, C_BRANCO, (0, y_fixo + offset, constantes.LARGURA_JANELA, 5))

        # Meta
        pygame.draw.rect(janela, C_BRANCO, (goal_x, y_fixo - 150, 50, 400))

        # Relva (opcional, para manter estilo)
        pygame.draw.rect(janela, C_VERDE, (0, -65, constantes.LARGURA_JANELA, 300))
        pygame.draw.rect(janela, C_VERDE, (0, 565, constantes.LARGURA_JANELA, 300))

        # Desenha a cobra (do último segmento para a cabeça)
        for i in range(len(segmentos)-1, -1, -1):
            x, y = segmentos[i]
            if i == 0 and img_cabeca:
                # Desenha cabeça com imagem (sem rotação, pois só move lateralmente)
                cabeca_red = pygame.transform.scale(img_cabeca, (50, 50))
                janela.blit(cabeca_red, (x, y))
            else:
                # Desenha corpo
                cor = C_SNAKE_HEAD if i == 0 else C_SNAKE_BODY
                pygame.draw.rect(janela, cor, (x, y, 50, 50))
                if i != 0:
                    # Borda mais escura para os segmentos do corpo
                    pygame.draw.rect(janela, (139, 69, 19), (x, y, 50, 50), 2)

        # Texto do tempo
        font = pygame.font.SysFont(None, 40)
        timer_text = font.render(f"Tempo restante: {total_time:.1f}s", True, C_BRANCO)
        janela.blit(timer_text, (20, 20))

        # Texto "FINISH" vertical
        finish = font.render("F I N I S H", True, (221, 90, 17))
        finish_line = pygame.transform.rotate(finish, 270)
        janela.blit(finish_line, (goal_x + 10, y_fixo - 40))

        pygame.display.flip()

    return 0