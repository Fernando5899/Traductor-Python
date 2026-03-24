import speech_recognition as sr
import whisper
import pyttsx3
import os
import warnings
from googletrans import Translator

# Ignoramos algunas advertencias inofensivas que a veces lanza Whisper
warnings.filterwarnings("ignore", category=UserWarning)

# Nuestro diccionario expandido
NOMBRES_IDIOMAS = {
    'en': 'Inglés', 'es': 'Español', 'fr': 'Francés', 'de': 'Alemán',
    'it': 'Italiano', 'pt': 'Portugués', 'zh': 'Chino', 'ja': 'Japonés',
    'ko': 'Coreano', 'ru': 'Ruso', 'sv': 'Sueco', 'ar': 'Árabe'
}


def configurar_voz():
    # Iniciamos el motor de voz nativo de Windows (100% offline)
    motor = pyttsx3.init()
    # Ajustamos la velocidad para que no hable tan rápido (200 es por defecto)
    motor.setProperty('rate', 150)
    return motor


def escuchar_y_detectar_local():
    print("⏳ Cargando el cerebro de la Inteligencia Artificial (Whisper)...")
    # Cargamos el modelo "base". La primera vez descargará unos ~74MB.
    modelo = whisper.load_model("base")
    reconocedor = sr.Recognizer()
    traductor = Translator()
    motor_voz = configurar_voz()

    archivo_temporal = "audio_temp.wav"

    with sr.Microphone() as fuente:
        print("\n🎤 Ajustando al ruido de fondo... un segundo...")
        reconocedor.adjust_for_ambient_noise(fuente, duration=1)

        print("🟢 ¡Ya puedes hablar! Intenta en CUALQUIER idioma (japonés, francés, alemán, español)...")
        try:
            # 1. Escuchar y guardar el audio crudo
            audio = reconocedor.listen(fuente, timeout=5, phrase_time_limit=10)

            with open(archivo_temporal, "wb") as f:
                f.write(audio.get_wav_data())

            print("🧠 Analizando el audio en tu computadora... esto puede tardar unos segundos...")

            # 2. Whisper detecta el idioma y transcribe (¡La verdadera magia!)
            resultado = modelo.transcribe(archivo_temporal, fp16=False)
            texto_capturado = resultado["text"].strip()
            codigo_idioma = resultado["language"]

            print(f"📝 Transcripción cruda: '{texto_capturado}'")

            # 3. Mapeo al español
            idioma_espanol = NOMBRES_IDIOMAS.get(codigo_idioma.lower(), codigo_idioma)

            # 4. Traducción al español (para que entiendas qué dijiste)
            traduccion = traductor.translate(texto_capturado, dest='es')
            texto_traducido = traduccion.text
            print(f"🌍 Significado en español: '{texto_traducido}'")

            # 5. Salida de texto y voz offline
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
            # Limpieza: Borramos el archivo temporal para no dejar basura en tu disco duro
            if os.path.exists(archivo_temporal):
                os.remove(archivo_temporal)


if __name__ == "__main__":
    escuchar_y_detectar_local()