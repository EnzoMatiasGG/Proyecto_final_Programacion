import pygame
from proyectil import BolaEnergia
from kamehameha import Kamehameha
from config import ANCHO, ALTO

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

        # Sistema de golpes
        self.golpe_animando = False
        self.golpe_tipo = None
        self.golpe_frame = 0
        self.golpe_contador = 0
        self.golpe_tiempo_frame = 100
        self.golpe_ultimo_tiempo = 0

        # Sistema de hitbox para colisiones
        self.hitbox_activa = False
        self.hitbox_ataque = None
        self.dano_golpe_j = 5
        self.dano_patada_k = 8
        self.dano_bola = 10

        # Sistema de kamehameha 
        self.usando_kamehameha = False
        self.kamehameha_inicio_tiempo = 0
        self.kamehameha_duracion = 800  

        # Sistema de defensa
        self.cubriendose = False

        # Sistema de proyectiles
        self.bolas_activas = []
        self.imagen_bola_original = self.sprites.get('poder_ligero', None)
        self.imagen_bola = self.imagen_bola_original if self.imagen_bola_original else None

        # Animacion lanzamiento bola
        self.lanzando_bola = False
        self.bola_energia_frames = self.sprites.get('bola_energia', [])
        self.bola_contador_mano = 0
        self.bola_energia_tiempo_frame = 150
        self.bola_energia_inicio_tiempo = 0

        # Sistema de vida y energia
        self.vida_maxima = 100
        self.vida_actual = 100
        self.stamina_maxima = 100
        self.stamina_actual = 100
        self.regeneracion_stamina = 0.15
        self.costo_stamina_golpe = 5
        self.costo_stamina_patada = 8
        self.costo_stamina_bola = 15
        self.costo_stamina_kamehameha = 50

        # Sistema de kamehameha
        self.kamehameha_activo = None
        self.usando_kamehameha = False
        self.costo_stamina_kamehameha = 50
        self.imagenes_kamehameha = self.sprites.get('kamehameha_poder', [])

        # Sistema de aturdimiento 
        self.golpes_consecutivos = 0
        self.tiempo_ultimo_golpe = 0
        self.tiempo_reseteo_combo = 2000
        self.aturdido = False
        self.tiempo_inicio_aturdido = 0
        self.duracion_aturdido = 1000  

        # Sistema de KO 
        self.en_ko = False
        self.ko_frame = 0
        self.ko_tiempo_frame = 300  
        self.ko_ultimo_tiempo = 0
        self.ko_animacion_completada = False

        # Sistema de movimiento final
        self.usando_movimiento_final = False
        self.movimiento_final_frame = 0
        self.movimiento_final_tiempo_frame = 200
        self.movimiento_final_inicio_tiempo = 0
        self.movimiento_final_tipo = None
        self.costo_stamina_movimiento_final = 80

    def obtener_dano_ataque(self):
        """Retorna el daño del ataque actual"""
        if self.golpe_tipo == 'golpe_j':
            return self.dano_golpe_j
        elif self.golpe_tipo == 'patada_k':
            return self.dano_patada_k
        return 0

    def crear_hitbox_ataque(self):
        """Crea la hitbox del ataque basada en la direccion del personaje"""
        ancho_hitbox = 60
        alto_hitbox = 40
        
        if self.mirando_derecha:
            x_hitbox = self.x + self.sprite.get_width()
            y_hitbox = self.y + self.sprite.get_height() // 2 - alto_hitbox // 2
        else:
            x_hitbox = self.x - ancho_hitbox
            y_hitbox = self.y + self.sprite.get_height() // 2 - alto_hitbox // 2
        
        self.hitbox_ataque = pygame.Rect(x_hitbox, y_hitbox, ancho_hitbox, alto_hitbox)
        self.hitbox_activa = True

    def dibujar(self, pantalla):
        imagen = self.sprite
        if not self.mirando_derecha:
            imagen = pygame.transform.flip(imagen, True, False)
        pantalla.blit(imagen, (self.x, self.y))

        if self.kamehameha_activo:
            self.kamehameha_activo.dibujar(pantalla)

        self.dibujar_proyectiles(pantalla)

    def actualizar(self):
        self.rect = pygame.Rect(self.x, self.y, self.sprite.get_width(), self.sprite.get_height())
        
        if self.en_ko:
            self.actualizar_ko()
            return
        
        if self.aturdido:
            self.actualizar_aturdimiento()
            return
        
        if self.lanzando_bola:
            self.actualizar_animacion_bola()
        if self.golpe_animando:
            self.actualizar_golpe()
        if self.usando_kamehameha:
            self.actualizar_kamehameha()
        if self.usando_movimiento_final:
            self.actualizar_movimiento_final()
        
        if not self.golpe_animando and not self.lanzando_bola and not self.usando_kamehameha and not self.usando_movimiento_final:
            self.regenerar_stamina()

    def regenerar_stamina(self):
        if self.stamina_actual < self.stamina_maxima:
            self.stamina_actual = min(self.stamina_maxima, self.stamina_actual + self.regeneracion_stamina)

    def tiene_stamina(self, costo):
        return self.stamina_actual >= costo

    def consumir_stamina(self, cantidad):
        self.stamina_actual = max(0, self.stamina_actual - cantidad)

    def recibir_dano(self, cantidad):
        """Reduce la vida del personaje y retorna el daño real recibido"""
        if self.aturdido:
            cantidad = cantidad * 2
        
        if not self.cubriendose:
            dano_real = cantidad
            self.vida_actual = max(0, self.vida_actual - cantidad)
        else:
            dano_real = cantidad * 0.3
            self.vida_actual = max(0, self.vida_actual - dano_real)
        
        if self.vida_actual <= 0 and not self.en_ko:
            self.iniciar_ko()
        
        return dano_real

    def iniciar_golpe(self, tipo_golpe):
        costo = self.costo_stamina_golpe if tipo_golpe == 'golpe_j' else self.costo_stamina_patada
        
        if not self.golpe_animando and self.tiene_stamina(costo):
            self.consumir_stamina(costo)
            self.golpe_animando = True
            self.golpe_tipo = tipo_golpe
            self.golpe_frame = 0
            self.golpe_ultimo_tiempo = pygame.time.get_ticks()
            
            self.crear_hitbox_ataque()
            
            if tipo_golpe == 'golpe_j':
                self.golpe_contador = (self.golpe_contador + 1) % 2
                self.sprite = self.sprites['golpe_j'][self.golpe_contador]
            elif tipo_golpe == 'patada_k':
                self.sprite = self.sprites['patada_k'][self.golpe_frame]

    def actualizar_golpe(self):
        ahora = pygame.time.get_ticks()
        if self.golpe_tipo == 'golpe_j':
            if ahora - self.golpe_ultimo_tiempo > self.golpe_tiempo_frame:
                self.golpe_animando = False
                self.hitbox_activa = False
                self.hitbox_ataque = None
                self.estado = 'inicio'
                self.sprite = self.sprites[self.estado]
        elif self.golpe_tipo == 'patada_k':
            if ahora - self.golpe_ultimo_tiempo > self.golpe_tiempo_frame:
                self.golpe_ultimo_tiempo = ahora
                self.golpe_frame += 1
                if self.golpe_frame < len(self.sprites['patada_k']):
                    self.sprite = self.sprites['patada_k'][self.golpe_frame]
                    self.crear_hitbox_ataque()
                else:
                    self.golpe_animando = False
                    self.hitbox_activa = False
                    self.hitbox_ataque = None
                    self.estado = 'inicio'
                    self.sprite = self.sprites[self.estado]

    def iniciar_kamehameha(self):
        if 'kamehameha' not in self.sprites or not self.imagenes_kamehameha:
            return
            
        if not self.usando_kamehameha and self.tiene_stamina(self.costo_stamina_kamehameha):
            self.consumir_stamina(self.costo_stamina_kamehameha)
            self.usando_kamehameha = True
            self.estado = 'kamehameha'
            self.sprite = self.sprites['kamehameha']
            
            if self.mirando_derecha:
                origen_x = self.x + self.sprite.get_width()
            else:
                origen_x = self.x
            
            self.kamehameha_activo = Kamehameha(
                origen_x,
                self.y,
                self.mirando_derecha,
                self.sprite,
                self.imagenes_kamehameha
            )

    def actualizar_kamehameha(self):
        if self.kamehameha_activo:
            self.kamehameha_activo.actualizar()
            
            if not self.kamehameha_activo.esta_activo():
                self.usando_kamehameha = False
                self.kamehameha_activo = None
                self.estado = 'inicio'
                self.sprite = self.sprites[self.estado]

    def cubrirse(self):
        self.cubriendose = True
        self.estado = 'cubrirse'
        self.sprite = self.sprites['cubrirse']

    def dejar_de_cubrirse(self):
        self.cubriendose = False
        self.estado = 'inicio'
        self.sprite = self.sprites[self.estado]

    def iniciar_lanzar_bola(self):
        if not self.lanzando_bola and not self.golpe_animando and not self.cubriendose and self.tiene_stamina(self.costo_stamina_bola):
            self.consumir_stamina(self.costo_stamina_bola)
            self.lanzando_bola = True
            self.bola_energia_inicio_tiempo = pygame.time.get_ticks()
            
            if isinstance(self.bola_energia_frames, list) and len(self.bola_energia_frames) >= 2:
                self.sprite = self.bola_energia_frames[self.bola_contador_mano]
                self.bola_contador_mano = (self.bola_contador_mano + 1) % 2
            elif isinstance(self.bola_energia_frames, list) and len(self.bola_energia_frames) == 1:
                self.sprite = self.bola_energia_frames[0]
            
            self.lanzar_bola()

    def actualizar_animacion_bola(self):
        if not self.lanzando_bola:
            return
        ahora = pygame.time.get_ticks()
        tiempo_transcurrido = ahora - self.bola_energia_inicio_tiempo
        if tiempo_transcurrido > self.bola_energia_tiempo_frame:
            self.lanzando_bola = False
            self.estado = 'inicio'
            self.sprite = self.sprites[self.estado]

    def lanzar_bola(self):
        if self.imagen_bola is None:
            return
        centro_y = self.y + self.sprite.get_height() // 2
        if self.mirando_derecha:
            inicio_x = self.x + self.sprite.get_width()
            direccion = True
        else:
            inicio_x = self.x
            direccion = False
        nueva_bola = BolaEnergia(inicio_x, centro_y, direccion, self.imagen_bola)
        self.bolas_activas.append(nueva_bola)

    def actualizar_proyectiles(self):
        for bola in self.bolas_activas[:]:
            bola.actualizar()
            if bola.esta_fuera_de_pantalla(ANCHO):
                self.bolas_activas.remove(bola)

    def mover(self, teclas):
        if self.golpe_animando or self.lanzando_bola or self.cubriendose or self.usando_kamehameha or self.aturdido or self.en_ko or self.usando_movimiento_final:
            return
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

    def dibujar_proyectiles(self, pantalla):
        for bola in self.bolas_activas:
            bola.dibujar(pantalla)

    def recibir_golpe_combo(self):
        """Registra un golpe para el combo de aturdimiento"""
        ahora = pygame.time.get_ticks()
        
        if ahora - self.tiempo_ultimo_golpe > self.tiempo_reseteo_combo:
            self.golpes_consecutivos = 0
        
        self.golpes_consecutivos += 1
        self.tiempo_ultimo_golpe = ahora
        
        if self.golpes_consecutivos >= 4 and not self.aturdido:
            self.iniciar_aturdimiento()

    def iniciar_aturdimiento(self):
        """Inicia el estado de aturdimiento"""
        self.aturdido = True
        self.tiempo_inicio_aturdido = pygame.time.get_ticks()
        self.golpes_consecutivos = 0
        self.estado = 'aturdido'
        if 'aturdido' in self.sprites:
            self.sprite = self.sprites['aturdido']

    def actualizar_aturdimiento(self):
        """Actualiza el estado de aturdimiento"""
        if not self.aturdido:
            return
        
        ahora = pygame.time.get_ticks()
        if ahora - self.tiempo_inicio_aturdido > self.duracion_aturdido:
            self.aturdido = False
            self.estado = 'inicio'
            self.sprite = self.sprites['inicio']

    def iniciar_ko(self):
        """Inicia la animación de KO"""
        if 'ko' not in self.sprites or len(self.sprites['ko']) == 0:
            return
        
        self.en_ko = True
        self.ko_frame = 0
        self.ko_ultimo_tiempo = pygame.time.get_ticks()
        self.ko_animacion_completada = False
        self.sprite = self.sprites['ko'][0]

    def actualizar_ko(self):
        """Actualiza la animación de KO - MEJORADO"""
        if not self.en_ko or 'ko' not in self.sprites:
            return
        
        ahora = pygame.time.get_ticks()
        
        if ahora - self.ko_ultimo_tiempo > self.ko_tiempo_frame:
            self.ko_ultimo_tiempo = ahora
            self.ko_frame = (self.ko_frame + 1) % len(self.sprites['ko'])
            self.sprite = self.sprites['ko'][self.ko_frame]

    def resetear_ko(self):
        """Resetea el estado de KO para un nuevo round"""
        self.en_ko = False
        self.ko_frame = 0
        self.ko_animacion_completada = False
        self.vida_actual = self.vida_maxima
        self.estado = 'inicio'
        self.sprite = self.sprites['inicio']

    def iniciar_movimiento_final(self):
        """Inicia el movimiento final específico del personaje"""
        if self.usando_movimiento_final or not self.tiene_stamina(self.costo_stamina_movimiento_final):
            return
        
        if 'genki_pose' in self.sprites:
            self.movimiento_final_tipo = 'genkidama'
        elif 'galick_gun' in self.sprites:
            self.movimiento_final_tipo = 'galick_gun'
        elif 'masenko' in self.sprites:
            self.movimiento_final_tipo = 'masenko'
        elif 'Ulti' in self.sprites:
            self.movimiento_final_tipo = 'bola_maligna'
        else:
            return
        
        self.consumir_stamina(self.costo_stamina_movimiento_final)
        self.usando_movimiento_final = True
        self.movimiento_final_frame = 0
        self.movimiento_final_inicio_tiempo = pygame.time.get_ticks()

    def actualizar_movimiento_final(self):
        """Actualiza la animación del movimiento final"""
        if not self.usando_movimiento_final:
            return
        
        ahora = pygame.time.get_ticks()
        tiempo_transcurrido = ahora - self.movimiento_final_inicio_tiempo
        
        if self.movimiento_final_tipo == 'genkidama' and 'genki_pose' in self.sprites:
            frames = self.sprites['genki_pose']
        elif self.movimiento_final_tipo == 'galick_gun' and 'galick_gun' in self.sprites:
            frames = self.sprites['galick_gun']
        elif self.movimiento_final_tipo == 'masenko' and 'masenko' in self.sprites:
            frames = self.sprites['masenko']
        elif self.movimiento_final_tipo == 'bola_maligna' and 'Ulti' in self.sprites:
            frames = self.sprites['Ulti']
        else:
            self.usando_movimiento_final = False
            return
        
        if tiempo_transcurrido > self.movimiento_final_tiempo_frame * self.movimiento_final_frame:
            self.movimiento_final_frame += 1
            
            if self.movimiento_final_frame < len(frames):
                self.sprite = frames[self.movimiento_final_frame]
            else:
                self.lanzar_movimiento_final()
                self.usando_movimiento_final = False
                self.estado = 'inicio'
                self.sprite = self.sprites['inicio']

    def lanzar_movimiento_final(self):
        """Lanza el proyectil del movimiento final"""
        imagen_proyectil = None
        
        if self.movimiento_final_tipo == 'genkidama' and 'genkidama' in self.sprites:
            imagen_proyectil = self.sprites['genkidama']
        elif self.movimiento_final_tipo == 'galick_gun' and 'galick_gun_poder' in self.sprites:
            imagen_proyectil = self.sprites['galick_gun_poder']
        elif self.movimiento_final_tipo == 'masenko' and 'masenko_poder' in self.sprites:
            imagen_proyectil = self.sprites['masenko_poder']
        elif self.movimiento_final_tipo == 'bola_maligna' and 'Ulti_poder' in self.sprites:
            imagen_proyectil = self.sprites['Ulti_poder']
        
        if imagen_proyectil is None:
            return
        
        centro_y = self.y + self.sprite.get_height() // 2
        
        if self.mirando_derecha:
            inicio_x = self.x + self.sprite.get_width()
            direccion = True
        else:
            inicio_x = self.x
            direccion = False
        
        nueva_bola = BolaEnergia(inicio_x, centro_y, direccion, imagen_proyectil, velocidad=8)
        self.bolas_activas.append(nueva_bola)