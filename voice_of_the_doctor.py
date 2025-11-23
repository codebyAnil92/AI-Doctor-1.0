import os
import subprocess
import platform
import logging
from gtts import gTTS
# Removed: import elevenlabs, ElevenLabs, ELEVENLABS_API_KEY

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration (All API keys removed) ---

# --- Step 1a: TTS with gTTS (The main save function) ---

def text_to_speech(input_text, output_filepath):
    """Saves text-to-speech audio to a file using gTTS (replacing the old ElevenLabs function)."""
    try:
        # gTTS uses a language code, not a voice name
        language = "en"
        audioobj = gTTS(
            text=input_text,
            lang=language,
            slow=False
        )
        audioobj.save(output_filepath)
        logging.info(f"gTTS audio saved to {output_filepath}")
    except Exception as e:
        logging.error(f"gTTS failed: {e}")
        # Re-raise the exception for the calling function to handle (e.g., in Gradio)
        raise

# --- Optional: Audio playback functions (Kept, but not used by Gradio pipeline) ---

def play_audio(output_filepath):
    """Plays the audio file using OS-specific commands."""
    os_name = platform.system()
    try:
        if os_name == "Darwin":  # macOS
            subprocess.run(['afplay', output_filepath])
        elif os_name == "Windows":  # Windows
            # Corrected PowerShell command for Windows compatibility
            subprocess.run(['powershell', '-c', f'(New-Object Media.SoundPlayer \"{output_filepath}\").PlaySync();'])
        elif os_name == "Linux":  # Linux
            subprocess.run(['aplay', output_filepath])
        else:
            logging.warning(f"Unsupported OS ({os_name}). Audio will not auto-play.")
    except Exception as e:
        logging.error(f"Error playing audio: {e}")