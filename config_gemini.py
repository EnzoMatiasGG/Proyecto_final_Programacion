GEMINI_API_KEY = ""

def obtener_api_key():
    """Retorna la API key configurada"""
    if not GEMINI_API_KEY or GEMINI_API_KEY == "":
        print("\n" + "="*60)
        print("  ADVERTENCIA: No hay API key de Gemini configurada")
        print("="*60)
        print(" Para activar Gemini AI en tu juego:")
        print("   1. entra a: https://aistudio.google.com/app/apikey")
        print("   2. Inicia sesión con tu cuenta de Google")
        print("   3. Hace clic en 'Create API Key' (es GRATIS)")
        print("   4. Copia la API key que te genera")
        print("   5. Edita config_gemini.py y pegala en GEMINI_API_KEY")
        print("\n Mientras tanto, el juego usara la IA tradicional")
        print("="*60 + "\n")
        return None
    return GEMINI_API_KEY


def verificar_configuracion():
    """Verifica si la API key está configurada correctamente"""
    api_key = obtener_api_key()
    if api_key:
        print("API key de Gemini configurada correctamente")
        print(f" Key: {api_key[:20]}..." + "*" * 20)
        return True
    else:
        print(" API key de Gemini NO configurada")
        return False