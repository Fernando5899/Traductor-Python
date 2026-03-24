import speech_recognition as sr
import whisper
import pyttsx3
import os
import warnings
from deep_translator import GoogleTranslator

# Ignoramos advertencias de Whisper
warnings.filterwarnings("ignore", category=UserWarning)

# El Diccionario Definitivo de Whisper
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


def configurar_voz():
    motor = pyttsx3.init()
    motor.setProperty('rate', 150)
    return motor


def escuchar_y_detectar_local():
    # Como ya se descargó la primera vez, esto será súper rápido
    modelo = whisper.load_model("base")
    reconocedor = sr.Recognizer()
    motor_voz = configurar_voz()

    archivo_temporal = "audio_temp.wav"

    with sr.Microphone() as fuente:
        print("\n🎤 Ajustando al ruido de fondo... un segundo...")
        reconocedor.adjust_for_ambient_noise(fuente, duration=1)

        # Le damos 2 segundos de paciencia para que no te corte si respiras o haces una pausa
        reconocedor.pause_threshold = 2.0

        print("🟢 ¡Ya puedes hablar!")
        try:
            # Quitamos el phrase_time_limit.
            # El timeout=10 solo es el tiempo máximo que esperará para que EMPIECES a hablar.
            audio = reconocedor.listen(fuente, timeout=10)

            with open(archivo_temporal, "wb") as f:
                f.write(audio.get_wav_data())

            print("🧠 Analizando el audio en tu computadora...")

            # Whisper hace la magia local
            resultado = modelo.transcribe(archivo_temporal, fp16=False)
            texto_capturado = resultado["text"].strip()
            codigo_idioma = resultado["language"]

            print(f"📝 Transcripción cruda: '{texto_capturado}'")

            idioma_espanol = NOMBRES_IDIOMAS.get(codigo_idioma.lower(), codigo_idioma)

            # TRADUCTOR CORREGIDO: Adaptamos el código de Whisper para que Google Translate lo entienda
            codigo_traductor = codigo_idioma.lower()

            # Si Whisper detecta Chino general, lo forzamos a Chino Simplificado para Google
            if codigo_traductor == 'zh':
                codigo_traductor = 'zh-CN'

            try:
                texto_traducido = GoogleTranslator(source=codigo_traductor, target='es').translate(texto_capturado)
            except:
                texto_traducido = GoogleTranslator(source='auto', target='es').translate(texto_capturado)

            print(f"🌍 Significado en español: '{texto_traducido}'")

            mensaje = f"El idioma detectado es {idioma_espanol}, y significa: {texto_traducido}."
            print(f"✅ {mensaje}")

            print("🔊 Generando voz offline...")
            motor_voz.say(mensaje)
            motor_voz.runAndWait()

        except sr.WaitTimeoutError:
            print("❌ No escuché a nadie hablar. Intenta de nuevo.")
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")
        finally:
            if os.path.exists(archivo_temporal):
                os.remove(archivo_temporal)


if __name__ == "__main__":
    escuchar_y_detectar_local()