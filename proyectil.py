import pygame

class BolaEnergia:
    """Representa un proyectil de energia lanzado por un peleador"""
    def __init__(self, x, y, direccion, imagen_original, velocidad=12):
        self.x = x
        self.y = y
        self.direccion = direccion  # True = derecha, False = izquierda

        self.imagen = imagen_original.copy()

        self.velocidad = velocidad
        self.rect = self.imagen.get_rect(center=(self.x, self.y))
        self.activa = True

    def actualizar(self):
        """Actualiza la posicion de la bola"""
        if self.direccion:
            self.x += self.velocidad
        else:
            self.x -= self.velocidad
        self.rect.center = (self.x, self.y)

    def dibujar(self, pantalla):
        """Dibuja la bola en la pantalla"""
        if self.activa:
            pantalla.blit(self.imagen, self.rect)

    def esta_fuera_de_pantalla(self, ancho_pantalla):
        """Verifica si la bola salio de la pantalla"""
        return self.x < -50 or self.x > ancho_pantalla + 50
