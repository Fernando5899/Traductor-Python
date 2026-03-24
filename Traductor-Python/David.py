import speech_recognition as sr
from deep_translator import GoogleTranslator
from langdetect import detect
from colorama import Fore, Style, init
import sys

# Inicializar colores y UTF-8 para el CMD
init(autoreset=True)
sys.stdout.reconfigure(encoding='utf-8')

IDIOMAS_TOTALES = {
    'en': 'Inglés', 'ja': 'Japonés', 'fr': 'Francés', 'de': 'Alemán',
    'it': 'Italiano', 'pt': 'Portugués', 'ru': 'Ruso', 'zh-CN': 'Chino',
    'ko': 'Coreano', 'ar': 'Árabe'
}



def obtener_mejor_transcripcion(recognizer, audio):
    """
    Intenta reconocer el audio en Japonés y Español,
    devolviendo la que tenga sentido fonético.
    """
    try:
        # Intentamos primero Japonés (es el más sensible a errores)
        texto_ja = recognizer.recognize_google(audio, language='ja-JP')
        # Si el texto contiene caracteres japoneses, lo priorizamos
        if any(ord(c) > 12000 for c in texto_ja):
            return texto_ja, 'ja'
    except:
        pass

    try:
        # Si no fue japonés claro, usamos Español/Inglés (es-MX capta nombres como David)
        texto_es = recognizer.recognize_google(audio, language='es-MX')
        return texto_es, 'auto'
    except:
        return None, None


def traductor_v3():
    recognizer = sr.Recognizer()

    with sr.Microphone() as source:
        print(f"\n{Fore.CYAN}{'=' * 50}")
        print(f"{Fore.WHITE}          TRADUCTOR UNIVERSAL (AUTO-DETECCIÓN)")
        print(f"{Fore.CYAN}{'=' * 50}")

        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print(f"{Fore.GREEN}>>> ESCUCHANDO... (Habla en cualquier idioma)")

        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=15)
            print(f"{Fore.MAGENTA}>>> Analizando fonética...")

            texto_crudo, hint = obtener_mejor_transcripcion(recognizer, audio)

            if not texto_crudo:
                print(f"{Fore.RED}>>> No se detectó voz clara.")
                return

            # Detección precisa de idioma
            try:
                cod_detectado = detect(texto_crudo)
            except:
                cod_detectado = 'es'

            # --- INTERFAZ VISUAL LIMPIA ---
            print(f"\n{Fore.WHITE}ORIGEN: {Fore.BLUE}{cod_detectado.upper()}")
            print(f"{Fore.WHITE}TEXTO : {Fore.YELLOW}{texto_crudo}")

            # Significado en Español (siempre se muestra)
            if cod_detectado != 'es':
                traduccion_es = GoogleTranslator(source='auto', target='es').translate(texto_crudo)
                print(f"{Fore.WHITE}TRAD  : {Fore.GREEN}{traduccion_es}")

            print(f"{Fore.CYAN}{'-' * 50}")

            # Opción rápida de multi-idioma
            opcion = input(f"{Fore.WHITE}¿Traducir a todos? {Fore.CYAN}(s/n): ").lower()

            if opcion == 's':
                print(f"\n{Fore.MAGENTA}--- TRADUCCIÓN MASIVA ---")
                for cod, nombre in IDIOMAS_TOTALES.items():
                    if cod != cod_detectado:
                        try:
                            t = GoogleTranslator(source='auto', target=cod).translate(texto_crudo)
                            print(f"{Fore.WHITE}{nombre:10} : {Fore.CYAN}{t}")
                        except:
                            continue
                print(f"{Fore.MAGENTA}{'-' * 25}")
                input(f"{Fore.GREEN}Enter para continuar...")

        except Exception as e:
            print(f"{Fore.RED}>>> Error del sistema: {e}")


if __name__ == "__main__":
    print(f"{Fore.RED}RECUERDA: Ejecuta 'chcp 65001' en tu CMD antes de iniciar.")
    while True:
        traductor_v3()