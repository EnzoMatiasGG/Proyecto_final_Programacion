# Sistema de Inteligencia Artificial potenciado por Gemini
# Controlador avanzado que usa la API de Google Gemini para tomar decisiones estrategicas

import pygame
import random
import requests
import json
from typing import Literal, Optional, Dict, Any
from src.entities.player import Player
from src.systems.ai import AIController

DificultadType = Literal["facil", "normal", "dificil"]


class GeminiAIController :
    """Controlador de IA potenciado por Google Gemini"""
    
    def __init__(self, jugador_ia : Player, jugador_oponente : Player, dificultad : DificultadType = "normal", api_key : Optional[str] = None) :
        """Inicializa el controlador de IA con Gemini"""
        self.jugador_ia = jugador_ia
        self.jugador_oponente = jugador_oponente
        self.dificultad = dificultad
        self.api_key = api_key
        
        # Fallback a IA tradicional si no hay API key
        self.ai_tradicional = AIController(jugador_ia, jugador_oponente, dificultad)
        self.usar_gemini = api_key is not None and len(api_key) > 0
        
        # Estado interno
        self.ultimo_llamado_gemini = 0
        self.intervalo_gemini = self._obtener_intervalo_por_dificultad()
        self.ultima_decision = None
        self.contador_decisiones = 0
        
        # Historial de combate 
        self.historial_combate = []
        self.max_historial = 5
        
        # URL de la API de Gemini
        if self.usar_gemini :
            self.api_url = f"https ://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash :generateContent?key={self.api_key}"
        
        print(f"🤖 Gemini AI {"ACTIVADO" if self.usar_gemini else "DESACTIVADO (usando IA tradicional)"}")
    
    def _obtener_intervalo_por_dificultad(self) -> int :
        """Determina con que frecuencia consultar a Gemini segun dificultad"""
        intervalos = {
            "facil" : 1500,    # Consulta cada 1.5 segundos
            "normal" : 800,    # Consulta cada 0.8 segundos
            "dificil" : 400    # Consulta cada 0.4 segundos
        }
        return intervalos.get(self.dificultad, 800)
    
    def actualizar(self) :
        """Logica principal del controlador"""
        if not self.usar_gemini :
            # Usar IA tradicional si Gemini no esta disponible
            self.ai_tradicional.actualizar()
            return
        
        ahora = pygame.time.get_ticks()
        
        # Verificar si el jugador esta bloqueado
        if self._esta_bloqueado() :
            return
        
        # Decidir si consultar a Gemini o ejecutar ultima decision
        if ahora - self.ultimo_llamado_gemini > self.intervalo_gemini :
            self._consultar_gemini(ahora)
        elif self.ultima_decision :
            self._ejecutar_decision(self.ultima_decision)
        else :
            # Comportamiento basico mientras espera decision
            self.ai_tradicional.actualizar()
    
    def _esta_bloqueado(self) -> bool :
        """Verifica si la IA esta en un estado bloqueante"""
        return any([
            self.jugador_ia.golpe_animando,
            self.jugador_ia.lanzando_bola,
            self.jugador_ia.usando_kamehameha,
            self.jugador_ia.usando_movimiento_final,
            self.jugador_ia.aturdido,
            self.jugador_ia.en_ko
        ])
    
    def _obtener_estado_juego(self) -> Dict[str, Any] :
        """Obtiene el estado actual del juego para enviar a Gemini"""
        distancia_x = abs(self.jugador_ia.x - self.jugador_oponente.x)
        distancia_y = abs(self.jugador_ia.y - self.jugador_oponente.y)
        
        return {
            "mi_vida" : round(self.jugador_ia.vida_actual, 1),
            "mi_vida_max" : self.jugador_ia.vida_maxima,
            "mi_energia" : round(self.jugador_ia.stamina_actual, 1),
            "mi_energia_max" : self.jugador_ia.stamina_maxima,
            "mi_posicion_x" : round(self.jugador_ia.x, 1),
            "mi_posicion_y" : round(self.jugador_ia.y, 1),
            "oponente_vida" : round(self.jugador_oponente.vida_actual, 1),
            "oponente_vida_max" : self.jugador_oponente.vida_maxima,
            "oponente_energia" : round(self.jugador_oponente.stamina_actual, 1),
            "oponente_posicion_x" : round(self.jugador_oponente.x, 1),
            "oponente_posicion_y" : round(self.jugador_oponente.y, 1),
            "distancia_x" : round(distancia_x, 1),
            "distancia_y" : round(distancia_y, 1),
            "oponente_atacando" : self.jugador_oponente.golpe_animando,
            "oponente_cubierto" : self.jugador_oponente.cubriendose,
            "mirando_derecha" : self.jugador_ia.mirando_derecha,
            "dificultad" : self.dificultad
        }
    
    def _crear_prompt(self, estado : Dict[str, Any]) -> str :
        """Crea el prompt para enviar a Gemini"""
        prompt = f"""Eres una IA experta en juegos de pelea de Dragon Ball Z. Debes decidir la MEJOR accion tactica para ganar.

ESTADO ACTUAL :
- Tu vida : {estado["mi_vida"]}/{estado["mi_vida_max"]} ({round(estado["mi_vida"]/estado["mi_vida_max"]*100)}%)
- Tu energia : {estado["mi_energia"]}/{estado["mi_energia_max"]} ({round(estado["mi_energia"]/estado["mi_energia_max"]*100)}%)
- Vida oponente : {estado["oponente_vida"]}/{estado["oponente_vida_max"]} ({round(estado["oponente_vida"]/estado["oponente_vida_max"]*100)}%)
- Energia oponente : {estado["oponente_energia"]}
- Distancia horizontal : {estado["distancia_x"]} pixeles
- Distancia vertical : {estado["distancia_y"]} pixeles
- Oponente atacando : {"Si" if estado["oponente_atacando"] else "NO"}
- Oponente defendiendo : {"Si" if estado["oponente_cubierto"] else "NO"}
- Dificultad : {estado["dificultad"]}

ACCIONES DISPONIBLES :
1. "acercarse" - Moverse hacia el oponente (util si distancia > 150)
2. "alejarse" - Retroceder del oponente (util si distancia < 50 o necesitas recuperar)
3. "golpe" - Golpe basico (rapido, bajo daño, costo : 5 energia, rango : 80px)
4. "patada" - Patada (medio daño, costo : 8 energia, rango : 80px)
5. "defender" - Bloquear ataques (reduce 70% daño)
6. "bola_energia" - Proyectil (medio daño, costo : 15 energia, rango : ilimitado)
7. "kamehameha" - Ataque potente (alto daño, costo : 50 energia, rango : ilimitado)
8. "movimiento_final" - Ataque definitivo (muy alto daño, costo : 80 energia, rango : 150px)
9. "esperar" - No hacer nada (recuperar stamina pasivamente)

ESTRATEGIA SEGUN SITUACION :
- Si distancia > 200 : acercarse o usar bola_energia
- Si distancia 80-200 : bola_energia o acercarse
- Si distancia < 80 : golpe, patada, o defender si oponente ataca
- Si distancia < 50 : alejarse si vida baja, o atacar si vida alta
- Si oponente ataca y distancia < 100 : defender
- Si tu vida < 30% y energia alta : usar kamehameha o movimiento_final
- Si energia < 20 : acercarse, golpe, o esperar
- En dificultad "dificil" : se mas agresivo y usa combos

Responde SOLO con un objeto JSON (sin markdown) :
{{"accion" : "nombre_accion", "razon" : "explicacion breve"}}"""
        
        return prompt
    
    def _consultar_gemini(self, ahora : int) :
        """Consulta a Gemini para obtener la siguiente accion"""
        try :
            estado = self._obtener_estado_juego()
            prompt = self._crear_prompt(estado)
            
            # Preparar request
            payload = {
                "contents" : [{
                    "parts" : [{
                        "text" : prompt
                    }]
                }],
                "generationConfig" : {
                    "temperature" : 0.7,
                    "maxOutputTokens" : 150,
                }
            }
            
            # Hacer request a Gemini
            response = requests.post(
                self.api_url,
                headers={"Content-Type" : "application/json"},
                json=payload,
                timeout=2)  # Timeout corto para no pausar el juego
            
            if response.status_code == 200 :
                result = response.json()
                texto_respuesta = result["candidates"][0]["content"]["parts"][0]["text"]
                
                # Limpiar respuesta 
                texto_respuesta = texto_respuesta.strip()
                if texto_respuesta.startswith("```json") :
                    texto_respuesta = texto_respuesta.replace("```json", "").replace("```", "").strip()
                elif texto_respuesta.startswith("```") :
                    texto_respuesta = texto_respuesta.replace("```", "").strip()
                
                decision = json.loads(texto_respuesta)
                self.ultima_decision = decision
                self.ultimo_llamado_gemini = ahora
                self.contador_decisiones += 1
                
                # Debug
                if self.contador_decisiones % 10 == 0 :
                    print(f"🧠 Gemini decidio : {decision["accion"]} - {decision.get("razon", "")}")
                
            else :
                print(f"⚠️ Error API Gemini : {response.status_code}")
                self._usar_fallback()
                
        except requests.exceptions.Timeout :
            # Timeout - usar IA tradicional esta vez
            self._usar_fallback()
        except Exception as e :
            print(f"⚠️ Error consultando Gemini : {e}")
            self._usar_fallback()
    
    def _ejecutar_decision(self, decision : Dict[str, Any]) :
        """Ejecuta la decision tomada por Gemini"""
        accion = decision.get("accion", "esperar")
        
        if accion == "acercarse" :
            self._acercarse_al_oponente()
        elif accion == "alejarse" :
            self._alejarse_del_oponente()
        elif accion == "golpe" :
            if self.jugador_ia.tiene_stamina(5) :
                self.jugador_ia.iniciar_golpe("golpe_j")
        elif accion == "patada" :
            if self.jugador_ia.tiene_stamina(8) :
                self.jugador_ia.iniciar_golpe("patada_k")
        elif accion == "defender" :
            self.jugador_ia.cubrirse()
        elif accion == "bola_energia" :
            if self.jugador_ia.tiene_stamina(15) :
                self.jugador_ia.iniciar_lanzar_bola()
        elif accion == "kamehameha" :
            if self.jugador_ia.tiene_stamina(50) :
                self.jugador_ia.iniciar_kamehameha()
        elif accion == "movimiento_final" :
            if self.jugador_ia.tiene_stamina(80) :
                self.jugador_ia.iniciar_movimiento_final()
        elif accion == "esperar" :
            # No hacer nada, recuperar stamina
            self.jugador_ia.estado = "inicio"
            self.jugador_ia.sprite = self.jugador_ia.sprites["inicio"]
    
    def _acercarse_al_oponente(self) :
        """Se acerca al oponente"""
        velocidad = 3.5
        if self.jugador_ia.x < self.jugador_oponente.x :
            self.jugador_ia.x += velocidad
            self.jugador_ia.estado = "derecha" if self.jugador_ia.mirando_derecha else "izquierda"
        else :
            self.jugador_ia.x -= velocidad
            self.jugador_ia.estado = "izquierda" if self.jugador_ia.mirando_derecha else "derecha"
        
        self.jugador_ia.sprite = self.jugador_ia.sprites[self.jugador_ia.estado]
    
    def _alejarse_del_oponente(self) :
        """Se aleja del oponente"""
        velocidad = 4.0
        if self.jugador_ia.x < self.jugador_oponente.x :
            self.jugador_ia.x -= velocidad
            self.jugador_ia.estado = "izquierda" if self.jugador_ia.mirando_derecha else "derecha"
        else :
            self.jugador_ia.x += velocidad
            self.jugador_ia.estado = "derecha" if not self.jugador_ia.mirando_derecha else "izquierda"
        
        self.jugador_ia.sprite = self.jugador_ia.sprites[self.jugador_ia.estado]
    
    def _usar_fallback(self) :
        """Usa la IA tradicional como respaldo"""
        self.ai_tradicional.actualizar()