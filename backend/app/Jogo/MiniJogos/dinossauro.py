import pygame
import random
import constantes
import os

# Cores da paleta
C_SNAKE_BODY = (160, 60, 0)
C_SNAKE_HEAD = (190, 75, 0)
C_OBSTACLE   = (220, 38, 38)

def minigame_dinossauro(calorias):
    pygame.init()

    GROUND_Y = constantes.ALTURA_JANELA - 80

    GRAVITY = 0.8
    JUMP_FORCE = -12
    OBS_SPEED = 6

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    caminho_bg = os.path.join(BASE_DIR, "Fundos", "background_dinossaur.png")

    screen = pygame.display.set_mode(
        (constantes.LARGURA_JANELA, constantes.ALTURA_JANELA)
    )
    pygame.display.set_caption("Minijogo Dinossauro")
    clock = pygame.time.Clock()

    background = pygame.image.load(caminho_bg).convert()
    background = pygame.transform.scale(
        background,
        (constantes.LARGURA_JANELA, constantes.ALTURA_JANELA)
    )

    # Carregar imagem da cabeça
    caminho_cabeca = os.path.join(BASE_DIR, "Fundos", "cabeca_snake.png")
    try:
        img_cabeca = pygame.image.load(caminho_cabeca).convert_alpha()
        img_cabeca = pygame.transform.scale(img_cabeca, (20, 20))
    except:
        img_cabeca = None

    head_x = 150
    head_y = GROUND_Y
    head_vel_y = 0
    head_on_ground = True

    num_segmentos = max(1, calorias // 100)
    DIST_SEG = 30
    DELAY_FRAMES = max(1, DIST_SEG // OBS_SPEED)

    input_buffer = []
    MAX_BUFFER = num_segmentos * DELAY_FRAMES + 20

    segmentos = [{"y": GROUND_Y, "vel_y": 0} for _ in range(num_segmentos)]

    obstaculos = []
    spawn_timer = 0

    def spawn_obstaculo():
        h = random.randint(30, 60)
        obstaculos.append(
            pygame.Rect(constantes.LARGURA_JANELA, GROUND_Y - h, 20, h)
        )

    tempo = 20.0

    running = True
    while running:
        dt = clock.tick(60) / 1000
        tempo -= dt
        jump_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return -1
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and head_on_ground:
                    head_vel_y = JUMP_FORCE
                    head_on_ground = False
                    jump_pressed = True

        input_buffer.insert(0, jump_pressed)
        if len(input_buffer) > MAX_BUFFER:
            input_buffer.pop()

        # Física cabeça
        head_vel_y += GRAVITY
        head_y += head_vel_y
        if head_y >= GROUND_Y:
            head_y = GROUND_Y
            head_vel_y = 0
            head_on_ground = True

        # Física cauda
        for i, seg in enumerate(segmentos):
            idx = (i + 1) * DELAY_FRAMES
            jump = input_buffer[idx] if idx < len(input_buffer) else False

            if jump and seg["y"] >= GROUND_Y:
                seg["vel_y"] = JUMP_FORCE

            seg["vel_y"] += GRAVITY
            seg["y"] += seg["vel_y"]

            if seg["y"] >= GROUND_Y:
                seg["y"] = GROUND_Y
                seg["vel_y"] = 0

        # Obstáculos
        spawn_timer += 1
        if spawn_timer > 90:
            spawn_timer = 0
            spawn_obstaculo()

        for obs in obstaculos:
            obs.x -= OBS_SPEED
        obstaculos = [o for o in obstaculos if o.x > -50]

        # Colisão cabeça
        head_rect = pygame.Rect(head_x - 10, head_y - 10, 20, 20)
        for obs in obstaculos:
            if head_rect.colliderect(obs):
                return 0

        if tempo <= 0:
            return random.randint(100, 200)

        # Desenho
        screen.blit(background, (0, 0))

        caminho_chao = os.path.join(BASE_DIR, "Fundos", "chao_dinossaur.png")
        chao_img = pygame.image.load(caminho_chao).convert_alpha()
        chao_img = pygame.transform.scale(chao_img, (constantes.LARGURA_JANELA, 100))
        screen.blit(chao_img, (0, GROUND_Y + 10))

        for obs in obstaculos:
            pygame.draw.rect(screen, C_OBSTACLE, obs)

        # Desenha cauda
        for i in reversed(range(num_segmentos)):
            x = head_x - (i + 1) * DIST_SEG
            y = segmentos[i]["y"]
            pygame.draw.rect(screen, C_SNAKE_BODY, (x - 8, y - 8, 16, 16))

        # Desenha cabeça
        if img_cabeca:
            rotated_head = pygame.transform.rotate(img_cabeca, -90)
            screen.blit(rotated_head, (head_x - 10, head_y - 10))
        else:
            pygame.draw.rect(screen, C_SNAKE_HEAD, (head_x - 10, head_y - 10, 20, 20))

        font = pygame.font.SysFont(None, 30)
        txt = font.render(f"{tempo:.1f}s", True, (255, 255, 255))
        screen.blit(txt, (20, 20))

        pygame.display.flip()

    return 0