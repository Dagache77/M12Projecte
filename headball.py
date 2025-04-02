import pygame
import random

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
ANCHO, ALTO = 800, 400
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Headball 1 vs 1")

# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
COLOR_PORTERIA = (100, 100, 100)

# Configuración del tiempo y FPS
FPS = 60
TIEMPO_TOTAL = 120000  # Duración en milisegundos (2 minutos)

# Clase para los jugadores
class Jugador:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.velocidad_y = 0
        self.en_suelo = True
        self.goles = 0

    def mover(self, dx):
        self.rect.x += dx * 7  # Velocidad incrementada
        self.rect.x = max(0, min(ANCHO - self.rect.width, self.rect.x))

    def saltar(self):
        if self.en_suelo:
            self.velocidad_y = -15
            self.en_suelo = False

    def actualizar(self):
        self.velocidad_y += 1  # Gravedad
        self.rect.y += self.velocidad_y
        if self.rect.y >= ALTO - self.rect.height:
            self.rect.y = ALTO - self.rect.height
            self.en_suelo = True
            self.velocidad_y = 0

    def dibujar(self, ventana):
        pygame.draw.rect(ventana, self.color, self.rect)

# Clase para la pelota
class Pelota:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.velocidad_x = random.choice([-4, 4])  # Velocidad reducida
        self.velocidad_y = 0

    def actualizar(self):
        self.velocidad_y += 1  # Gravedad
        self.rect.x += self.velocidad_x
        self.rect.y += self.velocidad_y

        # Rebote en el suelo
        if self.rect.y >= ALTO - self.rect.height:
            self.rect.y = ALTO - self.rect.height
            self.velocidad_y = -self.velocidad_y * 0.7
            self.velocidad_x *= 0.9

        # Rebote en paredes
        if self.rect.x <= 0 or self.rect.x >= ANCHO - self.rect.width:
            self.velocidad_x = -self.velocidad_x

    def colisionar_con_jugador(self, jugador):
        if self.rect.colliderect(jugador.rect):
            self.velocidad_x = 5 if self.rect.centerx > jugador.rect.centerx else -5
            self.velocidad_y = -10

    def reiniciar(self):
        self.rect.x, self.rect.y = ANCHO // 2 - 15, ALTO // 2 - 15
        self.velocidad_x = random.choice([-4, 4])
        self.velocidad_y = 0

    def dibujar(self, ventana):
        pygame.draw.ellipse(ventana, NEGRO, self.rect)

# Función para mostrar marcador
def mostrar_marcador(ventana, jugador1, jugador2, tiempo_restante):
    fuente = pygame.font.Font(None, 36)
    marcador = fuente.render(f"Jugador 1: {jugador1.goles}  Jugador 2: {jugador2.goles}", True, NEGRO)
    tiempo = fuente.render(f"Tiempo restante: {tiempo_restante}s", True, NEGRO)
    ventana.blit(marcador, (ANCHO // 2 - marcador.get_width() // 2, 10))
    ventana.blit(tiempo, (10, 10))

# Configuración inicial
reloj = pygame.time.Clock()
tiempo_inicio = pygame.time.get_ticks()

jugador1 = Jugador(50, ALTO - 75, AZUL)
jugador2 = Jugador(ANCHO - 100, ALTO - 75, ROJO)
pelota = Pelota(ANCHO // 2 - 15, ALTO // 2 - 15)

porteria1 = pygame.Rect(-20, ALTO - 140, 30, 150)
porteria2 = pygame.Rect(ANCHO - 10, ALTO - 140, 30, 150)

# Bucle principal
corriendo = True
while corriendo:
    ventana.fill(BLANCO)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            corriendo = False

    # Controles
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_a]:
        jugador1.mover(-1)
    if teclas[pygame.K_d]:
        jugador1.mover(1)
    if teclas[pygame.K_w]:
        jugador1.saltar()

    if teclas[pygame.K_LEFT]:
        jugador2.mover(-1)
    if teclas[pygame.K_RIGHT]:
        jugador2.mover(1)
    if teclas[pygame.K_UP]:
        jugador2.saltar()

    # Actualizar estado
    jugador1.actualizar()
    jugador2.actualizar()
    pelota.actualizar()
    pelota.colisionar_con_jugador(jugador1)
    pelota.colisionar_con_jugador(jugador2)

    # Detectar goles
    if pelota.rect.colliderect(porteria1):
        jugador2.goles += 1
        pelota.reiniciar()
    elif pelota.rect.colliderect(porteria2):
        jugador1.goles += 1
        pelota.reiniciar()

    # Dibujar elementos
    jugador1.dibujar(ventana)
    jugador2.dibujar(ventana)
    pelota.dibujar(ventana)
    pygame.draw.rect(ventana, COLOR_PORTERIA, porteria1)
    pygame.draw.rect(ventana, COLOR_PORTERIA, porteria2)

    # Mostrar marcador y tiempo
    tiempo_actual = pygame.time.get_ticks()
    tiempo_restante = max(0, (TIEMPO_TOTAL - (tiempo_actual - tiempo_inicio)) // 1000)
    mostrar_marcador(ventana, jugador1, jugador2, tiempo_restante)

    if tiempo_restante == 0:
        corriendo = False

    pygame.display.flip()
    reloj.tick(FPS)

# Pantalla final
ventana.fill(BLANCO)
fuente = pygame.font.Font(None, 74)
ganador = "Jugador 1" if jugador1.goles > jugador2.goles else "Jugador 2" if jugador2.goles > jugador1.goles else "Empate"
texto_final = fuente.render(f"Ganador: {ganador}", True, NEGRO)
ventana.blit(texto_final, (ANCHO // 2 - texto_final.get_width() // 2, ALTO // 2 - texto_final.get_height() // 2))
pygame.display.flip()
pygame.time.wait(5000)

pygame.quit()
