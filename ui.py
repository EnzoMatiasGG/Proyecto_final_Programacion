import pygame
from config import ANCHO, ALTO, AMARILLO, BLANCO, NEGRO, ROJO, NARANJA

class UI:
    """Maneja toda la interfaz de usuario del juego"""
    
    def __init__(self, pantalla):
        self.pantalla = pantalla
        
        # Fuentes
        self.fuente_ui = pygame.font.SysFont(None, 24)
        self.fuente_ui_pequena = pygame.font.SysFont(None, 18)
        
        # Cargar fuente personalizada PressStart2P
        try:
            self.fuente_press_start = pygame.font.Font("Fuentes/PressStart2P.ttf", 12)
            self.fuente_press_start_mediana = pygame.font.Font("Fuentes/PressStart2P.ttf", 16)
            self.fuente_press_start_grande = pygame.font.Font("Fuentes/PressStart2P.ttf", 24)
        except:
            self.fuente_press_start = pygame.font.SysFont(None, 18)
            self.fuente_press_start_mediana = pygame.font.SysFont(None, 24)
            self.fuente_press_start_grande = pygame.font.SysFont(None, 36)
        
        # Cargar icono de Z para los rounds
        try:
            self.icono_z = pygame.image.load("Assets/Imagenes_especiales/Z-logo.png").convert_alpha()
            self.icono_z = pygame.transform.scale(self.icono_z, (30, 30))
        except:
            self.icono_z = None
    
    def dibujar_barra(self, x, y, ancho, alto, valor_actual, valor_maximo, color_fondo, color_barra):
        """Dibuja una barra con texto dentro"""
        pygame.draw.rect(self.pantalla, BLANCO, (x-2, y-2, ancho+4, alto+4), 2)
        pygame.draw.rect(self.pantalla, color_fondo, (x, y, ancho, alto))
        
        porcentaje = max(0, valor_actual / valor_maximo)
        ancho_barra_relleno = int(ancho * porcentaje)
        pygame.draw.rect(self.pantalla, color_barra, (x, y, ancho_barra_relleno, alto))
        
        # Solo mostrar texto si la barra es lo suficientemente grande
        if alto >= 18:
            texto_valor = self.fuente_ui_pequena.render(f"{int(valor_actual)}/{valor_maximo}", True, BLANCO)
            texto_x = x + (ancho - texto_valor.get_width()) // 2
            texto_y = y + (alto - texto_valor.get_height()) // 2
            self.pantalla.blit(texto_valor, (texto_x, texto_y))
    
    def dibujar_barras_jugadores(self, jugador1, jugador2, rounds_j1, rounds_j2):
        """Dibuja las barras de vida y stamina de ambos jugadores"""
        margen = 20
        
        # Calcular ancho de barras para que lleguen hasta el timer
        ancho_timer = 100
        espacio_timer = 10
        ancho_barra = (ANCHO // 2) - margen - (ancho_timer // 2) - espacio_timer
        
        alto_barra_vida = 20
        alto_barra_stamina = 15
        espacio = 25
        
        # JUGADOR 1 (izquierda)
        x_j1 = margen
        y_j1 = margen
        
        texto_nombre = self.fuente_press_start.render("JUGADOR 1", True, AMARILLO)
        self.pantalla.blit(texto_nombre, (x_j1, y_j1))
        
        # Barras
        self.dibujar_barra(x_j1, y_j1 + 25, ancho_barra, alto_barra_vida, 
                          jugador1.vida_actual, jugador1.vida_maxima, (60, 0, 0), (0, 255, 0))
        self.dibujar_barra(x_j1, y_j1 + 25 + espacio, ancho_barra, alto_barra_stamina, 
                          jugador1.stamina_actual, jugador1.stamina_maxima, (0, 40, 60), (0, 200, 255))
        
        # Iconos de rounds ganados
        if self.icono_z:
            y_iconos = y_j1 + 25 + espacio + alto_barra_stamina + 10
            for i in range(rounds_j1):
                self.pantalla.blit(self.icono_z, (x_j1 + i * 35, y_iconos))
        
        # JUGADOR 2 (derecha)
        x_j2 = ANCHO - margen - ancho_barra
        y_j2 = margen
        
        texto_nombre2 = self.fuente_press_start.render("JUGADOR 2", True, AMARILLO)
        texto_rect = texto_nombre2.get_rect(topright=(ANCHO - margen, y_j2))
        self.pantalla.blit(texto_nombre2, texto_rect)
        
        # Barras
        self.dibujar_barra(x_j2, y_j2 + 25, ancho_barra, alto_barra_vida, 
                          jugador2.vida_actual, jugador2.vida_maxima, (60, 0, 0), (0, 255, 0))
        self.dibujar_barra(x_j2, y_j2 + 25 + espacio, ancho_barra, alto_barra_stamina, 
                          jugador2.stamina_actual, jugador2.stamina_maxima, (0, 40, 60), (0, 200, 255))
        
        # Iconos de rounds ganados
        if self.icono_z:
            y_iconos = y_j2 + 25 + espacio + alto_barra_stamina + 10
            for i in range(rounds_j2):
                self.pantalla.blit(self.icono_z, (ANCHO - margen - (i + 1) * 35, y_iconos))
    
    def dibujar_timer(self, tiempo_restante, en_introduccion=False):
        """Dibuja el timer del combate en el centro superior"""
        ancho_timer = 100
        alto_timer = 50
        x_centro = ANCHO // 2
        y_centro = 35
        
        rect_fondo = pygame.Rect(x_centro - ancho_timer // 2, y_centro - alto_timer // 2, 
                                 ancho_timer, alto_timer)
        pygame.draw.rect(self.pantalla, (20, 20, 40), rect_fondo)
        
        if not en_introduccion:
            # Colores segun tiempo restante
            if tiempo_restante <= 10:
                color_borde = ROJO
                color_numero = ROJO
                grosor_borde = 4
            elif tiempo_restante <= 30:
                color_borde = NARANJA
                color_numero = NARANJA
                grosor_borde = 3
            else:
                color_borde = AMARILLO
                color_numero = AMARILLO
                grosor_borde = 3
            
            pygame.draw.rect(self.pantalla, color_borde, rect_fondo, grosor_borde)
            
            # Numero del timer
            texto_tiempo = self.fuente_press_start_grande.render(str(tiempo_restante), True, color_numero)
            rect_tiempo = texto_tiempo.get_rect(center=(x_centro, y_centro))
            
            # Sombra
            sombra = self.fuente_press_start_grande.render(str(tiempo_restante), True, NEGRO)
            sombra_rect = sombra.get_rect(center=(x_centro + 2, y_centro + 2))
            self.pantalla.blit(sombra, sombra_rect)
            self.pantalla.blit(texto_tiempo, rect_tiempo)
            
            # Texto "TIME" abajo
            texto_time = self.fuente_press_start.render("TIME", True, AMARILLO)
            rect_time = texto_time.get_rect(center=(x_centro, y_centro + alto_timer // 2 + 12))
            self.pantalla.blit(texto_time, rect_time)
        else:
            # Durante la introduccion, mostrar "KO"
            pygame.draw.rect(self.pantalla, NARANJA, rect_fondo, 3)
            texto_ko = self.fuente_press_start_grande.render("KO", True, NARANJA)
            rect_ko = texto_ko.get_rect(center=(x_centro, y_centro))
            self.pantalla.blit(texto_ko, rect_ko)