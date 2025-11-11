import pygame

def cargar_imagen_transparente_con_blanco(ruta, escala=2):
    # Para sprites con fondo blanco
    imagen = pygame.image.load(ruta).convert()
    imagen.set_colorkey((255, 255, 255))
    ancho, alto = imagen.get_size()
    imagen = pygame.transform.scale(imagen, (ancho * escala, alto * escala))
    return imagen

def cargar_imagen_con_alpha(ruta, escala=2):
    # Para PNG con canal alfa real
    imagen = pygame.image.load(ruta).convert_alpha()
    ancho, alto = imagen.get_size()
    imagen = pygame.transform.scale(imagen, (ancho * escala, alto * escala))
    return imagen

def cargar_sprites():
    sprites_goku1 = {
        'derecha': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_avanza.png"),
        'izquierda': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_retrocede.png"),
        'bajar': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_baja.png"),
        'inicio': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_base.png"),
        'golpe_j': [
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_golpe_puño_derecho.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_golpe_puño_izquierdo.png"),
        ],
        'patada_k': [
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_patada_1.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_patada_2.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_patada_3.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_patada_4.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_patada_5.png"),
        ],
        'cubrirse': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_cubrirse.png"),
        'bola_energia': [
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_bola_energia_1.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_bola_energia_2.png"),
        ],
        'poder_ligero': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_bola.png"),
        'kamehameha': cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_kamehameha.png"),
        'kamehameha_poder' : [
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Kamehameha_inicio.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Kamehameha_cuerpo.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Kamehameha_final.png"),
        ],
        'genki_pose' : [ 
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_1.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_2.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_3.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_4.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_5.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genki_6.png"),
        ],
        'genkidama' : cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_Genkidama.png"),
        'aturdido' : cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_aturdido.png"),
        'ko' : [
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_KO_1.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Goku/Goku_KO_2.png"),
        ],
    }

    sprites_vegeta = {
        'derecha' :  cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_avanza.png"),
        'izquierda' :  cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_retrocede.png"),
        'bajar' : cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_baja.png"),
        'subir': cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_sube.png"),
        'inicio' : cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_base.png"),
        'golpe_j' : [
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_golpe_puño_derecho.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_golpe_puño_izquierdo.png"),
        ],
        'patada_k' : [
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_patada_1.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_patada_2.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_patada_3.png"),
        ],
        'cubrirse' : cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_cubrirse.png"),
        'bola_energia' : [
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_bola_energia_1.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_bola_energia_2.png"),
        ],
        'poder_ligero' : cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_bola.png"),
        'galick_gun' : [
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_galick_gun_1.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_galick_gun_2.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_galick_gun_3.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_galick_gun_4.png"),
        ],
        'galick_gun_poder' : cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/galick_gun_final.png"),
        'aturdido' : cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_aturdido.png"),
        'ko' : [
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_KO_1.png"),
            cargar_imagen_con_alpha("Assets/Sprites/Vegeta_1/Vegeta_KO_2.png"),
        ],
    }

    sprites_freezer1 = {
        'derecha': cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_avanza.png"),
        'izquierda': cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_retrocede.png"),
        'subir': cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_sube-baja.png"),
        'bajar': cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_sube-baja.png"),
        'inicio': cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_inicio.png"),
        'golpe_j': [
            cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_golpe_puño_izquierdo.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_golpe_puño_derecho.png"),
            ],
        'patada_k': [cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_patada.png")],
        'cubrirse': cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_cubrirse.png"),
        'poder_ligero' : cargar_imagen_con_alpha("Assets/Sprites/Freezer_1/Freezer_bola.png"),
        'bola_energia' : [cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_bola_energia.png")],
        'kamehameha' : cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_kamehameha.png"),
        'kamehameha_poder' : [
            cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_kamehameha_inico.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_kamehameha_final.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_kamehameha_inico.png"),
            ],
        'Ulti' : [
            cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_Ulti_1.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_Ulti_2.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_Ulti_3.png"),
            ],
        'Ulti_poder' : cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Bola_maligna.png"),
        'aturdido' : cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_aturdido.png"),
        'ko' : [
            cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_KO_1.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/Freezer_1/Freezer1_KO_2.png"),
        ],
    
    }

    sprites_gohan2 = {
        'derecha': cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_avanza.png"),
        'izquierda': cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_retrocede.png"),
        'bajar': cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_sube-baja.png"),
        'inicio': cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_inicio.png"),
        'golpe_j': [
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_puño_izquierdo.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_puño_derecho.png"),
        ],
        'patada_k': [
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_patada_1.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_patada_2.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_patada_3.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_patada_4.png"),
            ],
        'cubrirse': cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_cubrirse.png"),
        # CORRECCIÓN: Cambiar 'poder_ligero' a imagen simple y 'bola_energia' a lista
        'poder_ligero' : cargar_imagen_con_alpha("Assets/Sprites/GohanSSJ_1/Goku_bola.png"),
        'bola_energia' : [
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_bola_energia_1.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_bola_energia_2.png"),
        ],
        'kamehameha' : cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_kamehameha.png"),
        'kamehameha_poder' : [
            cargar_imagen_con_alpha("Assets/Sprites/GohanSSJ_1/kamehameha_inicio.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/kamehameha_cuerpo.png"),
            cargar_imagen_con_alpha("Assets/Sprites/GohanSSJ_1/kamehameha_final.png"),
        ],
        'masenko' : [
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_masenko_1.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_masenko_2.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_masenko_3.png"),
        ],
        'masenko_poder' : cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/Masenko.png"),
        'aturdido' : cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_aturdido.png"),
        'ko' : [
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_KO_1.png"),
            cargar_imagen_transparente_con_blanco("Assets/Sprites/GohanSSJ_1/GohankidSSJ_KO_2.png"),
        ],

    }

    personajes_data = [
        {
            "id": "goku",  
            "nombre": "Goku",
            "foto_seleccion": "Assets/Sprites/Goku/Goku_seleccion.png",
            "lore": "Un saiyajin criado en la Tierra, defensor incansable de sus seres queridos."
        },
        {
            "id": "vegeta",
            "nombre": "Vegeta",
            "foto_seleccion": "Assets/Sprites/Vegeta_1/Vegeta_seleccion.png",
            "lore": "Príncipe de los saiyajines, inicialmente un rival feroz de Goku, luego un aliado valioso."
        },
        {
            "id": "freezer",
            "nombre": "Freezer",
            "foto_seleccion": "Assets/Sprites/Freezer_1/Freezer1_seleccion.png",
            "lore": "Conquistador del universo y rival mortal de Goku y los guerreros Z."
        },
        {
            "id": "gohan",
            "nombre": "Gohan",
            "foto_seleccion": "Assets/Sprites/GohanSSJ_1/GohankidSSJ_seleccion.png",
            "lore": "Hijo mayor de Goku, combina gran poder con un corazón noble."
        },
    ]

    return sprites_goku1, sprites_vegeta, sprites_freezer1, sprites_gohan2, personajes_data