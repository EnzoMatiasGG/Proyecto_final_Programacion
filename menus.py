import pygame
import sys
from config import ANCHO, ALTO, NARANJA, AMARILLO, NEGRO, FPS_MENU, BLANCO

class MenuManager:
    """Maneja todos los menus del juego"""
    
    def __init__(self, pantalla, reloj, personajes_data, mapas_data):
        self.pantalla = pantalla
        self.reloj = reloj
        self.personajes_data = personajes_data
        self.mapas_data = mapas_data
        
        # Control de volumen
        self.volumen = 0.1  
        
        # Cargar recursos
        self.fondo_start = pygame.image.load("Fondos/Fondo_start_2.png").convert()
        self.fondo_start = pygame.transform.scale(self.fondo_start, (ANCHO, ALTO))
        
        # Cargar fuente personalizada PressStart2P
        try:
            self.fuente_grande = pygame.font.Font("Fuentes/PressStart2P.ttf", 24)
            self.fuente_media = pygame.font.Font("Fuentes/PressStart2P.ttf", 18)
            self.fuente_pequena = pygame.font.Font("Fuentes/PressStart2P.ttf", 12)
        except:
            self.fuente_grande = pygame.font.SysFont(None, 24)
            self.fuente_media = pygame.font.SysFont(None, 18)
            self.fuente_pequena = pygame.font.SysFont(None, 12)
        
        # Inicializar y reproducir musca del menu
        try:
            pygame.mixer.music.load("Sonidos/Sonido_menu.wav")
            pygame.mixer.music.set_volume(self.volumen)
            pygame.mixer.music.play(-1)  # -1 = Loop infinito
        except:
            print("No se pudo cargar la musica del menu")


        self.sonido_cursor = pygame.mixer.Sound("Sonidos/Sonido_cursor.wav")

        self.opciones_menu = ["Jugar", "Personajes", "Salir"]
        self.seleccion_menu = 0
        
    def get_posiciones_menu(self):
        """Calcula las posiciones de las opciones del menu"""
        y_inicial = ALTO * 0.7
        espacio = 60
        return [(ANCHO // 2, int(y_inicial + i * espacio)) 
                for i in range(len(self.opciones_menu))]
    
    def start_menu(self):
        """Pantalla inicial del juego"""
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN: # Control de volumen
                    if evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                        self.volumen = max(0.0, self.volumen - 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS or evento.key == pygame.K_EQUALS:
                        self.volumen = min(1.0, self.volumen + 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_RETURN:
                        return
            
            self.pantalla.blit(self.fondo_start, (0, 0))
            
            # Texto parpadeante
            if (pygame.time.get_ticks() // 500) % 2 == 0:
                info = self.fuente_media.render("Presiona ENTER para comenzar", True, NARANJA)
                rect_info = info.get_rect(center=(ANCHO // 2, ALTO // 2 + 40))
                self.pantalla.blit(info, rect_info)
            
            pygame.display.flip()
            self.reloj.tick(FPS_MENU)
    
    def dibujar_menu_principal(self):
        """Dibuja el menu principal"""
        self.pantalla.blit(self.fondo_start, (0, 0))
        
        # Overlay oscuro
        overlay = pygame.Surface((ANCHO, ALTO))
        overlay.fill((0, 0, 0))
        overlay.set_alpha(120)
        self.pantalla.blit(overlay, (0, 0))
        
        # Opciones del menu
        posiciones = self.get_posiciones_menu()
        for i, opcion in enumerate(self.opciones_menu):
            color = AMARILLO if i == self.seleccion_menu else NARANJA
            texto = self.fuente_grande.render(opcion, True, color)
            rect_texto = texto.get_rect(center=posiciones[i])
            self.pantalla.blit(texto, rect_texto)
        
        pygame.display.flip()
    
    def menu_principal(self):
        """Loop del menu principal"""
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    # Control de volumen
                    if evento.key == pygame.K_MINUS or evento.key == pygame.    K_KP_MINUS:
                        self.volumen = max(0.0, self.volumen - 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif (evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS or evento.key == pygame.K_EQUALS):
                        self.volumen = min(1.0, self.volumen + 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_UP:
                        self.seleccion_menu = (self.seleccion_menu - 1) % len(self.opciones_menu)
                        self.sonido_cursor.play()
                    elif evento.key == pygame.K_DOWN:
                        self.seleccion_menu = (self.seleccion_menu + 1) % len(self.opciones_menu)
                        self.sonido_cursor.play()
                    elif evento.key == pygame.K_RETURN:
                        return self.opciones_menu[self.seleccion_menu]

            self.dibujar_menu_principal()
            self.reloj.tick(FPS_MENU)

    
    def menu_seleccion_personaje(self, jugador_num=1):
        """Menu de seleccion de personaje para un jugador"""
        seleccion = 0
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    # Control de volumen
                    if evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                        self.volumen = max(0.0, self.volumen - 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS or       evento.key == pygame.K_EQUALS:
                        self.volumen = min(1.0, self.volumen + 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_LEFT:
                        seleccion = (seleccion - 1) % len(self.personajes_data)
                        self.sonido_cursor.play()
                    elif evento.key == pygame.K_RIGHT:
                        seleccion = (seleccion + 1) % len(self.personajes_data)
                        self.sonido_cursor.play()
                    elif evento.key == pygame.K_RETURN:
                        return self.personajes_data[seleccion]["id"]
                    elif evento.key == pygame.K_ESCAPE:
                        return None 

            
            # Fondo
            self.pantalla.fill((10, 10, 30))
            
            # Titulo
            if jugador_num == 2:
                titulo = self.fuente_grande.render("Elige tu rival", True, AMARILLO)
            else:
                titulo = self.fuente_grande.render(f"JUGADOR {jugador_num} - Elige tu personaje", True, AMARILLO)
            self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))
            
            # Mostrar personajes en grid
            cols = 4
            espacio_x = ANCHO // (cols + 1)
            espacio_y = 150
            inicio_y = 150
            
            for i, pj in enumerate(self.personajes_data):
                col = i % cols
                fila = i // cols
                x = espacio_x * (col + 1) - 60
                y = inicio_y + fila * espacio_y
                
                # Cargar y mostrar imagen
                try:
                    imagen = pygame.image.load(pj["foto_seleccion"]).convert()
                    imagen.set_colorkey((255, 255, 255))
                    imagen = pygame.transform.scale(imagen, (120, 120))
                    
                    # Resaltar seleccionado
                    if i == seleccion:
                        pygame.draw.rect(self.pantalla, AMARILLO, (x-5, y-5, 130, 130), 3)
                    
                    self.pantalla.blit(imagen, (x, y))
                    
                    # Nombre
                    color_texto = AMARILLO if i == seleccion else BLANCO
                    nombre = self.fuente_media.render(pj["nombre"], True, color_texto)
                    self.pantalla.blit(nombre, (x + 60 - nombre.get_width() // 2, y + 130))
                except:
                    pass
            
            # Instrucciones
            instrucciones = self.fuente_pequena.render("← → para navegar | ENTER para elegir | ESC para volver", True, NARANJA)
            self.pantalla.blit(instrucciones, (ANCHO // 2 - instrucciones.get_width() // 2, ALTO - 40))
            
            pygame.display.flip()
            self.reloj.tick(FPS_MENU)
    
    def menu_seleccion_mapa(self):
        """Menu de seleccion de escenario"""
        seleccion = 0
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:# Control de volumen
                    if evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                        self.volumen = max(0.0, self.volumen - 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS or evento.key == pygame.K_EQUALS:
                        self.volumen = min(1.0, self.volumen + 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_LEFT:
                        seleccion = (seleccion - 1) % len(self.mapas_data)
                    elif evento.key == pygame.K_RIGHT:
                        seleccion = (seleccion + 1) % len(self.mapas_data)
                    elif evento.key == pygame.K_RETURN:
                        return self.mapas_data[seleccion]["ruta"]
                    elif evento.key == pygame.K_ESCAPE:
                        return None
            
            # Fondo
            self.pantalla.fill((10, 10, 30))
            
            # Titulo
            titulo = self.fuente_grande.render("Elige el escenario", True, AMARILLO)
            self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))
            
            # Mostrar mapas
            cols = 3
            espacio_x = ANCHO // (cols + 1)
            espacio_y = 180
            inicio_y = 150
            
            for i, mapa in enumerate(self.mapas_data):
                col = i % cols
                fila = i // cols
                x = espacio_x * (col + 1) - 80
                y = inicio_y + fila * espacio_y
                
                # Cargar y mostrar preview
                try:
                    preview = pygame.image.load(mapa["ruta"]).convert()
                    preview = pygame.transform.scale(preview, (160, 120))
                    
                    # Resaltar seleccionado
                    if i == seleccion:
                        pygame.draw.rect(self.pantalla, AMARILLO, (x-5, y-5, 170, 130), 3)
                    
                    self.pantalla.blit(preview, (x, y))
                    
                    # Nombre
                    color_texto = AMARILLO if i == seleccion else BLANCO
                    nombre = self.fuente_pequena.render(mapa["nombre"], True, color_texto)
                    self.pantalla.blit(nombre, (x + 80 - nombre.get_width() // 2, y + 135))
                except:
                    # Cuadro de color si no se encuentra la imagen
                    pygame.draw.rect(self.pantalla, (50, 50, 50), (x, y, 160, 120))
                    nombre = self.fuente_pequena.render(mapa["nombre"], True, BLANCO)
                    self.pantalla.blit(nombre, (x + 80 - nombre.get_width() // 2, y + 60))
            
            # Instrucciones
            instrucciones = self.fuente_pequena.render("← → para navegar | ENTER para elegir | ESC para volver", True, NARANJA)
            self.pantalla.blit(instrucciones, (ANCHO // 2 - instrucciones.get_width() // 2, ALTO - 40))
            
            pygame.display.flip()
            self.reloj.tick(FPS_MENU)
    
    def menu_personajes(self):
        """Menu de informacion de personajes"""
        seleccion = 0
        fondo_nubes = pygame.image.load("Fondos/Fondo_nubes.png").convert()
        fondo_nubes = pygame.transform.scale(fondo_nubes, (ANCHO, ALTO))
        logo_imagen = pygame.image.load("Assets/imagenes_especiales/Logo_info.png").convert_alpha()
        logo_rect = logo_imagen.get_rect(center=(ANCHO // 2, 80))  # Centrado arriba
        boton_rect = pygame.Rect(ANCHO // 2 - 95, ALTO - 80, 190, 40)

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    # Control de volumen
                    if evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                        self.volumen = max(0.0, self.volumen - 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS or evento.key == pygame.K_EQUALS:
                        self.volumen = min(1.0, self.volumen + 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(self.personajes_data)
                    elif evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(self.personajes_data)
                    elif evento.key == pygame.K_RETURN:
                        self.mostrar_lore_personaje(seleccion)
                    elif evento.key == pygame.K_ESCAPE:
                        return
                    
            self.pantalla.blit(fondo_nubes , (0, 0))
            self.pantalla.blit(logo_imagen, logo_rect)
            
            for i, pj in enumerate(self.personajes_data):
                color = AMARILLO if i == seleccion else NARANJA
                texto = self.fuente_grande.render(pj["nombre"], True, color)
                rect_texto = texto.get_rect(center=(ANCHO // 2, 200 + i * 60))
                self.pantalla.blit(texto, rect_texto)
            
            pygame.draw.rect(self.pantalla, NARANJA, boton_rect)
            texto_boton = self.fuente_pequena.render("ESC para volver", True, NEGRO)
            rect_texto_boton = texto_boton.get_rect(center=boton_rect.center)
            self.pantalla.blit(texto_boton, rect_texto_boton)

            pygame.display.flip()
            self.reloj.tick(FPS_MENU)
    
    def mostrar_lore_personaje(self, indice):
        """Muestra informacion detallada de un personaje"""
        pj = self.personajes_data[indice]
        
        imagen = pygame.image.load(pj["foto_seleccion"]).convert()
        imagen.set_colorkey((255, 255, 255))
        imagen = pygame.transform.scale(imagen, (120, 120))
        
        meme_img = pygame.image.load("Assets/Imagenes_especiales/Meme.jpg").convert()
        meme_img = pygame.transform.scale(meme_img, (120, 120))
        
        boton_rect = pygame.Rect(ANCHO - 150 - 30, ALTO - 50 - 30, 150, 50)

        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:# Control de volumen
                    if evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                        self.volumen = max(0.0, self.volumen - 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS or evento.key == pygame.K_EQUALS:
                        self.volumen = min(1.0, self.volumen + 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key in (pygame.K_RETURN, pygame.K_ESCAPE):
                        return
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_rect.collidepoint(evento.pos):
                        return
            
            self.pantalla.fill((20, 20, 30))
            self.pantalla.blit(imagen, (ANCHO // 2 - 60, 50))
            
            nombre = self.fuente_grande.render(pj["nombre"], True, AMARILLO)
            self.pantalla.blit(nombre, (ANCHO // 2 - nombre.get_width() // 2, 180))
            
            # Lore 
            lore_texto = pj.get("lore", "")
            lore_lines = []
            max_lore_len = 46
            while lore_texto:
                lore_lines.append(lore_texto[:max_lore_len])
                lore_texto = lore_texto[max_lore_len:]
            
            y_lore = 230
            for i, linea in enumerate(lore_lines):
                lore_render = self.fuente_pequena.render(linea, True, BLANCO)
                self.pantalla.blit(lore_render, (ANCHO // 2 - lore_render.get_width() // 2, y_lore + i * 28))
            
            meme_x = (ANCHO // 2) - (meme_img.get_width() // 2)
            meme_y = ALTO - meme_img.get_height() - 90
            self.pantalla.blit(meme_img, (meme_x, meme_y))

            pygame.draw.rect(self.pantalla, AMARILLO, boton_rect)
            boton_texto = self.fuente_grande.render("Volver", True, NEGRO)
            rect_boton = boton_texto.get_rect(center=boton_rect.center)
            self.pantalla.blit(boton_texto, rect_boton)
            
            pygame.display.flip()
            self.reloj.tick(FPS_MENU)