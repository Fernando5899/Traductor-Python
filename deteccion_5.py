import speech_recognition as sr
import whisper
import pyttsx3
import os
import warnings
from deep_translator import GoogleTranslator

# Ignoramos advertencias de Whisper
warnings.filterwarnings("ignore", category=UserWarning)

# El Diccionario Definitivo
NOMBRES_IDIOMAS = {
    "en": "Inglés", "zh": "Chino", "de": "Alemán", "es": "Español", "ru": "Ruso",
    "ko": "Coreano", "fr": "Francés", "ja": "Japonés", "pt": "Portugués", "tr": "Turco",
    "pl": "Polaco", "ca": "Catalán", "nl": "Neerlandés", "ar": "Árabe", "sv": "Sueco",
    "it": "Italiano", "id": "Indonesio", "hi": "Hindi", "fi": "Finlandés", "vi": "Vietnamita",
    "he": "Hebreo", "uk": "Ucraniano", "el": "Griego", "ms": "Malayo", "cs": "Checo",
    "ro": "Rumano", "da": "Danés", "hu": "Húngaro", "ta": "Tamil", "no": "Noruego",
    "th": "Tailandés", "ur": "Urdu", "hr": "Croata", "bg": "Búlgaro", "lt": "Lituano",
    "la": "Latín", "mi": "Maorí", "ml": "Malayalam", "cy": "Galés", "sk": "Eslovaco",
    "te": "Telugu", "fa": "Persa", "lv": "Letón", "bn": "Bengalí", "sr": "Serbio",
    "az": "Azerbaiyano", "sl": "Esloveno", "kn": "Canarés", "et": "Estonio", "mk": "Macedonio",
    "br": "Bretón", "eu": "Euskera", "is": "Islandés", "hy": "Armenio", "ne": "Nepalí",
    "mn": "Mongol", "bs": "Bosnio", "kk": "Kazajo", "sq": "Albanés", "sw": "Suajili",
    "gl": "Gallego", "mr": "Marathi", "pa": "Punyabí", "si": "Cingalés", "km": "Jemer",
    "sn": "Shona", "yo": "Yoruba", "so": "Somalí", "af": "Afrikáans", "oc": "Occitano",
    "ka": "Georgiano", "be": "Bielorruso", "tg": "Tayiko", "sd": "Sindhi", "gu": "Guyaratí",
    "am": "Amárico", "yi": "Yidis", "lo": "Lao", "uz": "Uzbeko", "fo": "Feroés",
    "ht": "Haitiano", "ps": "Pastún", "tk": "Turcomano", "nn": "Nynorsk", "mt": "Maltés",
    "sa": "Sánscrito", "lb": "Luxemburgués", "my": "Birmano", "bo": "Tibetano", "tl": "Tagalo",
    "mg": "Malgache", "as": "Asamés", "tt": "Tártaro", "haw": "Hawaiano", "ln": "Lingala",
    "ha": "Hausa", "ba": "Baskir", "jw": "Javanés", "su": "Sudanés"
}


def hablar_texto(texto):
    """Mini-función aislada para hablar sin trabar el micrófono"""
    motor = pyttsx3.init()
    motor.setProperty('rate', 150)
    for voz in motor.getProperty('voices'):
        if 'es' in voz.id.lower() or 'spanish' in voz.name.lower() or 'sabina' in voz.name.lower():
            motor.setProperty('voice', voz.id)
            break
    motor.say(texto)
    motor.runAndWait()


