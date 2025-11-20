# Modulo de proyectiles
# Maneja las bolas de energia y proyectiles especiales

import pygame
from src.utils.config import TimeConfig


class Projectile :
    """Representa un proyectil de energia"""
    
    def __init__(self, x : float, y : float, direccion : bool, imagen_original : pygame.Surface, velocidad : int = None,dano : float = None) :

        """Inicializa un proyectil"""
        self.x = x
        self.y = y
        self.direccion = direccion
        self.velocidad = velocidad or TimeConfig.VELOCIDAD_PROYECTIL
        self.dano_custom = dano  # Daño personalizado (para movimientos finales)
        
        # Voltea las imagenes si va hacia la izquierda
        if direccion :
            self.imagen = imagen_original.copy()
        else :
            self.imagen = pygame.transform.flip(imagen_original.copy(), True, False)
        
        self.rect = self.imagen.get_rect(center=(self.x, self.y))
        self.activa = True
    
    def actualizar(self) :
        """Actualiza la posicion del proyectil"""
        if self.direccion :
            self.x += self.velocidad
        else :
            self.x -= self.velocidad
        
        self.rect.center = (self.x, self.y)
    
    def dibujar(self, pantalla : pygame.Surface) :
        """Dibuja el proyectil en pantalla"""
        if self.activa :
            pantalla.blit(self.imagen, self.rect)
    
    def esta_fuera_de_pantalla(self, ancho_pantalla : int) -> bool :
        """Verifica si el proyectil salio de la pantalla"""
        return self.x < -50 or self.x > ancho_pantalla + 50
    
    def obtener_dano(self) -> float :
        """Obtiene el daño del proyectil"""
        return self.dano_custom if self.dano_custom is not None else 0