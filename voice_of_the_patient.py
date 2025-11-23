import logging
import speech_recognition as sr
from pydub import AudioSegment
from io import BytesIO
import os
# Removed: from groq import Groq, GROQ_API_KEY, STT_MODEL

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration (Keys are removed) ---
AUDIO_FILEPATH = "patient_voice_test_for_patient.mp3" # For standalone testing


# --- Step 1: Record Audio Function (Kept as is, relies on sr and pydub) ---

def record_audio(file_path, timeout=20, phrase_time_limit=None):
    """
    Records audio from the microphone and saves it as an MP3 file.
    This function is primarily for *standalone* testing, Gradio handles the recording.
    """
    recognizer = sr.Recognizer()
    
    # This logic is complex because it records WAV (for sr) and saves MP3 (for convenience).
    # Since Gradio handles the initial file path, we'll keep this only for potential direct testing.
    # The Gradio app relies on the file path it receives being readable by the next function.
    # For now, keep the original implementation (assuming it works for recording test files).
    try:
        with sr.Microphone() as source:
            logging.info("Adjusting for ambient noise...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            logging.info("Start speaking now...")
            
            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("Recording complete.")
            
            wav_data = audio_data.get_wav_data()
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))
            audio_segment.export(file_path, format="mp3", bitrate="128k")
            
            logging.info(f"Audio saved to {file_path}")
            return True

    except Exception as e:
        logging.error(f"An error occurred during recording: {e}")
        return False


# --- Step 2: Speech to Text (STT) Function (Groq Whisper replaced by Free Google STT) ---

def transcribe_with_free_google(audio_filepath):
    """Transcribes an audio file using the free Google Web Speech API via the speech_recognition library."""
    recognizer = sr.Recognizer()
    
    # Gradio passes a file path. We need to read it into a format recognizer.record can use.
    # This assumes the input file is a WAV or a format compatible with AudioFile.
    try:
        with sr.AudioFile(audio_filepath) as source:
            audio = recognizer.record(source)  # read the entire audio file
            logging.info(f"Sending {os.path.basename(audio_filepath)} to Google STT...")
            # Use the free Google Web Speech API for transcription
            transcription = recognizer.recognize_google(audio)
            return transcription
            
    except sr.UnknownValueError:
        return "Could not understand audio"
    except sr.RequestError as e:
        # This usually means no internet connection or rate limiting
        return f"Could not request results from Google Speech Recognition service; {e}"
    except FileNotFoundError:
        return "Error: Audio file not found. Please ensure the file exists."
    except Exception as e:
        logging.error(f"Transcription failed: {e}")
        return f"An unknown transcription error occurred: {e}"