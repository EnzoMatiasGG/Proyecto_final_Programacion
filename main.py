import pygame
import sys
from sprites import cargar_sprites
from menus import MenuManager
from juego import Juego
from config import ANCHO, ALTO

def main():
    """Funcion principal del juego"""
    # Iniciar pygame
    pygame.init()
    
    # Configurar pantalla
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Dragon Ball Z - Fighting Game")
    icono = pygame.image.load("Assets/Imagenes_especiales/Icono_ventana.png")
    pygame.display.set_icon(icono)
    reloj = pygame.time.Clock()
    
    # Cargar sprites
    sprites_goku, sprites_vegeta, sprites_freezer, sprites_gohan, personajes_data = cargar_sprites()
    
    # Organizar sprites por personaje
    sprites_personajes = {
        'goku': sprites_goku,
        'vegeta': sprites_vegeta,
        'freezer': sprites_freezer,
        'gohan': sprites_gohan,
    }
    
    # Definir mapas disponibles
    mapas_data = [
        {
            "nombre" : "Arena Mario",
            "ruta" : "Fondos/Fondo_Mario.jpg"
        },
        {
            "nombre" : "Artes Marciales",
            "ruta" : "Fondos/Fondo_torneo.jpg"
        },
        {
            "nombre" : "Planeta Namek",
            "ruta" : "Fondos/Fondo_Namek.png"
        },
        {
            "nombre" : "StreetFighter 2",
            "ruta" : "Fondos/Fondo_ST2_Ryu.jpg"
        },
        {
            "nombre" : "Google Dino",
            "ruta" : "Fondos/Fondo_Dino_Google.jpg"
        },
        {
            "nombre" : "Ruinas",
            "ruta" : "Fondos/Fondo_ruinas.png"
        }
    ]
    
    # Crear menu
    menu_manager = MenuManager(pantalla, reloj, personajes_data, mapas_data)
    
    # Mostrar pantalla de inicio
    menu_manager.start_menu()
    
    # Loop principal del juego
    while True:
        opcion = menu_manager.menu_principal()
        
        if opcion == "Salir":
            pygame.quit()
            sys.exit()
            
        elif opcion == "Jugar":
            # Seleccionar personaje jugador 1
            personaje1 = menu_manager.menu_seleccion_personaje(1)
            if personaje1 is None:
                continue  # Volver al menu principal
            
            # Seleccionar mapa
            mapa_seleccionado = menu_manager.menu_seleccion_mapa()
            if mapa_seleccionado is None:
                continue  # Volver al menu principal
            
            
            personaje2 = 'freezer'
            
            # Iniciar juego con las selecciones
            juego = Juego(pantalla, reloj, sprites_personajes, mapa_seleccionado, personaje1, personaje2)
            juego.ejecutar(personaje1_nombre=personaje1, personaje2_nombre=personaje2)
            
        elif opcion == "Personajes":
            menu_manager.menu_personajes()

if __name__ == "__main__":
    main()