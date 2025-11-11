import pygame
import sys
from config import ANCHO, ALTO, AMARILLO, NEGRO, BLANCO, NARANJA, ROJO, FPS

class RoundsManager:
    """Maneja el sistema de rounds y pantallas finales"""
    
    def __init__(self, pantalla, reloj, ui):
        self.pantalla = pantalla
        self.reloj = reloj
        self.ui = ui
        
        self.rounds_jugador1 = 0
        self.rounds_jugador2 = 0
        self.max_rounds = 2  # Primero en ganar 2
        self.round_actual = 1
        self.en_cuenta_regresiva = False
        self.tiempo_cuenta_regresiva = 0
        self.pelea_terminada = False
        
        # Control de animacion KO
        self.mostrando_ko = False
        self.tiempo_inicio_ko = 0
        self.duracion_ko = 2000  # 2 segundos para mostrar la animacion KO
        
        # Estadisticas
        self.stats_jugador1 = {
            'golpes_totales': 0,
            'dano_causado': 0,
            'dano_recibido': 0
        }
        self.stats_jugador2 = {
            'golpes_totales': 0,
            'dano_causado': 0,
            'dano_recibido': 0
        }
        self.tiempo_inicio_pelea_total = 0
        
        # Fuente grande para textos de round
        self.fuente_grande = pygame.font.SysFont(None, 100)
    
    def reiniciar(self):
        """Reinicia el sistema de rounds"""
        self.rounds_jugador1 = 0
        self.rounds_jugador2 = 0
        self.round_actual = 1
        self.pelea_terminada = False
        self.mostrando_ko = False
        self.stats_jugador1 = {'golpes_totales': 0, 'dano_causado': 0, 'dano_recibido': 0}
        self.stats_jugador2 = {'golpes_totales': 0, 'dano_causado': 0, 'dano_recibido': 0}
        self.tiempo_inicio_pelea_total = pygame.time.get_ticks()
    
    def terminar_round(self, ganador):
        """Termina el round actual y actualiza el marcador"""
        if ganador == 1:
            self.rounds_jugador1 += 1
        elif ganador == 2:
            self.rounds_jugador2 += 1
        
        # Iniciar animacion de KO
        self.mostrando_ko = True
        self.tiempo_inicio_ko = pygame.time.get_ticks()
        
        # Verificar si alguien gano el mejor de 3
        if self.rounds_jugador1 >= self.max_rounds or self.rounds_jugador2 >= self.max_rounds:
            self.pelea_terminada = True
    
    def iniciar_cuenta_regresiva(self):
        """Inicia la cuenta regresiva entre rounds"""
        self.en_cuenta_regresiva = True
        self.tiempo_cuenta_regresiva = pygame.time.get_ticks()
        self.round_actual += 1
    
    def reiniciar_jugadores(self, jugador1, jugador2):
        """Reinicia los jugadores para un nuevo round"""
        from config import ALTO
        
        # Resetear estados de KO
        jugador1.resetear_ko()
        jugador2.resetear_ko()
        
        # Reiniciar vida y stamina
        jugador1.vida_actual = jugador1.vida_maxima
        jugador1.stamina_actual = jugador1.stamina_maxima
        jugador2.vida_actual = jugador2.vida_maxima
        jugador2.stamina_actual = jugador2.stamina_maxima
        
        # Reiniciar posiciones
        jugador1.x = 100
        jugador1.y = ALTO - 150 - 80
        jugador2.x = ANCHO - 200
        jugador2.y = ALTO - 150 - 80
        
        # Limpiar proyectiles
        jugador1.bolas_activas = []
        jugador2.bolas_activas = []
        jugador1.kamehameha_activo = None
        jugador2.kamehameha_activo = None
    
    def mostrar_animacion_ko(self, fondo, jugador1, jugador2):
        """Muestra la animación de KO antes de continuar al siguiente round"""
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio_ko
        
        if fondo:
            self.pantalla.blit(fondo, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        # Actualizar y dibujar personajes 
        jugador1.actualizar()
        jugador2.actualizar()
        jugador1.dibujar(self.pantalla)
        jugador2.dibujar(self.pantalla)
        
        # Dibujar UI
        self.ui.dibujar_barras_jugadores(jugador1, jugador2, self.rounds_jugador1, self.rounds_jugador2)
        self.ui.dibujar_timer(0, en_introduccion=True)
        
        # Mostrar texto "K.O."
        texto_ko = self.fuente_grande.render("K.O.", True, ROJO)
        texto_rect = texto_ko.get_rect(center=(ANCHO // 2, ALTO // 2))
        
        # Sombra
        sombra = self.fuente_grande.render("K.O.", True, NEGRO)
        sombra_rect = sombra.get_rect(center=(ANCHO // 2 + 3, ALTO // 2 + 3))
        self.pantalla.blit(sombra, sombra_rect)
        self.pantalla.blit(texto_ko, texto_rect)
        
        pygame.display.flip()
        
        # Verificar si termino la animacion
        if tiempo_transcurrido > self.duracion_ko:
            self.mostrando_ko = False
            if not self.pelea_terminada:
                self.iniciar_cuenta_regresiva()
            return True
        
        return False
    
    def mostrar_cuenta_regresiva(self, fondo, jugador1, jugador2):
        """Muestra la cuenta regresiva 3, 2, 1 entre rounds"""
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - self.tiempo_cuenta_regresiva) / 1000
        
        if fondo:
            self.pantalla.blit(fondo, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        jugador1.dibujar(self.pantalla)
        jugador2.dibujar(self.pantalla)
        self.ui.dibujar_barras_jugadores(jugador1, jugador2, self.rounds_jugador1, self.rounds_jugador2)
        self.ui.dibujar_timer(0, en_introduccion=True)
        
        # Mostrar "ROUND X"
        if tiempo_transcurrido < 1.5:
            texto_round = self.fuente_grande.render(f"ROUND {self.round_actual}", True, AMARILLO)
            texto_rect = texto_round.get_rect(center=(ANCHO // 2, ALTO // 2 - 50))
            sombra = self.fuente_grande.render(f"ROUND {self.round_actual}", True, NEGRO)
            sombra_rect = sombra.get_rect(center=(ANCHO // 2 + 3, ALTO // 2 - 47))
            self.pantalla.blit(sombra, sombra_rect)
            self.pantalla.blit(texto_round, texto_rect)
        
        # Cuenta regresiva 3, 2, 1
        elif tiempo_transcurrido < 4.5:
            tiempo_cuenta = tiempo_transcurrido - 1.5
            numero = 3 - int(tiempo_cuenta)
            
            if numero > 0:
                texto = str(numero)
                color = AMARILLO
            else:
                texto = "FIGHT!"
                color = ROJO
            
            texto_render = self.fuente_grande.render(texto, True, color)
            texto_rect = texto_render.get_rect(center=(ANCHO // 2, ALTO // 2))
            
            sombra = self.fuente_grande.render(texto, True, NEGRO)
            sombra_rect = sombra.get_rect(center=(ANCHO // 2 + 3, ALTO // 2 + 3))
            self.pantalla.blit(sombra, sombra_rect)
            self.pantalla.blit(texto_render, texto_rect)
        else:
            self.en_cuenta_regresiva = False
            return pygame.time.get_ticks()  # Retorna tiempo para iniciar combate
        
        pygame.display.flip()
        return None
    
    def mostrar_pantalla_final(self):
        """Muestra la pantalla final con estadisticas"""
        ganador = "JUGADOR 1" if self.rounds_jugador1 > self.rounds_jugador2 else "JUGADOR 2"
        color_ganador = AMARILLO
        
        # Calcular tiempo total
        tiempo_total = (pygame.time.get_ticks() - self.tiempo_inicio_pelea_total) // 1000
        minutos = tiempo_total // 60
        segundos = tiempo_total % 60
        
        # Botones
        boton_menu = pygame.Rect(ANCHO // 2 - 250, ALTO - 100, 200, 50)
        boton_rematch = pygame.Rect(ANCHO // 2 + 50, ALTO - 100, 200, 50)
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "menu"
                    elif evento.key == pygame.K_RETURN:
                        return "rematch"
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if boton_menu.collidepoint(evento.pos):
                        return "menu"
                    elif boton_rematch.collidepoint(evento.pos):
                        return "rematch"
            
            # Fondo
            self.pantalla.fill((10, 10, 30))
            
            # Titulo
            titulo = self.ui.fuente_press_start_grande.render("VICTORIA", True, color_ganador)
            self.pantalla.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 50))
            
            # Ganador
            texto_ganador = self.ui.fuente_press_start_mediana.render(f"{ganador} GANA!", True, AMARILLO)
            self.pantalla.blit(texto_ganador, (ANCHO // 2 - texto_ganador.get_width() // 2, 120))
            
            # Rounds
            texto_rounds = self.ui.fuente_press_start.render(
                f"Rounds: {self.rounds_jugador1} - {self.rounds_jugador2}", 
                True, BLANCO
            )
            self.pantalla.blit(texto_rounds, (ANCHO // 2 - texto_rounds.get_width() // 2, 180))
            
            # Estadisticas J1
            y_stats = 240
            stats_j1_titulo = self.ui.fuente_press_start.render("JUGADOR 1", True, AMARILLO)
            self.pantalla.blit(stats_j1_titulo, (100, y_stats))
            
            stats_j1 = [
                f"Golpes: {self.stats_jugador1['golpes_totales']}",
                f"Dano causado: {int(self.stats_jugador1['dano_causado'])}",
                f"Dano recibido: {int(self.stats_jugador1['dano_recibido'])}"
            ]
            
            for i, stat in enumerate(stats_j1):
                texto = self.ui.fuente_ui_pequena.render(stat, True, BLANCO)
                self.pantalla.blit(texto, (100, y_stats + 30 + i * 25))
            
            # Estadisticas J2
            stats_j2_titulo = self.ui.fuente_press_start.render("JUGADOR 2", True, AMARILLO)
            self.pantalla.blit(stats_j2_titulo, (ANCHO - 300, y_stats))
            
            stats_j2 = [
                f"Golpes: {self.stats_jugador2['golpes_totales']}",
                f"Dano causado: {int(self.stats_jugador2['dano_causado'])}",
                f"Dano recibido: {int(self.stats_jugador2['dano_recibido'])}"
            ]
            
            for i, stat in enumerate(stats_j2):
                texto = self.ui.fuente_ui_pequena.render(stat, True, BLANCO)
                self.pantalla.blit(texto, (ANCHO - 300, y_stats + 30 + i * 25))
            
            # Tiempo total
            tiempo_texto = self.ui.fuente_press_start.render(
                f"Tiempo total: {minutos}:{segundos:02d}", 
                True, NARANJA
            )
            self.pantalla.blit(tiempo_texto, (ANCHO // 2 - tiempo_texto.get_width() // 2, 400))
            
            # Botones
            pygame.draw.rect(self.pantalla, NARANJA, boton_menu)
            pygame.draw.rect(self.pantalla, AMARILLO, boton_rematch)
            
            texto_menu = self.ui.fuente_press_start.render("MENU", True, NEGRO)
            texto_rematch = self.ui.fuente_press_start.render("REMATCH", True, NEGRO)
            
            self.pantalla.blit(texto_menu, (boton_menu.centerx - texto_menu.get_width() // 2, 
                                           boton_menu.centery - texto_menu.get_height() // 2))
            self.pantalla.blit(texto_rematch, (boton_rematch.centerx - texto_rematch.get_width() // 2, 
                                              boton_rematch.centery - texto_rematch.get_height() // 2))
            
            pygame.display.flip()
            self.reloj.tick(FPS)