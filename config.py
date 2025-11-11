import pygame

# Configuracion de pantalla
ANCHO = 800
ALTO = 600

# Colores
NARANJA = (255, 165, 0)
AMARILLO = (255, 255, 0)
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# Configuracion de juego
FPS = 60
FPS_MENU = 30

# Controles
CONTROLES_JUGADOR1 = {
    "izquierda": pygame.K_a,
    "derecha": pygame.K_d,
    "arriba": pygame.K_w,
    "abajo": pygame.K_s,
    "golpe_ligero": pygame.K_j,
    "patada": pygame.K_k,
    "cubrirse": pygame.K_l,
    "bola": pygame.K_i,
    "kamehameha": pygame.K_o,
    "movimiento_final": pygame.K_p,  
}

CONTROLES_JUGADOR2 = {
    'izquierda': pygame.K_LEFT,
    'derecha': pygame.K_RIGHT,
    'arriba': pygame.K_UP,
    'abajo': pygame.K_DOWN,
    'golpe_ligero': pygame.K_KP1,
    'patada': pygame.K_KP2,
    'cubrirse': pygame.K_KP4,
    'bola': pygame.K_KP3,
    'movimiento_final': pygame.K_KP5, 
}