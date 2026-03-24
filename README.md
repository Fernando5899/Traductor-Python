# 🧠 Traductor Inteligente Local con IA (Whisper)

Este proyecto es un **traductor de voz a voz completamente local** (*hands-free*), diseñado para ofrecer traducciones fluidas y precisas sin depender de servicios en la nube. Utiliza el modelo **Whisper de OpenAI** para garantizar privacidad y velocidad de procesamiento en hardware local.

-----

## 📖 Descripción del Proyecto

A diferencia de las soluciones tradicionales, este sistema ejecuta redes neuronales directamente en tu equipo. Es ideal para entornos de desarrollo, aprendizaje de idiomas o como asistente personal de traducción.

### **Versiones Disponibles:**

  * **`detector_3.py` (Básico):** Realiza una traducción y termina.
  * **`deteccion_4.py` (Híbrido):** Traducción continua con confirmación por **teclado** (`si/no`).
  * **`deteccion_5.py` (Hands-Free):** Traducción continua con confirmación por **voz**. El sistema te pregunta y tú respondes hablando.

-----

## ✨ Características Principales

  * **IA Local:** Procesamiento sin latencia de red y con total privacidad.
  * **Soporte Multilingüe:** Capacidad para identificar y traducir más de **90 idiomas**.
  * **Modo Hands-Free:** Interacción controlada totalmente por comandos de voz.
  * **Ajuste de Ruido:** Calibración automática de ambiente para mayor precisión.
  * **Gestión de Hardware:** Optimización del motor de voz para evitar conflictos con el micrófono.

-----

## 🛠️ Requisitos Previos (System Requirements)

Antes de instalar las librerías de Python, es obligatorio configurar estas herramientas en Windows:

### 1\. FFmpeg (Procesamiento de Audio)

Es el motor que Whisper utiliza para leer tus grabaciones.

  * **Instalación rápida:** Abre PowerShell como administrador y ejecuta:
    ```bash
    winget install ffmpeg
    ```
  * ⚠️ **IMPORTANTE:** Una vez instalado, **debes cerrar y volver a abrir Visual Studio Code y tu terminal** para que Windows reconozca los cambios. Si no lo haces, el programa dirá que no encuentra FFmpeg.

### 2\. Visual Studio Build Tools (Compilador C++)

Necesario para que la librería `PyAudio` pueda compilarse.

  * **Descarga oficial:** [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
  * **Instrucciones:** Al ejecutar el instalador, marca la casilla **"Desarrollo para el escritorio con C++"** (Desktop development with C++). Sin esto, la instalación de las librerías de Python fallará.

-----

## ⚙️ Instalación y Configuración

Sigue estos pasos para preparar tu entorno (son los mismos para cualquier versión del script):

### 1\. Clonar el repositorio

```bash
git clone https://github.com/Fernando5899/Traductor-Python.git
cd Traductor-Python
```

### 2\. Crear y activar el entorno virtual

Usa **Python 3.12.10** para asegurar compatibilidad total:

```bash
# Crear entorno
python -m venv .venv

# Activar en Windows
.\.venv\Scripts\activate
```

### 3\. Instalar Dependencias

```bash
pip install openai-whisper SpeechRecognition pyttsx3 deep-translator setuptools
```

-----

## 🚀 Uso del Programa

Dependiendo de qué nivel de automatización prefieras, corre cualquiera de estos comandos:

```bash
# Versión sencilla
python detector_3.py

# Versión con confirmación por teclado
python deteccion_4.py

# Versión 100% voz (Recomendado)
python deteccion_5.py
```

> **Nota:** En la primera ejecución, se descargará el modelo **"base"** de Whisper (\~140MB). Esto solo ocurre una vez.

-----

## 👨‍💻 Autor

**Fernando Jose Reynosa Vidal**

  * Estudiante de Ingeniería en Sistemas Computacionales.
  * **Universidad Tres Culturas (UTC)**.
  * GitHub: [Fernando5899](https://github.com/Fernando5899)

-----