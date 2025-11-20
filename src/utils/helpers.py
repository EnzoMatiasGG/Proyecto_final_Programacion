# Funciones auxiliares y utilidades compartidas

import pygame
from typing import Tuple, Optional

def cargar_imagen_con_colorkey(ruta : str, escala : int = 2, colorkey : Tuple[int, int, int] = (255, 255, 255)) -> pygame.Surface :
    """Carga una imagen con transparencia basada en colorkey"""
    try :
        imagen = pygame.image.load(ruta).convert()
        imagen.set_colorkey(colorkey)
        ancho, alto = imagen.get_size()
        imagen = pygame.transform.scale(imagen, (ancho * escala, alto * escala))
        return imagen
    except pygame.error as e :
        print(f"Error cargando imagen {ruta} : {e}")
        # Retornar superficie vacia como fallback
        return pygame.Surface((64 * escala, 64 * escala))


def cargar_imagen_con_alpha(ruta : str, escala : int = 2) -> pygame.Surface :
    """Carga una imagen PNG con canal alpha real"""
    try :
        imagen = pygame.image.load(ruta).convert_alpha()
        ancho, alto = imagen.get_size()
        imagen = pygame.transform.scale(imagen, (ancho * escala, alto * escala))
        return imagen
    except pygame.error as e :
        print(f"Error cargando imagen {ruta} : {e}")
        return pygame.Surface((64 * escala, 64 * escala), pygame.SRCALPHA)


def cargar_fuente(ruta : str, tamano : int) -> pygame.font.Font :
    """Carga una fuente personalizada con fallback a fuente del sistema"""
    try :
        return pygame.font.Font(ruta, tamano)
    except :
        print(f"No se pudo cargar la fuente {ruta}, usando fuente del sistema")
        return pygame.font.SysFont(None, tamano)


def centrar_texto(texto_surface : pygame.Surface, centro_x : int, centro_y : int) -> Tuple[int, int] :
    """Calcula la posicion para centrar un texto"""
    rect = texto_surface.get_rect(center=(centro_x, centro_y))
    return rect.topleft


def dibujar_texto_con_sombra(pantalla : pygame.Surface, fuente : pygame.font.Font, texto : str, color_texto : Tuple[int, int, int], color_sombra : Tuple[int, int, int], centro_x : int, centro_y : int, offset_sombra : int = 3) :
    """Dibuja texto con efecto de sombra"""
    # Sombra
    sombra = fuente.render(texto, True, color_sombra)
    rect_sombra = sombra.get_rect(center=(centro_x + offset_sombra, centro_y + offset_sombra))
    pantalla.blit(sombra, rect_sombra)
    
    # Texto principal
    texto_render = fuente.render(texto, True, color_texto)
    rect_texto = texto_render.get_rect(center=(centro_x, centro_y))
    pantalla.blit(texto_render, rect_texto)


def crear_overlay(ancho : int, alto : int, color : Tuple[int, int, int] = (0, 0, 0), alpha : int = 128) -> pygame.Surface :
    """Crea una superficie semi-transparente para overlay"""
    overlay = pygame.Surface((ancho, alto), pygame.SRCALPHA)
    overlay.fill((*color, alpha))
    return overlay


def limitar_valor(valor : float, minimo : float, maximo : float) -> float :
    """Limita un valor entre un minimo y maximo"""
    return max(minimo, min(valor, maximo))


def calcular_distancia(x1 : float, y1 : float, x2 : float, y2 : float) -> Tuple[float, float] :
    """Calcula la distancia entre dos puntos en X e Y"""
    return abs(x2 - x1), abs(y2 - y1)


def formatear_tiempo(segundos : int) -> str :
    """Formatea segundos a formato MM :SS"""
    minutos = segundos // 60
    segs = segundos % 60
    return f"{minutos} :{segs :02d}"


def interpolacion_lineal(inicio : float, fin : float, t : float) -> float :
    """Interpolacion lineal entre dos valores"""
    return inicio + (fin - inicio) * t


def crear_rectangulo_con_borde(pantalla : pygame.Surface, x : int, y : int, ancho : int, alto : int, color_relleno : Tuple[int, int, int], color_borde : Tuple[int, int, int], grosor_borde : int = 2) :
    """Dibuja un rectangulo con relleno y borde"""
    rect = pygame.Rect(x, y, ancho, alto)
    pygame.draw.rect(pantalla, color_relleno, rect)
    pygame.draw.rect(pantalla, color_borde, rect, grosor_borde)


def parpadeo(tiempo_actual : int, intervalo : int = 500) -> bool :
    """Genera un efecto de parpadeo basado en el tiempo"""
    return (tiempo_actual // intervalo) % 2 == 0


def escalar_mantener_aspecto(imagen : pygame.Surface, ancho_objetivo : int, alto_objetivo : int) -> pygame.Surface :
    """Escala una imagen manteniendo su relacion de aspecto"""
    ancho_original, alto_original = imagen.get_size()
    ratio = min(ancho_objetivo / ancho_original, alto_objetivo / alto_original)
    
    nuevo_ancho = int(ancho_original * ratio)
    nuevo_alto = int(alto_original * ratio)
    
    return pygame.transform.scale(imagen, (nuevo_ancho, nuevo_alto))


def validar_entrada_alfabetica(caracter : str) -> bool :
    """Valida que un caracter sea alfabetico"""
    return caracter.isalpha() and len(caracter) == 1