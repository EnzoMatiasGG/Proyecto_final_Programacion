import pygame
import sys
from personaje import Peleador
from config import ANCHO, ALTO, ROJO, NEGRO, FPS, CONTROLES_JUGADOR1, CONTROLES_JUGADOR2, AMARILLO, BLANCO, NARANJA
from ui import UI
from rounds import RoundsManager

class Juego:
    """Maneja la logica principal del juego"""
    
    def __init__(self, pantalla, reloj, sprites_personajes, fondo_seleccionado, personaje1_nombre='goku', personaje2_nombre='freezer'):
        self.pantalla = pantalla
        self.reloj = reloj
        self.sprites_personajes = sprites_personajes
        self.personaje1_nombre = personaje1_nombre
        self.personaje2_nombre = personaje2_nombre
        self.jugador1 = None
        self.jugador2 = None
        self.ejecutando = False
        self.en_introduccion = True
        self.tiempo_inicio = 0
        self.fase_intro = "vs"
        
        # Timer del combate
        self.tiempo_combate = 60
        self.tiempo_inicio_combate = 0
        
        # Control de volumen
        self.volumen = 0.5
        
        # Cargar imagen VS
        try:
            self.imagen_vs = pygame.image.load("Assets/Imagenes_especiales/vs.png").convert_alpha()
            ancho_vs = 300
            alto_vs = int(self.imagen_vs.get_height() * (ancho_vs / self.imagen_vs.get_width()))
            self.imagen_vs = pygame.transform.scale(self.imagen_vs, (ancho_vs, alto_vs))
        except:
            self.imagen_vs = None
        
        # Cargar fondo
        try:
            self.fondo = pygame.image.load(fondo_seleccionado).convert()
            self.fondo = pygame.transform.scale(self.fondo, (ANCHO, ALTO))
        except:
            self.fondo = None
        
        # Fuente grande para textos
        self.fuente_grande = pygame.font.SysFont(None, 100)
        
        # Crear modulos
        self.ui = UI(pantalla)
        self.rounds_manager = RoundsManager(pantalla, reloj, self.ui)
        
    def inicializar_jugadores(self, personaje1_nombre, personaje2_nombre='freezer'):
        """Crea los jugadores del juego"""
        self.jugador1 = Peleador(100, ALTO - 150 - 80, CONTROLES_JUGADOR1, self.sprites_personajes[personaje1_nombre])
        self.jugador2 = Peleador(ANCHO - 200, ALTO - 150 - 80, CONTROLES_JUGADOR2, self.sprites_personajes[personaje2_nombre])
        self.jugador2.mirando_derecha = False
    
    def mostrar_introduccion(self):
        """Pantalla VS y cuenta regresiva"""
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = (tiempo_actual - self.tiempo_inicio) / 1000
        
        if self.fondo:
            self.pantalla.blit(self.fondo, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        self.jugador1.dibujar(self.pantalla)
        self.jugador2.dibujar(self.pantalla)
        
        if self.fase_intro == "vs":
            if self.imagen_vs:
                vs_rect = self.imagen_vs.get_rect(center=(ANCHO // 2, ALTO // 2))
                self.pantalla.blit(self.imagen_vs, vs_rect)
            else:
                texto_vs = self.fuente_grande.render("VS", True, ROJO)
                texto_rect = texto_vs.get_rect(center=(ANCHO // 2, ALTO // 2))
                self.pantalla.blit(texto_vs, texto_rect)
            
            if tiempo_transcurrido >= 4.0:
                self.fase_intro = "countdown"
                self.tiempo_inicio = pygame.time.get_ticks()
        
        elif self.fase_intro == "countdown":
            tiempo_countdown = int(4 - tiempo_transcurrido)
            
            if tiempo_countdown > 0:
                texto = str(tiempo_countdown)
                color = AMARILLO
            elif tiempo_transcurrido < 4.5:
                texto = "FIGHT!"
                color = ROJO
            else:
                self.en_introduccion = False
                self.tiempo_inicio_combate = pygame.time.get_ticks()
                return
            
            texto_render = self.fuente_grande.render(texto, True, color)
            texto_rect = texto_render.get_rect(center=(ANCHO // 2, ALTO // 2))
            
            sombra = self.fuente_grande.render(texto, True, NEGRO)
            sombra_rect = sombra.get_rect(center=(ANCHO // 2 + 3, ALTO // 2 + 3))
            self.pantalla.blit(sombra, sombra_rect)
            self.pantalla.blit(texto_render, texto_rect)
        
        pygame.display.flip()
    
    def manejar_eventos(self):
        """Maneja eventos del juego"""
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
            elif evento.type == pygame.KEYDOWN:
                # Control de volumen durante la pelea
                if evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                    self.volumen = max(0.0, self.volumen - 0.1)
                    pygame.mixer.music.set_volume(self.volumen)
                elif evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS or evento.key == pygame.K_EQUALS:
                    self.volumen = min(1.0, self.volumen + 0.1)
                    pygame.mixer.music.set_volume(self.volumen)
                elif evento.key == pygame.K_ESCAPE:
                    self.menu_pausa()
                    return
                
                # Controles JUGADOR 1
                if evento.key == CONTROLES_JUGADOR1['golpe_ligero']:
                    self.jugador1.iniciar_golpe('golpe_j')
                elif evento.key == CONTROLES_JUGADOR1['patada']:
                    self.jugador1.iniciar_golpe('patada_k')
                elif evento.key == CONTROLES_JUGADOR1['cubrirse']:
                    self.jugador1.cubrirse()
                elif evento.key == CONTROLES_JUGADOR1['bola']:
                    self.jugador1.iniciar_lanzar_bola()
                elif evento.key == CONTROLES_JUGADOR1.get('kamehameha'):
                    if evento.key:
                        self.jugador1.iniciar_kamehameha()
                elif evento.key == CONTROLES_JUGADOR1['movimiento_final']:
                    self.jugador1.iniciar_movimiento_final()
                
                # Controles JUGADOR 2
                elif evento.key == CONTROLES_JUGADOR2['golpe_ligero']:
                    self.jugador2.iniciar_golpe('golpe_j')
                elif evento.key == CONTROLES_JUGADOR2['patada']:
                    self.jugador2.iniciar_golpe('patada_k')
                elif evento.key == CONTROLES_JUGADOR2['cubrirse']:
                    self.jugador2.cubrirse()
                elif evento.key == CONTROLES_JUGADOR2['bola']:
                    self.jugador2.iniciar_lanzar_bola()
                elif evento.key == CONTROLES_JUGADOR2.get('movimiento_final'):
                    if evento.key:
                        self.jugador2.iniciar_movimiento_final()
            
            elif evento.type == pygame.KEYUP:# Dejar de cubrirse
                if evento.key == CONTROLES_JUGADOR1['cubrirse']:
                    self.jugador1.dejar_de_cubrirse()
                elif evento.key == CONTROLES_JUGADOR2['cubrirse']:
                    self.jugador2.dejar_de_cubrirse()

    def detectar_colisiones(self):
        """Detecta colisiones entre ataques y personajes"""
        # Ataques cuerpo a cuerpo J1 -> J2
        if self.jugador1.hitbox_activa and self.jugador1.hitbox_ataque:
            if self.jugador1.hitbox_ataque.colliderect(self.jugador2.rect):
                dano = self.jugador1.obtener_dano_ataque()
                dano_real = self.jugador2.recibir_dano(dano)
                self.jugador1.hitbox_activa = False
                self.jugador2.recibir_golpe_combo()
                
                # Actualizar estadisticas
                self.rounds_manager.stats_jugador1['golpes_totales'] += 1
                self.rounds_manager.stats_jugador1['dano_causado'] += dano_real
                self.rounds_manager.stats_jugador2['dano_recibido'] += dano_real
        
        # Ataques cuerpo a cuerpo J2 -> J1
        if self.jugador2.hitbox_activa and self.jugador2.hitbox_ataque:
            if self.jugador2.hitbox_ataque.colliderect(self.jugador1.rect):
                dano = self.jugador2.obtener_dano_ataque()
                dano_real = self.jugador1.recibir_dano(dano)
                self.jugador2.hitbox_activa = False
                self.jugador1.recibir_golpe_combo()
                
                # Actualizar estadisticas
                self.rounds_manager.stats_jugador2['golpes_totales'] += 1
                self.rounds_manager.stats_jugador2['dano_causado'] += dano_real
                self.rounds_manager.stats_jugador1['dano_recibido'] += dano_real
        
        # Proyectiles J1 -> J2
        for bola in self.jugador1.bolas_activas[:]:
            if bola.rect.colliderect(self.jugador2.rect):
                dano_real = self.jugador2.recibir_dano(self.jugador1.dano_bola)
                self.jugador1.bolas_activas.remove(bola)
                
                # Actualizar estadisticas
                self.rounds_manager.stats_jugador1['golpes_totales'] += 1
                self.rounds_manager.stats_jugador1['dano_causado'] += dano_real
                self.rounds_manager.stats_jugador2['dano_recibido'] += dano_real
        
        # Proyectiles J2 -> J1
        for bola in self.jugador2.bolas_activas[:]:
            if bola.rect.colliderect(self.jugador1.rect):
                dano_real = self.jugador1.recibir_dano(self.jugador2.dano_bola)
                self.jugador2.bolas_activas.remove(bola)
                
                # Actualizar estadisticas
                self.rounds_manager.stats_jugador2['golpes_totales'] += 1
                self.rounds_manager.stats_jugador2['dano_causado'] += dano_real
                self.rounds_manager.stats_jugador1['dano_recibido'] += dano_real
        
        # Kamehameha J1 -> J2
        if self.jugador1.kamehameha_activo:
            hitboxes = self.jugador1.kamehameha_activo.obtener_hitboxes()
            for hitbox in hitboxes:
                if hitbox.colliderect(self.jugador2.rect):
                    dano_real = self.jugador2.recibir_dano(0.5)
                    self.jugador1.kamehameha_activo.marcar_impacto()
                    
                    if not hasattr(self.jugador1.kamehameha_activo, '_stats_registradas'):
                        self.rounds_manager.stats_jugador1['dano_causado'] += dano_real
                        self.rounds_manager.stats_jugador2['dano_recibido'] += dano_real
                        self.jugador1.kamehameha_activo._stats_registradas = True
                    break
        
        # Kamehameha J2 -> J1
        if self.jugador2.kamehameha_activo:
            hitboxes = self.jugador2.kamehameha_activo.obtener_hitboxes()
            for hitbox in hitboxes:
                if hitbox.colliderect(self.jugador1.rect):
                    dano_real = self.jugador1.recibir_dano(0.5)
                    self.jugador2.kamehameha_activo.marcar_impacto()
                    
                    if not hasattr(self.jugador2.kamehameha_activo, '_stats_registradas'):
                        self.rounds_manager.stats_jugador2['dano_causado'] += dano_real
                        self.rounds_manager.stats_jugador1['dano_recibido'] += dano_real
                        self.jugador2.kamehameha_activo._stats_registradas = True
                    break
    
    def actualizar(self):
        """Actualiza la logica del juego"""
        teclas = pygame.key.get_pressed()
        
        self.jugador1.actualizar()
        self.jugador2.actualizar()
        
        # Movimiento J1
        if not self.jugador1.golpe_animando and not self.jugador1.cubriendose and not self.jugador1.lanzando_bola and not self.jugador1.usando_kamehameha and not self.jugador1.usando_movimiento_final:
            self.jugador1.mover(teclas)
        
        # Movimiento J2
        if not self.jugador2.golpe_animando and not self.jugador2.cubriendose and not self.jugador2.lanzando_bola and not self.jugador2.usando_kamehameha and not self.jugador2.usando_movimiento_final:
            self.jugador2.mover(teclas)
        
        # Los personajes se miran
        if self.jugador1.x < self.jugador2.x:
            self.jugador1.mirando_derecha = True
            self.jugador2.mirando_derecha = False
        else:
            self.jugador1.mirando_derecha = False
            self.jugador2.mirando_derecha = True
        
        self.jugador1.actualizar_proyectiles()
        self.jugador2.actualizar_proyectiles()
        
        self.detectar_colisiones()
        
        # Verificar si alguien perdio toda su vida
        if self.jugador1.vida_actual <= 0:
            self.rounds_manager.terminar_round(2)
        elif self.jugador2.vida_actual <= 0:
            self.rounds_manager.terminar_round(1)
    
    def dibujar(self):
        """Dibuja todos los elementos"""
        if self.fondo:
            self.pantalla.blit(self.fondo, (0, 0))
        else:
            self.pantalla.fill(NEGRO)
        
        self.jugador1.dibujar(self.pantalla)
        self.jugador2.dibujar(self.pantalla)
        
        self.jugador1.dibujar_proyectiles(self.pantalla)
        self.jugador2.dibujar_proyectiles(self.pantalla)
        
        # Dibujar UI
        self.ui.dibujar_barras_jugadores(self.jugador1, self.jugador2, self.rounds_manager.rounds_jugador1, self.rounds_manager.rounds_jugador2)
        
        # Calcular tiempo restante
        if not self.en_introduccion:
            tiempo_actual = pygame.time.get_ticks()
            segundos_transcurridos = (tiempo_actual - self.tiempo_inicio_combate) / 1000
            tiempo_restante = max(0, self.tiempo_combate - int(segundos_transcurridos))
            self.ui.dibujar_timer(tiempo_restante, en_introduccion=False)
            
            # Verificar si se acabo el tiempo
            if tiempo_restante <= 0:
                self.terminar_combate_por_tiempo()
        else:
            self.ui.dibujar_timer(0, en_introduccion=True)
        
        pygame.display.flip()
    
    def terminar_combate_por_tiempo(self):
        """Termina el combate cuando se acaba el tiempo"""
        if self.jugador1.vida_actual > self.jugador2.vida_actual:
            self.rounds_manager.terminar_round(1)
        elif self.jugador2.vida_actual > self.jugador1.vida_actual:
            self.rounds_manager.terminar_round(2)
        else:
            # Empate
            pass
    
    def ejecutar(self, personaje1_nombre='goku', personaje2_nombre='freezer'):
        """Loop principal del juego"""
        self.inicializar_jugadores(personaje1_nombre, personaje2_nombre)
        self.ejecutando = True
        self.en_introduccion = True
        self.tiempo_inicio = pygame.time.get_ticks()
        self.fase_intro = "vs"
        
        # Reiniciar sistema de rounds
        self.rounds_manager.reiniciar()
        
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load("Sonidos/Sonido_pelea_1.wav")
            pygame.mixer.music.set_volume(self.volumen)
            pygame.mixer.music.play(-1)
        except:
            print("No se pudo cargar la musica de pelea")
        
        while self.ejecutando:
            self.manejar_eventos()
            
            if self.rounds_manager.pelea_terminada:
                resultado = self.rounds_manager.mostrar_pantalla_final()
                if resultado == "menu":
                    self.ejecutando = False
                elif resultado == "rematch":
                    return self.ejecutar(personaje1_nombre, personaje2_nombre)
            elif self.rounds_manager.mostrando_ko:
                # Mostrar animación de KO
                self.rounds_manager.mostrar_animacion_ko(self.fondo, self.jugador1, self.jugador2)
                if not self.rounds_manager.mostrando_ko and not self.rounds_manager.pelea_terminada:
                    # Reiniciar jugadores después de KO
                    self.rounds_manager.reiniciar_jugadores(self.jugador1, self.jugador2)
            elif self.en_introduccion:
                self.mostrar_introduccion()
            elif self.rounds_manager.en_cuenta_regresiva:
                nuevo_tiempo = self.rounds_manager.mostrar_cuenta_regresiva(
                    self.fondo, self.jugador1, self.jugador2
                )
                if nuevo_tiempo:
                    self.tiempo_inicio_combate = nuevo_tiempo
            else:
                self.actualizar()
                self.dibujar()
            
            self.reloj.tick(FPS)
        
        # Al salir, restaurar musica del menu
        pygame.mixer.music.stop()
        try:
            pygame.mixer.music.load("Sonidos/Sonido_menu.wav")
            pygame.mixer.music.set_volume(self.volumen)
            pygame.mixer.music.play(-1)
        except:
            pass
    
    def menu_pausa(self):
        """Menu de pausa"""
        opciones = ["Continuar", "Volver al menu"]
        seleccion = 0

        try:
            fuente = pygame.font.Font("Fuentes/PressStart2P.ttf", 24)
        except:
            fuente = pygame.font.SysFont(None, 24)

        radar_img = pygame.image.load("Assets/Imagenes_especiales/Dragon_Radar.png").convert_alpha()
        escalar = int(ALTO * 0.6)
        radar_img = pygame.transform.smoothscale(radar_img, (escalar, escalar))
        radar_rect = radar_img.get_rect(center=(ANCHO // 2, ALTO // 2))

        fondo_pausa = self.pantalla.copy()

        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_MINUS or evento.key == pygame.K_KP_MINUS:
                        self.volumen = max(0.0, self.volumen - 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_PLUS or evento.key == pygame.K_KP_PLUS or evento.key == pygame.K_EQUALS:
                        self.volumen = min(1.0, self.volumen + 0.1)
                        pygame.mixer.music.set_volume(self.volumen)
                    elif evento.key == pygame.K_UP:
                        seleccion = (seleccion - 1) % len(opciones)
                    elif evento.key == pygame.K_DOWN:
                        seleccion = (seleccion + 1) % len(opciones)
                    elif evento.key == pygame.K_RETURN or evento.key == pygame.K_ESCAPE:
                        if evento.key == pygame.K_ESCAPE or opciones[seleccion] == "Continuar":
                            return
                        elif opciones[seleccion] == "Volver al menu":
                            self.ejecutando = False
                            return

            self.pantalla.blit(fondo_pausa, (0, 0))

            overlay = pygame.Surface((ANCHO, ALTO), pygame.SRCALPHA)
            overlay.fill((15, 15, 30, 180))
            self.pantalla.blit(overlay, (0, 0))

            self.pantalla.blit(radar_img, radar_rect)

            y_inicio = radar_rect.top + escalar // 2 - 40
            for i, opcion in enumerate(opciones):
                color = AMARILLO if i == seleccion else NARANJA
                texto = fuente.render(opcion, True, color)
                rect = texto.get_rect(center=(ANCHO // 2, y_inicio + i * 40))
                self.pantalla.blit(texto, rect)

            pygame.display.flip()
            self.reloj.tick(FPS)