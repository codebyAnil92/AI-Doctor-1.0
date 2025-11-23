# AI Doctor 2.0: Voice and Vision Medical Assistant

This project is a Gradio-based application that simulates an AI medical assistant capable of performing basic consultations using voice input and image analysis. The application uses a multimodal Large Language Model (LLM) to analyze medical images (e.g., a rash or injury) and provide a concise, doctor-like response via text and speech.

## 🚀 Key Features

* **Multimodal Analysis:** Analyzes a patient's verbal query and an uploaded image simultaneously.
* **Free-Tier LLM:** Utilizes the **Gemini API (`gemini-2.5-flash`)** for cost-effective, high-performance vision and language processing.
* **Voice Input (STT):** Transcribes patient questions using the free **Google Web Speech API** via the `SpeechRecognition` library.
* **Voice Output (TTS):** Generates the doctor's audio response using the free **gTTS (Google Text-to-Speech)** library.
* **Gradio Interface:** Provides a simple, modern web interface for interaction.

---

## 🛠️ Setup and Installation

### 1. Prerequisites

You need **Python 3.8+** installed on your system.

### 2. Install System Dependencies (FFmpeg)

The `pydub` library, which is used for audio handling, requires the system-level FFmpeg library.

* **Windows:** Use Chocolatey: `choco install ffmpeg`
* **macOS:** Use Homebrew: `brew install ffmpeg`
* **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install ffmpeg`

### 3. Install Python Dependencies

Navigate to your project directory (`ai-doctor-2.0-voice-and-vision-main`) and run the following command using the `requirements.txt` file provided:

```bash
pip install -r requirements.txt