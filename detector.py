import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import os
from playsound import playsound

# Nuestro diccionario para cumplir el requerimiento
NOMBRES_IDIOMAS = {
    'en': 'Inglés', 'es': 'Español', 'fr': 'Francés', 'de': 'Alemán',
    'it': 'Italiano', 'pt': 'Portugués', 'zh-cn': 'Chino', 'ja': 'Japonés',
    'haw': 'Hawaiano', 'ko': 'Coreano', 'ru': 'Ruso', 'sv': 'Sueco'
}


def hablar_resultado(texto):
    print("🔊 Generando voz...")
    # Creamos el audio en español
    tts = gTTS(text=texto, lang='es')
    archivo = "respuesta.mp3"
    tts.save(archivo)

    # Reproducimos el audio por las bocinas
    playsound(archivo)

    # Limpiamos nuestra basura (borramos el archivo temporal)
    os.remove(archivo)


def escuchar_y_detectar():
    reconocedor = sr.Recognizer()
    traductor = Translator()

    with sr.Microphone() as fuente:
        print("\n🎤 Ajustando al ruido de fondo... un segundo...")
        reconocedor.adjust_for_ambient_noise(fuente, duration=1)

        print("🟢 ¡Ya puedes hablar! Intenta decir algo en INGLÉS para esta prueba...")
        try:
            audio = reconocedor.listen(fuente, timeout=5, phrase_time_limit=10)
            print("⏳ Procesando el audio en la nube, espera un momento...")

            # 1. Convertimos a texto
            texto_capturado = reconocedor.recognize_google(audio)
            print(f"📝 Texto original: '{texto_capturado}'")

            # 2. Detectamos el idioma
            deteccion = traductor.detect(texto_capturado)
            codigo_idioma = deteccion.lang.lower()
            idioma_espanol = NOMBRES_IDIOMAS.get(codigo_idioma, codigo_idioma)

            # 3. ¡LA MAGIA NUEVA! Traducimos el texto al español
            traduccion = traductor.translate(texto_capturado, dest='es')
            texto_traducido = traduccion.text
            print(f"🌍 Traducción al español: '{texto_traducido}'")

            # 4. Armamos el mensaje final y lo hablamos
            mensaje = f"El idioma detectado es {idioma_espanol}, y en español significa: {texto_traducido}."
            print(f"✅ {mensaje}")

            hablar_resultado(mensaje)

        except sr.WaitTimeoutError:
            print("❌ No escuché a nadie hablar. Intenta de nuevo.")
        except sr.UnknownValueError:
            print("❌ Escuché algo, pero el modelo en inglés no logró entenderlo.")
        except Exception as e:
            print(f"❌ Ocurrió un error inesperado: {e}")


if __name__ == "__main__":
    escuchar_y_detectar()
