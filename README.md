# Proyecto Final Programación 🐉

Juego 2D creado en Python

---

## Descripción 📖

Este es un juego 2D desarrollado en Python, basado en el universo de Dragon Ball.  
Incluye dos modos principales de juego:

- 🥊 **Modo clásico 1 vs 1** 🥊: enfrenta a dos personajes en batallas directas, al estilo de los clásicos juegos de lucha.
- 🏯 **Modo torre** 🏯: desafía una serie de combates consecutivos contra diferentes rivales, inspirado en el modo torre de Mortal Kombat, donde avanzarás hasta llegar al jefe final.

Los personajes tienen ataques especiales, animaciones fluidas y controles sencillos para que disfrutes de la experiencia de pelea tipo arcade.

---

## 🎮 Controles 🎮

- Movimiento: Flechas del teclado o WASD
- Ataque rápido: tecla J
- Patada/Combo: tecla K
- Cubrirse: tecla L
- Bola de energía: tecla I
- Kamehameha: tecla O
- Ulti: tecla P
- Pausa/Menu: tecla ESC

---

##  🛠️ Requisitos 🛠️

- Python 3.x
- Pygame

---

## ⚡ Instalación ⚡

1. Clona este repositorio:
```bash
git clone https://github.com/EnzoMatiasGG/Proyecto_final_Programacion.git
```


2. Instala la dependencia necesaria ejecutando:
```bash
pip install -r requirements.txt
```

3. Ejecutar el juego
```bash
python main.py
```

---

## 📂 Estructura del proyecto 📂
```bash
PROYECTOFINALPROGRA_1/
│
├── Data/
│ ├── records_torre.txt # Datos de records del modo torre
│ ├── recordsJson # (Carpeta o archivo, segun tu estructura)
│ └── records.txt # Datos adicionales de records
│
├── Fondos/ # Fondos graficos del juego
│
├── Fuentes/
│ └── PressStart2P.ttf # Fuente usada en menus y HUD
│
├── Sonidos/
│
├── Assets/
│ ├── Imagenes_especiales # Decoracion
│ └── Sprites # Imagenes de personajes y animaciones
│
├── src/ # Codigo fuente del juego
│ ├── core/
│ │ ├── init.py
│ │ └── game.py # Logica principal y motor del juego
│ ├── entities/
│ │ ├── init.py
│ │ ├── player.py # Control y logica del jugador
│ │ ├── proyectile.py # Logica de proyectiles
│ │ └── special_moves.py # Movimientos especiales y ataques unicos
│ ├── managers/
│ │ ├── audio_manager.py # Gestion del audio
│ │ ├── records_manager.py # Control de records y puntajes
│ │ ├── resource_manager.py # Administracion de recursos
│ │ └── tower_manager.py # Logica del modo torre
│ ├── systems/
│ │ ├── ui/
│ │ │ ├── hud.py # Interfaz HUD (vida, energia, etc.)
│ │ │ ├── menus.py # Pantallas y menus
│ │ │ ├── transitions.py # Efectos visuales de transicion
│ │ │ └── init.py
│ │ └── utils.py # Funciones auxiliares
│ ├── config_gemini.py # Configuraciones generales
│ └── main.py # Punto de entrada del programa
│
├── requirements.txt # Dependencias del proyecto
└── README
