import pygame
import sys
import random

# Inicialización
pygame.init()

# Configuración de audio
pygame.mixer.init()

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

# Función para mostrar el menú principal
def mostrar_menu():
    # Reproducir música del menú
    try:
        pygame.mixer.music.load("assets/menu.mp3")  # Ruta de la música del menú
        pygame.mixer.music.play(-1)  # Repetir indefinidamente
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

    # Mensaje para iniciar el juego
    start_text = font.render("Presiona ENTER para jugar", True, NEGRE)
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT - 100))
    pygame.display.flip()
    esperar_tecla_menu()

    pygame.mixer.music.stop()  # Detener la música del menú

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
    y_start = 50
    gap = 250  # Aumentar el espacio entre personajes
    personajes_rects = {}

    personajes = {
        "VINICIUS": pygame.image.load("assets/Vini.png"),
        "MESSI": pygame.image.load("assets/messi.png"),
    }

    for i, (key, img) in enumerate(personajes.items()):
        personajes[key] = pygame.transform.scale(img, (150, 150))  # Cambiar tamaño a 150x150
        x = x_start + (i % 5) * gap
        y = y_start + (i // 5) * gap
        personajes_rects[key] = pygame.Rect(x, y, 150, 150)  # Ajustar tamaño

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
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Cambiar de K_p a K_RETURN
                    jugar()  # Llamar directamente a jugar
                    return
                elif event.key == pygame.K_p:  # Opcional: mantener esta lógica si quieres incluir el menú de personajes
                    selected_p1, selected_p2 = mostrar_menu_personajes()
                    print(f"Jugador 1: {selected_p1}, Jugador 2: {selected_p2}")
                    jugar()
                    return
    # Música de fondo para el juego
    try:
        pygame.mixer.music.load("assets/ambiente.mp3")  # Ruta de la música de ambiente
        pygame.mixer.music.play(-1)  # Repetir indefinidamente
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'ambiente.mp3' en la carpeta 'assets'.")

def jugar():
    # Música de fondo para el juego
    try:
        pygame.mixer.music.load("assets/ambiente.mp3")  # Ruta de la música de ambiente
        pygame.mixer.music.play(-1)  # Repetir indefinidamente
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'ambiente.mp3' en la carpeta 'assets'.")

    PLAYER_WIDTH, PLAYER_HEIGHT = 300, 200  # Tamaño aumentado de los jugadores
    BALL_RADIUS = 30  # Tamaño del balón

    # Posicionar a los jugadores a la misma altura que el balón
    player1_y = HEIGHT - BALL_RADIUS * 2 - PLAYER_HEIGHT
    player2_y = HEIGHT - BALL_RADIUS * 2 - PLAYER_HEIGHT

    player1 = pygame.Rect(100, player1_y, PLAYER_WIDTH, PLAYER_HEIGHT)
    player2 = pygame.Rect(WIDTH - 250, player2_y, PLAYER_WIDTH, PLAYER_HEIGHT)

    player1_vel = [0, 0]
    player2_vel = [0, 0]
    player_speed = 7
    jump_strength = -15
    gravity = 0.7
    on_ground1 = True
    on_ground2 = True

    # Cargar las imágenes de los jugadores
    try:
        # Jugador 1 (Lewandowski)
        player1_image = pygame.image.load("assets/lewan.png").convert_alpha()
        player1_image = pygame.transform.scale(player1_image, (PLAYER_WIDTH, PLAYER_HEIGHT))  # Escalar tamaño al nuevo tamaño

        # Jugador 2 (Haaland)
        player2_image = pygame.image.load("assets/haaland.png").convert_alpha()
        player2_image = pygame.transform.scale(player2_image, (PLAYER_WIDTH, PLAYER_HEIGHT))  # Escalar tamaño al nuevo tamaño
        player2_image = pygame.transform.flip(player2_image, True, False)  # Voltear horizontalmente para que mire a la izquierda
    except FileNotFoundError as e:
        print(f"Error: No se encontró el archivo {e.filename} en la carpeta 'assets'.")
        pygame.quit()
        sys.exit()

    # Cargar la imagen del campo
    try:
        field_image = pygame.image.load("assets/campo.png").convert_alpha()
        field_image = pygame.transform.scale(field_image, (WIDTH, HEIGHT))  # Escalar al tamaño de la pantalla
    except FileNotFoundError:
        print("Error: No se encuentra el archivo 'campo.png' en la carpeta 'assets'.")
        pygame.quit()
        sys.exit()

    # Cargar la imagen del balón
    ball_image = pygame.image.load("assets/balon.png").convert_alpha()
    ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))  # Ajustar el tamaño de la imagen

    # Crear un rectángulo para manejar la posición y colisiones del balón
    ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_vel = [4, 0]

    # Configurar las porterías
    GOAL_WIDTH, GOAL_HEIGHT = 100, 200  # Hacer las porterías más anchas
    goal1 = pygame.Rect(0, HEIGHT - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT)
    goal2 = pygame.Rect(WIDTH - GOAL_WIDTH, HEIGHT - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT)

    score1 = 0
    score2 = 0
    TOTAL_TIME = 120
    start_ticks = pygame.time.get_ticks()
    ball_reset_time = None

    def reset_ball():
        nonlocal ball_reset_time
        ball.x = WIDTH // 2 - BALL_RADIUS
        ball.y = HEIGHT - BALL_RADIUS * 2
        ball_vel[0] = 0
        ball_vel[1] = 0
        ball_reset_time = pygame.time.get_ticks() + 2000

    def activate_ball():
        ball_vel[0] = random.choice([-4, 4])
        ball_vel[1] = 0

    running = True
    while running:
        clock.tick(60)

        # Dibujar el campo como fondo
        screen.blit(field_image, (0, 0))

        # Dibujar la línea central del campo
        pygame.draw.line(screen, BLANC, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

        # Dibujar los jugadores con sus imágenes
        screen.blit(player1_image, (player1.x, player1.y))
        screen.blit(player2_image, (player2.x, player2.y))

        # Dibujar el balón
        screen.blit(ball_image, (ball.x, ball.y))

        # Resto del código del juego...

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

        # Manejar eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Manejar controles de los jugadores
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player1.left > 0:
            player1.x -= player_speed
        if keys[pygame.K_d] and player1.right < WIDTH:
            player1.x += player_speed
        if keys[pygame.K_w] and on_ground1:
            player1_vel[1] = jump_strength
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

        if ball.left <= 0 or ball.right >= WIDTH:
            ball_vel[0] *= -1
        if ball.top <= 0:
            ball.top = 0
            ball_vel[1] *= -1
        if ball.bottom >= HEIGHT:
            ball.bottom = HEIGHT
            ball_vel[1] *= -0.8
            if abs(ball_vel[1]) < 1:
                ball_vel[1] = 0

        if player1.colliderect(ball):
            ball_vel[0] = 4
            ball_vel[1] = -5
        if player2.colliderect(ball):
            ball_vel[0] = -4
            ball_vel[1] = -5

        # Comprobar si el balón entra en las porterías
        if ball.colliderect(goal1):
            score2 += 1
            reset_ball()
        if ball.colliderect(goal2):
            score1 += 1
            reset_ball()

        # Mostrar la puntuación y el tiempo restante
        score_text = font.render(f"{score1} - {score2}", True, NEGRE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        time_text = font.render(f"{time_remaining}s", True, NEGRE)
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 100))

        # Actualizar la pantalla
        pygame.display.flip()

    pygame.quit()
    sys.exit()

    # Cargar la imagen del campo
    try:
        field_image = pygame.image.load("assets/campo.png").convert_alpha()
        field_image = pygame.transform.scale(field_image, (WIDTH, HEIGHT))  # Escalar al tamaño de la pantalla
    except FileNotFoundError:
        print("Error: No se encuentra el archivo 'campo.png' en la carpeta 'assets'.")
        pygame.quit()
        sys.exit()

    # Cargar la imagen del balón
    ball_image = pygame.image.load("assets/balon.png").convert_alpha()
    BALL_RADIUS = 20  # Tamaño del balón
    ball_image = pygame.transform.scale(ball_image, (BALL_RADIUS * 2, BALL_RADIUS * 2))  # Ajustar el tamaño de la imagen

    # Crear un rectángulo para manejar la posición y colisiones del balón
    ball = pygame.Rect(WIDTH // 2 - BALL_RADIUS, HEIGHT - BALL_RADIUS * 2, BALL_RADIUS * 2, BALL_RADIUS * 2)
    ball_vel = [4, 0]

    # Configurar las porterías
    GOAL_WIDTH, GOAL_HEIGHT = 100, 200  # Hacer las porterías más anchas
    goal1 = pygame.Rect(0, HEIGHT - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT)
    goal2 = pygame.Rect(WIDTH - GOAL_WIDTH, HEIGHT - GOAL_HEIGHT, GOAL_WIDTH, GOAL_HEIGHT)

    score1 = 0
    score2 = 0
    TOTAL_TIME = 120
    start_ticks = pygame.time.get_ticks()
    ball_reset_time = None

    def reset_ball():
        nonlocal ball_reset_time
        ball.x = WIDTH // 2 - BALL_RADIUS
        ball.y = HEIGHT - BALL_RADIUS * 2
        ball_vel[0] = 0
        ball_vel[1] = 0
        ball_reset_time = pygame.time.get_ticks() + 2000

    def activate_ball():
        ball_vel[0] = random.choice([-4, 4])
        ball_vel[1] = 0

    running = True
    while running:
        clock.tick(60)

        # Dibujar el campo como fondo
        screen.blit(field_image, (0, 0))

        # Dibujar la línea central del campo
        pygame.draw.line(screen, BLANC, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT), 5)

        # Dibujar los jugadores con sus imágenes
        screen.blit(player1_image, (player1.x, player1.y))
        screen.blit(player2_image, (player2.x, player2.y))

        # Dibujar el balón
        screen.blit(ball_image, (ball.x, ball.y))

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

        # Manejar eventos del juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Manejar controles de los jugadores
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and player1.left > 0:
            player1.x -= player_speed
        if keys[pygame.K_d] and player1.right < WIDTH:
            player1.x += player_speed
        if keys[pygame.K_w] and on_ground1:
            player1_vel[1] = jump_strength
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

        if ball.left <= 0 or ball.right >= WIDTH:
            ball_vel[0] *= -1
        if ball.top <= 0:
            ball.top = 0
            ball_vel[1] *= -1
        if ball.bottom >= HEIGHT:
            ball.bottom = HEIGHT
            ball_vel[1] *= -0.8
            if abs(ball_vel[1]) < 1:
                ball_vel[1] = 0

        if player1.colliderect(ball):
            ball_vel[0] = 4
            ball_vel[1] = -5
        if player2.colliderect(ball):
            ball_vel[0] = -4
            ball_vel[1] = -5

        # Comprobar si el balón entra en las porterías
        if ball.colliderect(goal1):
            score2 += 1
            reset_ball()
        if ball.colliderect(goal2):
            score1 += 1
            reset_ball()

        # Mostrar la puntuación y el tiempo restante
        score_text = font.render(f"{score1} - {score2}", True, NEGRE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))
        time_text = font.render(f"{time_remaining}s", True, NEGRE)
        screen.blit(time_text, (WIDTH // 2 - time_text.get_width() // 2, 100))

        # Actualizar la pantalla
        pygame.display.flip()

    pygame.quit()
    sys.exit()

# Iniciar el programa
mostrar_menu()
