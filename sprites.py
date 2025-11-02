import pygame

def cargar_imagen_transparente(ruta, escala=2):
    imagen = pygame.image.load(ruta).convert()
    color_clave = (255, 255, 255)
    imagen.set_colorkey(color_clave)
    imagen = imagen.convert_alpha()
    ancho, alto = imagen.get_size()
    imagen = pygame.transform.scale(imagen, (ancho * escala, alto * escala))
    return imagen

def cargar_sprites():
    sprites_goku1 = {
        'derecha': cargar_imagen_transparente("Assets/Sprites/Goku/Goku_avanza.png"),
        'izquierda': cargar_imagen_transparente("Assets/Sprites/Goku/Goku_retrocede.png"),
        'bajar': cargar_imagen_transparente("Assets/Sprites/Goku/Goku_baja.png"),
        'inicio': cargar_imagen_transparente("Assets/Sprites/Goku/Goku_11.png"),
    }
    sprites_freezer1 = {
        'derecha': cargar_imagen_transparente("Assets/Sprites/Freezer_1/Freezer1_avanza.png"),
        'izquierda': cargar_imagen_transparente("Assets/Sprites/Freezer_1/Freezer1_retrocede.png"),
        'bajar': cargar_imagen_transparente("Assets/Sprites/Freezer_1/Freezer1_sube-baja.png"),
        'inicio': cargar_imagen_transparente("Assets/Sprites/Freezer_1/Freezer1_inicio.png"),
    }

    sprites_gohan2 = {
        'derecha': cargar_imagen_transparente("Assets/Sprites/GohanSSJ_1/GohankidSSJ_avanza.png"),
        'izquierda': cargar_imagen_transparente("Assets/Sprites/GohanSSJ_1/GohankidSSJ_retrocede.png"),
        'bajar': cargar_imagen_transparente("Assets/Sprites/GohanSSJ_1/GohankidSSJ_sube-baja.png"),
        'inicio': cargar_imagen_transparente("Assets/Sprites/GohanSSJ_1/GohankidSSJ_inicio.png"),
    }

    sprites_cell3 = {
        'derecha': cargar_imagen_transparente("Assets/Sprites/Cell_1/Cell1_avanza.png"),
        'izquierda': cargar_imagen_transparente("Assets/Sprites/Cell_1/Cell1_retrocede.png"),
        'bajar': cargar_imagen_transparente("Assets/Sprites/Cell_1/Cell1_sube-baja.png"),
        'inicio': cargar_imagen_transparente("Assets/Sprites/Cell_1/Cell1_inicio.png"),
    }

    personajes_data = [
        {
            "nombre": "Goku",
            "foto_seleccion": "Assets/Sprites/Goku/Goku_seleccion.png",
            "lore": "Un saiyajin criado en la Tierra, defensor incansable de sus seres queridos."
        },
        {
            "nombre": "Freezer",
            "foto_seleccion": "Assets/Sprites/Freezer_1/Freezer1_seleccion.png",
            "lore": "Conquistador del universo y rival mortal de Goku y los guerreros Z."
        },
        {
            "nombre": "Gohan",
            "foto_seleccion": "Assets/Sprites/GohanSSJ_1/GohankidSSJ_seleccion.png",
            "lore": "Hijo mayor de Goku, combina gran poder con un corazón noble."
        },
        {
            "nombre": "Cell",
            "foto_seleccion": "Assets/Sprites/Cell_1/Cell1_seleccion.png",
            "lore": "Una bio-creación de Dr. Gero, mezcla de las células de los guerreros más poderosos."
        }
    ]
    return sprites_goku1, sprites_freezer1, sprites_gohan2, sprites_cell3, personajes_data

