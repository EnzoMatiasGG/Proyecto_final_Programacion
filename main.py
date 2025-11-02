import pygame
import sys
from sprites import cargar_sprites

pygame.init()

ANCHO, ALTO = 800, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

NARANJA = (255, 165, 0)
AMARILLO = (255, 255, 0)
NEGRO = (0, 0, 0)

fuente = pygame.font.SysFont(None, 48)
opciones_menu = ["Jugar", "Personajes", "Salir"]

def obtener_posiciones_menu():
    y_inicial = ALTO * 0.7
    espacio = 60
    return [(ANCHO // 2, int(y_inicial + i * espacio)) for i in range(len(opciones_menu))]

posiciones_menu = obtener_posiciones_menu()
seleccion_menu = 0

sprites_goku, sprites_freezer, sprites_gohan, sprites_cell, personajes_data = cargar_sprites()

def dibujar_menu():
    pantalla.fill(NEGRO)
    for i, opcion in enumerate(opciones_menu):
        color = AMARILLO if i == seleccion_menu else NARANJA
        texto = fuente.render(opcion, True, color)
        rect_texto = texto.get_rect(center=posiciones_menu[i])
        pantalla.blit(texto, rect_texto)
    pygame.display.flip()

def start_menu():
    fuente_titulo = pygame.font.SysFont(None, 80)
    fuente_info = pygame.font.SysFont(None, 36)
    titulo = fuente_titulo.render("DRAGON FIGHTERS", True, AMARILLO)
    info = fuente_info.render("Presiona ENTER para comenzar", True, NARANJA)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    return
        pantalla.fill((20, 20, 30))
        rect_titulo = titulo.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
        rect_info = info.get_rect(center=(ANCHO // 2, ALTO // 2 + 40))
        pantalla.blit(titulo, rect_titulo)
        pantalla.blit(info, rect_info)
        pygame.display.flip()
        reloj.tick(30)

def menu_personajes():
    seleccion = 0
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion = (seleccion - 1) % len(personajes_data)
                elif evento.key == pygame.K_DOWN:
                    seleccion = (seleccion + 1) % len(personajes_data)
                elif evento.key == pygame.K_RETURN:
                    mostrar_lore_personaje(seleccion)
                elif evento.key == pygame.K_ESCAPE:
                    return
        pantalla.fill((10, 10, 30))
        for i, pj in enumerate(personajes_data):
            color = AMARILLO if i == seleccion else NARANJA
            texto = fuente.render(pj["nombre"], True, color)
            rect_texto = texto.get_rect(center=(ANCHO // 2, int(ALTO * 0.65 + i * 60)))
            pantalla.blit(texto, rect_texto)
        pygame.display.flip()
        reloj.tick(30)

def mostrar_lore_personaje(indice):
    pj = personajes_data[indice]
    imagen = pygame.image.load(pj["foto_seleccion"]).convert()
    imagen.set_colorkey((255, 255, 255))
    imagen = imagen.convert_alpha()
    imagen = pygame.transform.scale(imagen, (120, 120))
    volver = False
    boton_ancho = 150
    boton_alto = 50
    margen = 30
    boton_rect = pygame.Rect(ANCHO - boton_ancho - margen, ALTO - boton_alto - margen, boton_ancho, boton_alto)

    while not volver:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                    volver = True
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(evento.pos):
                    volver = True
        pantalla.fill((20, 20, 30))
        pantalla.blit(imagen, (ANCHO // 2 - 200, ALTO // 2 - 60))
        parrafo = render_multiline(pj["lore"], fuente, 300)
        for i, linea in enumerate(parrafo):
            pantalla.blit(linea, (ANCHO // 2 - 40, ALTO // 2 - 40 + 28 * i))
        nombre = fuente.render(pj["nombre"], True, AMARILLO)
        pantalla.blit(nombre, (ANCHO // 2 - 40, ALTO // 2 - 80))
        pygame.draw.rect(pantalla, AMARILLO, boton_rect)
        texto_boton = fuente.render("Volver", True, NEGRO)
        rect_texto = texto_boton.get_rect(center=boton_rect.center)
        pantalla.blit(texto_boton, rect_texto)
        pygame.display.flip()
        reloj.tick(30)

def render_multiline(texto, font, width):
    palabras = texto.split(" ")
    lineas = []
    linea_actual = ""
    for palabra in palabras:
        test_line = linea_actual + palabra + " "
        if font.size(test_line)[0] < width:
            linea_actual = test_line
        else:
            lineas.append(font.render(linea_actual, True, (255, 255, 255)))
            linea_actual = palabra + " "
    if linea_actual:
        lineas.append(font.render(linea_actual, True, (255, 255, 255)))
    return lineas

class Peleador:
    def __init__(self, x, y, controles, sprites_personaje):
        self.x = x
        self.y = y
        self.controles = controles
        self.sprites = sprites_personaje
        self.velocidad = 5
        self.estado = 'inicio'
        self.sprite = self.sprites[self.estado]
        self.mirando_derecha = True
        self.rect = pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())

    def mover(self, teclas, otro_jugador):
        mov_x, mov_y = 0, 0
        estado_horizontal = None
        if teclas[self.controles['izquierda']] and teclas[self.controles['arriba']]:
            mov_x = -self.velocidad
            mov_y = -self.velocidad
            estado_horizontal = 'izquierda'
        elif teclas[self.controles['derecha']] and teclas[self.controles['arriba']]:
            mov_x = self.velocidad
            mov_y = -self.velocidad
            estado_horizontal = 'derecha'
        elif teclas[self.controles['izquierda']] and teclas[self.controles['abajo']]:
            mov_x = -self.velocidad
            mov_y = self.velocidad
            estado_horizontal = 'izquierda'
        elif teclas[self.controles['derecha']] and teclas[self.controles['abajo']]:
            mov_x = self.velocidad
            mov_y = self.velocidad
            estado_horizontal = 'derecha'
        elif teclas[self.controles['izquierda']]:
            mov_x = -self.velocidad
            estado_horizontal = 'izquierda'
        elif teclas[self.controles['derecha']]:
            mov_x = self.velocidad
            estado_horizontal = 'derecha'
        elif teclas[self.controles['arriba']]:
            mov_y = -self.velocidad
        elif teclas[self.controles['abajo']]:
            mov_y = self.velocidad
        nuevo_x = self.x + mov_x
        nuevo_y = self.y + mov_y
        ancho_sprite = self.sprite.get_width()
        alto_sprite = self.sprite.get_height()
        rect_provisional = pygame.Rect(nuevo_x, nuevo_y, ancho_sprite, alto_sprite)
        superposicion_permitida = 5
        if rect_provisional.colliderect(otro_jugador.rect):
            if self.x < otro_jugador.x:
                max_x = otro_jugador.x - ancho_sprite + superposicion_permitida
                if nuevo_x > max_x:
                    nuevo_x = max_x
            else:
                min_x = otro_jugador.x + otro_jugador.rect.width - superposicion_permitida
                if nuevo_x < min_x:
                    nuevo_x = min_x
        if nuevo_x < 0:
            nuevo_x = 0
        elif nuevo_x > ANCHO - ancho_sprite:
            nuevo_x = ANCHO - ancho_sprite
        if nuevo_y < 0:
            nuevo_y = 0
        elif nuevo_y > ALTO - alto_sprite:
            nuevo_y = ALTO - alto_sprite
        self.x = nuevo_x
        self.y = nuevo_y
        self.rect.topleft = (self.x, self.y)
        if estado_horizontal is not None:
            self.estado = estado_horizontal
        else:
            if mov_y != 0:
                self.estado = 'bajar'
            else:
                self.estado = 'inicio'
        self.sprite = self.sprites[self.estado]

    def actualizar_direccion(self, otro_jugador):
        self.mirando_derecha = self.x < otro_jugador.x

    def dibujar(self, pantalla):
        if self.mirando_derecha:
            if self.estado == 'izquierda':
                imagen = self.sprites['izquierda']
            elif self.estado == 'derecha':
                imagen = self.sprites['derecha']
            elif self.estado == 'bajar':
                imagen = self.sprites['bajar']
            else:
                imagen = self.sprites['inicio']
        else:
            if self.estado == 'izquierda':
                imagen = pygame.transform.flip(self.sprites['derecha'], True, False)
            elif self.estado == 'derecha':
                imagen = pygame.transform.flip(self.sprites['izquierda'], True, False)
            elif self.estado == 'bajar':
                imagen = pygame.transform.flip(self.sprites['bajar'], True, False)
            else:
                imagen = pygame.transform.flip(self.sprites['inicio'], True, False)
        pantalla.blit(imagen, (self.x, self.y))

def main():
    controles_jugador1 = {'izquierda': pygame.K_a, 'derecha': pygame.K_d, 'arriba': pygame.K_w, 'abajo': pygame.K_s}
    controles_jugador2 = {'izquierda': pygame.K_LEFT, 'derecha': pygame.K_RIGHT, 'arriba': pygame.K_UP, 'abajo': pygame.K_DOWN}
    jugador1 = Peleador(100, ALTO - 150 - 80, controles_jugador1, sprites_goku)
    jugador2 = Peleador(600, ALTO - 150 - 80, controles_jugador2, sprites_freezer)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        teclas = pygame.key.get_pressed()
        jugador1.mover(teclas, jugador2)
        jugador2.mover(teclas, jugador1)
        jugador1.actualizar_direccion(jugador2)
        jugador2.actualizar_direccion(jugador1)
        pantalla.fill((0, 0, 0))
        pygame.draw.line(pantalla, (255, 0, 0), (ANCHO // 2, 0), (ANCHO // 2, ALTO), 3)
        jugador1.dibujar(pantalla)
        jugador2.dibujar(pantalla)
        pygame.display.flip()
        reloj.tick(60)

def main_menu():
    global seleccion_menu
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    seleccion_menu = (seleccion_menu - 1) % len(opciones_menu)
                elif evento.key == pygame.K_DOWN:
                    seleccion_menu = (seleccion_menu + 1) % len(opciones_menu)
                elif evento.key == pygame.K_RETURN:
                    if opciones_menu[seleccion_menu] == "Salir":
                        pygame.quit()
                        sys.exit()
                    elif opciones_menu[seleccion_menu] == "Jugar":
                        main()
                    elif opciones_menu[seleccion_menu] == "Personajes":
                        menu_personajes()
        dibujar_menu()
        reloj.tick(30)

if __name__ == "__main__":
    start_menu()
    main_menu()
