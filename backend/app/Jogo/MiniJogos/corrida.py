import pygame
import random
import sys
import constantes

def minigame_corrida(calorias):
    pygame.init()
    janela = pygame.display.set_mode((constantes.LARGURA_JANELA, constantes.ALTURA_JANELA))
    pygame.display.set_caption("Running Minigame")
    player_x = 50
    player_y = constantes.ALTURA_JANELA // 2 - 25
    player_speed = 10
    goal_x = constantes.LARGURA_JANELA - 100
    last_key = None
    total_time = 10
    clock = pygame.time.Clock()
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
                    if event.key == pygame.K_q and last_key != 'q':
                        player_x += player_speed
                        last_key = 'q'
                    if event.key == pygame.K_e and last_key != 'e':
                        player_x += player_speed
                        last_key = 'e'
        if player_x >= goal_x:
            return random.randint(200, 600)
        if total_time <= 0:
            return 0
        janela.fill((221, 90, 17))
        pygame.draw.rect(janela, (255, 255, 255), (goal_x, player_y - 150, 50, 400))
        pygame.draw.rect(janela, (255, 255, 255), (0, player_y - 140, 900, 5))
        pygame.draw.rect(janela, (255, 255, 255), (0, player_y - 75, 900, 5))
        pygame.draw.rect(janela, (255, 255, 255), (0, player_y - 10, 900, 5))
        pygame.draw.rect(janela, (255, 255, 255), (0, player_y + 55, 900, 5))
        pygame.draw.rect(janela, (255, 255, 255), (0, player_y + 120, 900, 5))
        pygame.draw.rect(janela, (255, 255, 255), (0, player_y + 185, 900, 5))
        pygame.draw.rect(janela, (0, 255, 0), (player_x, player_y, 50, 50))
        pygame.draw.rect(janela, (0, 255, 0), (0, -65, 900, 300))
        pygame.draw.rect(janela, (0, 255, 0), (0, 565, 900, 300))
        font = pygame.font.SysFont(None, 40)
        timer_text = font.render(f"Tempo restante: {total_time:.1f}s", True, (255, 255, 255))
        janela.blit(timer_text, (20, 20))
        finish = font.render("F I N I S H", True, (221, 90, 17))
        finish_line = pygame.transform.rotate(finish, 270)
        janela.blit(finish_line, (goal_x + 10, player_y - 40))
        pygame.display.flip()
    
    return 0