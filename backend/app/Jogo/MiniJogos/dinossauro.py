def minigame_dinossauro(calorias):
    import pygame, random, sys

    pygame.init()

    WIDTH, HEIGHT = 900, 400
    GROUND_Y = HEIGHT - 80

    GRAVITY = 0.8
    JUMP_FORCE = -12
    OBS_SPEED = 6

    # cauda baseada nas calorias
    num_segmentos = max(1, calorias // 100)
    DIST_SEG = 30
    DELAY_FRAMES = max(1, DIST_SEG // OBS_SPEED)

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minijogo Dinossauro")
    clock = pygame.time.Clock()

    # ======================
    # CABEÇA
    # ======================
    head_x = 150
    head_y = GROUND_Y
    head_vel_y = 0
    head_on_ground = True

    # buffer inputs
    input_buffer = []
    MAX_BUFFER = num_segmentos * DELAY_FRAMES + 20

    # segmentos físicos
    segmentos = [{"y": GROUND_Y, "vel_y": 0} for _ in range(num_segmentos)]

    # obstáculos
    obstaculos = []
    spawn_timer = 0

    def spawn_obstaculo():
        h = random.randint(30, 60)
        obstaculos.append(pygame.Rect(WIDTH, GROUND_Y - h, 20, h))

    # timer 10 segundos
    tempo = 10.0

    running = True
    while running:
        dt = clock.tick(60) / 1000
        tempo -= dt
        jump_pressed = False

        # INPUT
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 0

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and head_on_ground:
                    head_vel_y = JUMP_FORCE
                    head_on_ground = False
                    jump_pressed = True

        # guardar input
        input_buffer.insert(0, jump_pressed)
        if len(input_buffer) > MAX_BUFFER:
            input_buffer.pop()

        # física cabeça
        head_vel_y += GRAVITY
        head_y += head_vel_y
        if head_y >= GROUND_Y:
            head_y = GROUND_Y
            head_vel_y = 0
            head_on_ground = True

        # física cauda
        for i, seg in enumerate(segmentos):
            idx = (i+1) * DELAY_FRAMES
            jump = input_buffer[idx] if idx < len(input_buffer) else False

            if jump and seg["y"] >= GROUND_Y:
                seg["vel_y"] = JUMP_FORCE

            seg["vel_y"] += GRAVITY
            seg["y"] += seg["vel_y"]

            if seg["y"] >= GROUND_Y:
                seg["y"] = GROUND_Y
                seg["vel_y"] = 0

        # obstáculos
        spawn_timer += 1
        if spawn_timer > 90:
            spawn_timer = 0
            spawn_obstaculo()

        for obs in obstaculos:
            obs.x -= OBS_SPEED
        obstaculos = [o for o in obstaculos if o.x > -50]

        # colisão cabeça
        head_rect = pygame.Rect(head_x - 10, head_y - 10, 20, 20)
        for obs in obstaculos:
            if head_rect.colliderect(obs):
                pygame.quit()
                return 0  # morreu

        # ganhou (sobreviveu 10s)
        if tempo <= 0:
            pygame.quit()
            return random.randint(100, 200)

        # desenho simples
        screen.fill((30, 30, 30))
        pygame.draw.rect(screen, (70, 70, 70), (0, GROUND_Y + 10, WIDTH, 100))

        for obs in obstaculos:
            pygame.draw.rect(screen, (200, 50, 50), obs)

        # cauda
        for i in reversed(range(num_segmentos)):
            x = head_x - (i + 1) * DIST_SEG
            y = segmentos[i]["y"]
            pygame.draw.rect(screen, (0, 200, 0), (x - 8, y - 8, 16, 16))

        # cabeça
        pygame.draw.rect(screen, (0, 255, 0), (head_x - 10, head_y - 10, 20, 20))

        # timer UI
        font = pygame.font.SysFont(None, 30)
        txt = font.render(f"{tempo:.1f}s", True, (255, 255, 255))
        screen.blit(txt, (20, 20))

        pygame.display.flip()
