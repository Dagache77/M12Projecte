import pygame
import sys
import random
import time

# Inicialización
pygame.init()

# Configuración de pantalla
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Head Ball 1v1")
clock = pygame.time.Clock()

# Colores
VERD = (0, 200, 0)
BLANC = (255, 255, 255)
NEGRE = (0, 0, 0)
ROIG = (255, 50, 50)
BLAU = (50, 50, 255)
GRIS = (200, 200, 200)

font = pygame.font.SysFont(None, 72)

def mostrar_menu():
    # Reproducir música del menú
    try:
        pygame.mixer.music.load("assets/menu.mp3")
        pygame.mixer.music.play(-1)
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'menu.mp3' en la carpeta 'assets'.")

    # Mostrar imagen del menú
    try:
        menu_img = pygame.image.load("assets/menu.png").convert_alpha()
        menu_img = pygame.transform.scale(menu_img, (WIDTH, HEIGHT))
        screen.blit(menu_img, (0, 0))
    except FileNotFoundError:
        screen.fill(BLANC)
        error_text = font.render("menu.png no encontrado en 'assets'", True, ROIG)
        screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT // 2 - error_text.get_height() // 2))

    pygame.display.flip()
    esperar_tecla_menu()
    pygame.mixer.music.stop()

def mostrar_menu_personajes():
    try:
        personajes_img = pygame.image.load("assets/menu-personajes.png").convert_alpha()
        personajes_img = pygame.transform.scale(personajes_img, (WIDTH, HEIGHT))
        screen.blit(personajes_img, (0, 0))
    except FileNotFoundError:
        screen.fill(BLANC)
        error_text = font.render("menu-personajes.png no encontrado en 'assets'", True, ROIG)
        screen.blit(error_text, (WIDTH // 2 - error_text.get_width() // 2, HEIGHT // 2 - error_text.get_height() // 2))

    pygame.display.flip()

    selected_p1 = None
    selected_p2 = None
    x_start = 50
    y_start = 200
    gap = 250
    personajes_rects = {}

    personajes = {
        "VINICIUS": pygame.image.load("assets/Vini.png"),
        "MESSI": pygame.image.load("assets/messi.png"),
    }

    for i, (key, img) in enumerate(personajes.items()):
        personajes[key] = pygame.transform.scale(img, (150, 150))
        x = x_start + (i % 5) * gap
        y = y_start + (i // 5) * gap
        personajes_rects[key] = pygame.Rect(x, y, 150, 150)

    while True:
        screen.blit(personajes_img, (0, 0))
        for key, rect in personajes_rects.items():
            screen.blit(personajes[key], (rect.x, rect.y))

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for key, rect in personajes_rects.items():
                    if rect.collidepoint(mouse_pos):
                        if not selected_p1:
                            selected_p1 = key
                        elif not selected_p2:
                            selected_p2 = key
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and selected_p1 and selected_p2:
                    return selected_p1, selected_p2

def esperar_tecla_menu():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    pygame.mixer.music.stop()
                    jugar()
                    return
                elif event.key == pygame.K_p:
                    selected_p1, selected_p2 = mostrar_menu_personajes()
                    print(f"Jugador 1: {selected_p1}, Jugador 2: {selected_p2}")
                    jugar()
                    return

def jugar():
    # Música de fondo para el juego
    try:
        pygame.mixer.music.load("assets/ambiente.mp3")
        pygame.mixer.music.play(-1)
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'ambiente.mp3' en la carpeta 'assets'.")

    # Personajes aún más grandes
    PLAYER_WIDTH, PLAYER_HEIGHT = 270, 200  # Más grandes
    BALL_RADIUS = 30

    # --- Ajuste: centra la imagen del jugador en el área de colisión circular ---
    # El área de colisión circular estará centrada en la cabeza (parte superior central de la imagen)
    HEAD_RADIUS = PLAYER_WIDTH // 2 - 10
    HEAD_CENTER_OFFSET_Y = 60  # Ajusta este valor para que el círculo de colisión esté en la cabeza

    # Altura base de los personajes
    player1_y = HEIGHT - PLAYER_HEIGHT
    player2_y = HEIGHT - PLAYER_HEIGHT

    player1 = pygame.Rect(10, player1_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    player2 = pygame.Rect(WIDTH - 10 - PLAYER_WIDTH, player2_y, PLAYER_WIDTH, PLAYER_HEIGHT)

    # El balón a la misma altura que la base de los personajes
    ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT - PLAYER_HEIGHT - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_vel = [4, 0]

    player1_vel = [0, 0]
    player2_vel = [0, 0]
    player_speed = 7
    jump_strength = -15
    gravity = 0.7
    on_ground1 = True
    on_ground2 = True

    # Área de colisión (muro invisible)
    jugador1 = pygame.Rect(100, 500, 50, 50)  # <-- Esto define la colisión y el movimiento

    # Imagen visual (puede ser de otro tamaño)

    jugador1_img = pygame.image.load("assets/lewan.png")
    jugador1_img = pygame.transform.scale(jugador1_img, (60, 60))

    # Dibujo la imagen en la posición del rectángulo
    screen.blit(jugador1_img, (jugador1.x, jugador1.y))

    # Cargar imágenes y ajustarlas al nuevo tamaño grande
    try:
        player1_image = pygame.image.load("assets/lewan.png").convert_alpha()
        player1_image = pygame.transform.scale(player1_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        player2_image = pygame.image.load("assets/haaland.png").convert_alpha()
        player2_image = pygame.transform.scale(player2_image, (PLAYER_WIDTH, PLAYER_HEIGHT))
        player2_image = pygame.transform.flip(player2_image, True, False)
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo {e.filename} en la carpeta 'assets'.")
        pygame.quit()
        sys.exit()

    try:
        field_image = pygame.image.load("assets/campo.png").convert_alpha()
        field_image = pygame.transform.scale(field_image, (WIDTH, HEIGHT))
    except FileNotFoundError:
        print("Error: No se encuentra el archivo 'campo.png' en la carpeta 'assets'.")
        pygame.quit()
        sys.exit()

    try:
        ball_image = pygame.image.load("assets/balon.png").convert_alpha()
        ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))
    except FileNotFoundError:
        print("Error: No se encuentra el archivo 'balon.png' en la carpeta 'assets'.")
        pygame.quit()
        sys.exit()

    # Crear máscaras para los personajes
    player1_mask = pygame.mask.from_surface(player1_image)
    player2_mask = pygame.mask.from_surface(player2_image)

    # Detectar colisión entre los personajes
    offset = (player2.x - player1.x, player2.y - player1.y)
    collision = player1_mask.overlap(player2_mask, offset)

    if collision:
        print("Colisión detectada entre los personajes")

    # Puntos clave del jugador 1
    player1_head = (player1.centerx, player1.top)
    player1_feet = (player1.centerx, player1.bottom)

    # Verificar si los puntos clave están dentro del rectángulo del jugador 2
    if player2.collidepoint(player1_head) or player2.collidepoint(player1_feet):
        print("Colisión detectada entre los personajes")

    if player1.colliderect(player2):
        if player1.right > player2.left:
            player1.x -= 5  # Empujar al jugador 1 hacia la izquierda
        if player2.left < player1.right:
            player2.x += 5  # Empujar al jugador 2 hacia la derecha

    player1_collision_rect = player1.inflate(-50, -50)
    player2_collision_rect = player2.inflate(-50, -50)

    if player1_collision_rect.colliderect(player2_collision_rect):
        print("Colisión detectada con áreas reducidas")

    
    # Crear rectángulos de colisión más pequeños
    player1_collision_rect = player1.inflate(-80, -80)
    player2_collision_rect = player2.inflate(-80, -80)

    # Usar estos para la colisión entre personajes
    if player1_collision_rect.colliderect(player2_collision_rect):
        # Lógica de colisión aquí
        print("Colisión detectada con muro más pequeño")


    # Tamaño único para ambos: colisión y visual
    PLAYER_WIDTH, PLAYER_HEIGHT = 100, 100
    player1 = pygame.Rect(100, 500, PLAYER_WIDTH, PLAYER_HEIGHT)
    player1_img = pygame.image.load('assets/lewan.png').convert_alpha()
    player1_img = pygame.transform.scale(player1_img, (PLAYER_WIDTH, PLAYER_HEIGHT))

    # Dibuja la imagen alineada con el rectángulo de colisión
    screen.blit(player1_img, (player1.x, player1.y))

    score1 = 0
    score2 = 0
    TOTAL_TIME = 40
    start_ticks = pygame.time.get_ticks()
    ball_reset_time = None

    def reset_ball():
        nonlocal ball_reset_time
        # El balón a la misma altura que la base de los personajes
        ball.x = WIDTH // 2 - BALL_RADIUS
        ball.y = HEIGHT - PLAYER_HEIGHT - BALL_RADIUS * 2
        ball_vel[0] = 0
        ball_vel[1] = 0
        ball_reset_time = pygame.time.get_ticks() + 2000

    def activate_ball():
        ball_vel[0] = random.choice([-4, 4])
        ball_vel[1] = 0

    def show_end_message(winner):
        screen.fill(BLANC)
        if winner == "Empate":
            message = font.render("¡Empate!", True, ROIG)
        else:
            message = font.render(f"Ganador: {winner}", True, ROIG)
        screen.blit(message, (WIDTH // 2 - message.get_width() // 2, HEIGHT // 2 - message.get_height() // 2))
        pygame.display.flip()
        pygame.time.wait(3000)

    player1_stats = {"speed": player_speed, "jump_strength": jump_strength}

    running = True
    while running:
        clock.tick(60)
        screen.blit(field_image, (0, 0))
        pygame.draw.line(screen, BLANC, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)
        # --- Dibuja la imagen del jugador alineada con el rectángulo ---
        screen.blit(player1_image, (player1.x, player1.y))
        screen.blit(player2_image, (player2.x, player2.y))
        screen.blit(ball_image, (ball.x, ball.y))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Actualizar el tiempo restante
        seconds_passed = (pygame.time.get_ticks() - start_ticks) // 1000
        time_remaining = TOTAL_TIME - seconds_passed

        if time_remaining <= 0:
            if score1 > score2:
                show_end_message("Jugador 1")
            elif score2 > score1:
                show_end_message("Jugador 2")
            else:
                show_end_message("Empate")
            running = False
            continue

        # Mostrar la puntuación y el tiempo restante
        score_text = font.render(f"{score1} - {score2}", True, NEGRE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        time_text = font.render(f"{max(0, time_remaining)}s", True, NEGRE)
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 100))

        # Controles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player1.left > 0:
            player1.x -= player1_stats["speed"]
        if keys[pygame.K_d] and player1.right < WIDTH:
            player1.x += player1_stats["speed"]
        if keys[pygame.K_w] and on_ground1:
            player1_vel[1] = player1_stats["jump_strength"]
            on_ground1 = False

        if keys[pygame.K_LEFT] and player2.left > 0:
            player2.x -= player_speed
        if keys[pygame.K_RIGHT] and player2.right < WIDTH:
            player2.x += player_speed
        if keys[pygame.K_UP] and on_ground2:
            player2_vel[1] = jump_strength
            on_ground2 = False

        # Gravedad y movimiento vertical
        player1_vel[1] += gravity
        player2_vel[1] += gravity
        player1.y += player1_vel[1]
        player2.y += player2_vel[1]

        # Límite suelo
        if player1.bottom >= HEIGHT:
            player1.bottom = HEIGHT
            on_ground1 = True
            player1_vel[1] = 0
        if player2.bottom >= HEIGHT:
            player2.bottom = HEIGHT
            on_ground2 = True
            player2_vel[1] = 0

        # Movimiento de la pelota
        if ball_reset_time and pygame.time.get_ticks() >= ball_reset_time:
            activate_ball()
            ball_reset_time = None

        ball.x += ball_vel[0]
        ball.y += ball_vel[1]
        ball_vel[1] += gravity

        # Rebotes en los bordes
        bounce_damping = 0.8
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_vel[0] *= -1
        if ball.top <= 0:
            ball.top = 0
            ball_vel[1] *= -1
        if ball.bottom >= HEIGHT:
            ball.bottom = HEIGHT
            ball_vel[1] *= -bounce_damping
            if abs(ball_vel[1]) < 1:
                ball_vel[1] = 0

        # Colisiones con los jugadores (ajustadas para el tamaño grande)
        if player1.colliderect(ball):
            if ball.bottom > player1.top and ball.top < player1.bottom:
                if ball.centerx > player1.centerx:
                    ball_vel[0] = 4
                else:
                    ball_vel[0] = -4
                ball_vel[1] = -5
        if player2.colliderect(ball):
            if ball.bottom > player2.top and ball.top < player2.bottom:
                if ball.centerx > player2.centerx:
                    ball_vel[0] = 4
                else:
                    ball_vel[0] = -4
                ball_vel[1] = -5

        # --- Mejora de colisiones entre jugadores y balón usando máscaras circulares ---
        # Definir círculos de colisión para los jugadores (centrados en la cabeza)
        player1_head_center = (player1.x + PLAYER_WIDTH // 2, player1.y + HEAD_CENTER_OFFSET_Y)
        player2_head_center = (player2.x + PLAYER_WIDTH // 2, player2.y + HEAD_CENTER_OFFSET_Y)
        player_radius = HEAD_RADIUS

        # Centro y radio del balón
        ball_center = (ball.x + BALL_RADIUS, ball.y + BALL_RADIUS)
        ball_radius = BALL_RADIUS

        def circles_collide(center1, radius1, center2, radius2):
            dx = center1[0] - center2[0]
            dy = center1[1] - center2[1]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            return distance < (radius1 + radius2)

        # Colisión jugador 1 - balón
        if circles_collide(player1_head_center, player_radius, ball_center, ball_radius):
            dx = ball_center[0] - player1_head_center[0]
            dy = ball_center[1] - player1_head_center[1]
            dist = max((dx ** 2 + dy ** 2) ** 0.5, 1)
            ball_vel[0] = int(7 * dx / dist)
            ball_vel[1] = int(7 * dy / dist) - 5

        # Colisión jugador 2 - balón
        if circles_collide(player2_head_center, player_radius, ball_center, ball_radius):
            dx = ball_center[0] - player2_head_center[0]
            dy = ball_center[1] - player2_head_center[1]
            dist = max((dx ** 2 + dy ** 2) ** 0.5, 1)
            ball_vel[0] = int(7 * dx / dist)
            ball_vel[1] = int(7 * dy / dist) - 5

        # --- Mejora de colisión entre jugadores (empuje suave, usando la cabeza) ---
        dx = player1_head_center[0] - player2_head_center[0]
        dy = player1_head_center[1] - player2_head_center[1]
        dist = (dx ** 2 + dy ** 2) ** 0.5
        min_dist = player_radius * 2 - 10
        if dist < min_dist and dist > 0:
            overlap = min_dist - dist
            push_x = int(overlap * dx / dist / 2)
            push_y = int(overlap * dy / dist / 2)
            player1.x += push_x
            player2.x -= push_x
            player1.y += push_y
            player2.y -= push_y

        # Comprobar si el balón entra en las porterías

     
        # Definir porterías antes del bucle principal en jugar()
        GOAL_WIDTH, GOAL_HEIGHT = 100, 200
        goal1 = pygame.Rect(0, HEIGHT - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT)
        goal2 = pygame.Rect(WIDTH - GOAL_WIDTH, HEIGHT - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT)

        if ball.colliderect(goal1):
            score2 += 1
            reset_ball()
        if ball.colliderect(goal2):
            score1 += 1
            reset_ball()

        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Iniciar el programa
if __name__ == "__main__":
    mostrar_menu()
