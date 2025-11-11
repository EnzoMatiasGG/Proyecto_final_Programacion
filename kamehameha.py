import pygame

class Kamehameha:
    """Representa un ataque Kamehameha con animación de 3 partes"""
    
    def __init__(self, x, y, direccion, sprite_personaje, imagenes_kamehameha):
        """
        Args:
            x: Posición X del origen (personaje)
            y: Posición Y del origen (personaje)
            direccion: True = derecha, False = izquierda
            sprite_personaje: Sprite del personaje para calcular altura
            imagenes_kamehameha: Lista [inicio, cuerpo, final]
        """
        self.origen_x = x
        self.origen_y = y
        self.direccion = direccion
        self.sprite_personaje = sprite_personaje
        
        # Cargar imágenes
        self.imagen_inicio = imagenes_kamehameha[0] if len(imagenes_kamehameha) > 0 else None
        self.imagen_cuerpo = imagenes_kamehameha[1] if len(imagenes_kamehameha) > 1 else None
        self.imagen_final = imagenes_kamehameha[2] if len(imagenes_kamehameha) > 2 else None
        
        # Control de tiempo
        self.tiempo_inicio = pygame.time.get_ticks()
        self.duracion = 1000  
        self.velocidad_expansion = 15  # Píxeles por frame
        
        # Partes del kamehameha
        self.partes = []
        self.activo = True
        self.impacto = False  # Indica si ya impactó con algo
        self.distancia_maxima = 0  # Distancia máxima alcanzada
        
    def actualizar(self):
        """Actualiza la animación del kamehameha"""
        tiempo_actual = pygame.time.get_ticks()
        tiempo_transcurrido = tiempo_actual - self.tiempo_inicio
        
        # Verificar si terminó la duración
        if tiempo_transcurrido > self.duracion:
            self.activo = False
            return
        
        # Limpiar partes anteriores
        self.partes = []
        
        # Calcular centro vertical
        centro_y = self.origen_y + self.sprite_personaje.get_height() // 2
        
        # Calcular distancia (se detiene si ya impacto)
        if not self.impacto:
            distancia = (tiempo_transcurrido - 100) / 10 * self.velocidad_expansion
            self.distancia_maxima = distancia
        else:
            distancia = self.distancia_maxima  
        # FASE 1: Punta del kamehameha 
        if tiempo_transcurrido >= 100 and self.imagen_final:
            if self.direccion:  # Derecha
                x_final = self.origen_x + distancia
            else:  # Izquierda
                x_final = self.origen_x - distancia - self.imagen_final.get_width()
            
            self.partes.append({
                'tipo': 'final',
                'x': x_final,
                'y': centro_y - self.imagen_final.get_height() // 2,
                'imagen': self.imagen_final
            })
        
        # FASE 2: Cuerpo del kamehameha 
        if tiempo_transcurrido >= 300 and self.imagen_cuerpo and len(self.partes) > 0:
            if self.direccion:  # Derecha
                x_cuerpo = self.origen_x
                ancho_cuerpo = self.partes[0]['x'] - self.origen_x
            else:  # Izquierda
                ancho_cuerpo = self.origen_x - (self.partes[0]['x'] + self.imagen_final.get_width())
                x_cuerpo = self.partes[0]['x'] + self.imagen_final.get_width()
            
            if ancho_cuerpo > 0:
                cuerpo_escalado = pygame.transform.scale(
                    self.imagen_cuerpo,
                    (int(ancho_cuerpo), self.imagen_cuerpo.get_height())
                )
                
                self.partes.append({
                    'tipo': 'cuerpo',
                    'x': x_cuerpo,
                    'y': centro_y - cuerpo_escalado.get_height() // 2,
                    'imagen': cuerpo_escalado
                })
        
        # FASE 3: Inicio del kamehameha 
        if tiempo_transcurrido >= 500 and self.imagen_inicio:
            if self.direccion:  # Derecha
                x_inicio = self.origen_x
            else:  # Izquierda
                x_inicio = self.origen_x - self.imagen_inicio.get_width()
            
            self.partes.append({
                'tipo': 'inicio',
                'x': x_inicio,
                'y': centro_y - self.imagen_inicio.get_height() // 2,
                'imagen': self.imagen_inicio
            })
    
    def dibujar(self, pantalla):
        """Dibuja todas las partes del kamehameha"""
        if not self.activo:
            return
        # Dibuja en orden: inicio, cuerpo, final
        partes_ordenadas = sorted(self.partes, key=lambda p: ['inicio', 'cuerpo', 'final'].index(p['tipo']))
        
        for parte in partes_ordenadas:
            imagen = parte['imagen']
            if not self.direccion:# Voltear imagen si va hacia la izquierda
                imagen = pygame.transform.flip(imagen, True, False)
            pantalla.blit(imagen, (parte['x'], parte['y']))
    
    def obtener_hitboxes(self):
        """Retorna las hitboxes de todas las partes del kamehameha"""
        hitboxes = []
        for parte in self.partes:
            hitbox = pygame.Rect(
                parte['x'],
                parte['y'],
                parte['imagen'].get_width(),
                parte['imagen'].get_height()
            )
            hitboxes.append(hitbox)
        return hitboxes
    
    def esta_activo(self):
        """Verifica si el kamehameha sigue activo"""
        return self.activo
    
    def marcar_impacto(self):
        """Marca que el kamehameha impactó con algo y debe detenerse"""
        self.impacto = True