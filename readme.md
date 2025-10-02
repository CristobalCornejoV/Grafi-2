# Conversor de Texto a Audio MP3 (Edge TTS) "GRAFI 2"

creado por: Cristóbal Cornejo V.

El presente proyecto es una aplicación de escritorio desarrollada en Python, diseñada para la conversión eficiente de documentos de texto (TXT, PDF, PPTX) a archivos de audio MP3 de alta fidelidad, utilizando la tecnología de síntesis de voz **Edge TTS (Microsoft Azure)**. La arquitectura del software se ha implementado rigurosamente bajo el patrón **Modelo-Vista-Controlador (MVC)**, garantizando una clara separación de responsabilidades y facilitando su mantenimiento y escalabilidad.

---

## 1. Requisitos del Sistema

La ejecución exitosa de esta aplicación requiere los siguientes componentes:

### 1.1 Entorno de Desarrollo
* **Python 3.12** o superior.

### 1.2 Dependencia Externa Crítica
* **FFmpeg (versión 8.0 o posterior):** Es fundamental para el procesamiento y la manipulación de flujos de audio. Su ejecutable debe estar accesible a través de la variable de entorno del sistema (`PATH`).

---

## 2. Instalación y Configuración

Siga los siguientes pasos para preparar y ejecutar el entorno de la aplicación.

### 2.1 Instalación de Módulos Python

Instale los módulos requeridos utilizando `pip`:

```bash
pip install tk tkinterdnd2 edge-tts PyPDF2 python-pptx pydub