def preguntar_continuar(modelo, reconocedor):
    """Función que usa Whisper para escuchar tu respuesta de 'sí' o 'no'"""
    print("\n=============================================")
    print("❓ Esperando tu confirmación para continuar...")
    hablar_texto("¿Deseas traducir otra frase?")

    archivo_resp = "respuesta_temp.wav"
    with sr.Microphone() as fuente:
        reconocedor.adjust_for_ambient_noise(fuente, duration=0.5)
        print("🎤 Responde 'sí' o 'no' (¡en cualquier idioma!)...")
        try:
            # Solo te damos 5 segundos para responder (es una respuesta rápida)
            audio = reconocedor.listen(fuente, timeout=5, phrase_time_limit=4)

            with open(archivo_resp, "wb") as f:
                f.write(audio.get_wav_data())

            # Whisper procesa tu respuesta
            resultado = modelo.transcribe(archivo_resp, fp16=False)
            texto_original = resultado["text"].strip()
            codigo_idioma = resultado["language"].lower()

            # Traducimos lo que respondiste a español para evaluarlo
            codigo_traductor = 'zh-CN' if codigo_idioma == 'zh' else codigo_idioma
            try:
                texto_traducido = GoogleTranslator(source=codigo_traductor, target='es').translate(
                    texto_original).lower()
            except:
                texto_traducido = GoogleTranslator(source='auto', target='es').translate(texto_original).lower()

            print(f"🗣️ Entendí tu respuesta: '{texto_original}' -> Que significa: '{texto_traducido}'")

            # Palabras clave para apagar el programa
            negativas = ['no', 'parar', 'detener', 'salir', 'basta', 'fin', 'terminar', 'suficiente']

            for palabra in negativas:
                if palabra in texto_traducido:
                    return False

            # Si respondiste "sí" u otra cosa afirmativa, continuamos
            return True

        except sr.WaitTimeoutError:
            print("⏳ No respondiste nada. Asumiré que terminamos por hoy.")
            return False
        except Exception as e:
            print(f"❌ Error al escuchar tu respuesta: {e}")
            return False
        finally:
            if os.path.exists(archivo_resp):
                os.remove(archivo_resp)


def escuchar_y_detectar_local():
    print("⏳ Cargando el cerebro de la Inteligencia Artificial (Whisper)...")
    modelo = whisper.load_model("base")
    reconocedor = sr.Recognizer()
    archivo_temporal = "audio_temp.wav"

    while True:
        with sr.Microphone() as fuente:
            print("\n=============================================")
            print("🎤 Ajustando al ruido de fondo... un segundo...")
            reconocedor.adjust_for_ambient_noise(fuente, duration=1)
            reconocedor.pause_threshold = 2.0

            print("🟢 ¡Ya puedes hablar! Te estoy escuchando...")
            try:
                audio = reconocedor.listen(fuente, timeout=10)

                with open(archivo_temporal, "wb") as f:
                    f.write(audio.get_wav_data())

                print("🧠 Analizando el audio en tu computadora...")

                resultado = modelo.transcribe(archivo_temporal, fp16=False)
                texto_capturado = resultado["text"].strip()
                codigo_idioma = resultado["language"]

                print(f"📝 Transcripción cruda: '{texto_capturado}'")

                idioma_espanol = NOMBRES_IDIOMAS.get(codigo_idioma.lower(), codigo_idioma)

                codigo_traductor = codigo_idioma.lower()
                if codigo_traductor == 'zh':
                    codigo_traductor = 'zh-CN'

                try:
                    texto_traducido = GoogleTranslator(source=codigo_traductor, target='es').translate(texto_capturado)
                except:
                    texto_traducido = GoogleTranslator(source='auto', target='es').translate(texto_capturado)

                print(f"✅ Idioma detectado: {idioma_espanol}")
                print(f"🌍 Significado en español: '{texto_traducido}'")

                print("🔊 Generando voz offline...")
                hablar_texto(texto_traducido)

            except sr.WaitTimeoutError:
                print("❌ No escuché a nadie hablar.")
            except Exception as e:
                print(f"❌ Ocurrió un error inesperado: {e}")
            finally:
                if os.path.exists(archivo_temporal):
                    os.remove(archivo_temporal)

        # --- PREGUNTA CON VOZ (¡Adiós teclado!) ---
        if not preguntar_continuar(modelo, reconocedor):
            mensaje_despedida = "Apagando el traductor. ¡Hasta pronto!"
            print(f"\n🛑 {mensaje_despedida}")
            hablar_texto(mensaje_despedida)
            break


if __name__ == "__main__":
    escuchar_y_detectar_local()