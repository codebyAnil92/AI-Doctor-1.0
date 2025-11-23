import os
import gradio as gr
import logging
import tempfile 
from brain_of_the_doctor import analyze_image_with_query # New Gemini-powered function
from voice_of_the_patient import transcribe_with_free_google # New free STT function
from voice_of_the_doctor import text_to_speech # New gTTS function

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Configuration ---

SYSTEM_PROMPT = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
    What's in this image?. Do you find anything wrong with it medically? 
    If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
    your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
    Donot say 'In the image I see' but say 'With what I see, I think you have ....'
    Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
    Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

# --- Main Logic ---

def process_inputs(audio_filepath, image_filepath):
    """
    Handles the transcription, Gemini LLM analysis, and gTTS generation pipeline.
    """
    
    # 1. Speech to Text (STT) - Get the transcription
    if not audio_filepath:
        speech_to_text_output = "No audio recorded."
    else:
        # Call the free Google STT service
        speech_to_text_output = transcribe_with_free_google(audio_filepath)
        
    # 2. Multimodal LLM / Doctor's Response (using the Gemini API)
    
    if not image_filepath and ("Error" in speech_to_text_output or "Could not understand" in speech_to_text_output):
        doctor_response = "I need both an image and clear speech to provide an assessment. Please try again."
        
    elif not image_filepath:
        # Only audio provided
        doctor_response = f"Thank you for your question: '{speech_to_text_output}'. Please upload an image for a proper visual assessment."
        
    elif "Error" in speech_to_text_output or "Could not understand" in speech_to_text_output:
        # Image provided, but speech failed. Use a default query.
        query_for_llm = "Analyze this medical image and provide a diagnosis based on the image."
        doctor_response = analyze_image_with_query(
            query=query_for_llm, 
            image_path=image_filepath,
            system_prompt=SYSTEM_PROMPT 
        )
        
    else:
        # Both image and clear audio provided. Use the transcribed text as the query.
        doctor_response = analyze_image_with_query(
            query=speech_to_text_output, 
            image_path=image_filepath,
            system_prompt=SYSTEM_PROMPT 
        )


    # 3. Text to Speech (TTS) - Using gTTS
    # Create a temporary file path for the doctor's audio response
    temp_output_file = os.path.join(tempfile.gettempdir(), f"doctor_voice_response.mp3")
    
    try:
        # Use the gTTS function
        text_to_speech(
            input_text=doctor_response, 
            output_filepath=temp_output_file
        )
        # Return the path to the newly created temporary file.
        return speech_to_text_output, doctor_response, temp_output_file
        
    except Exception as e:
        logging.error(f"TTS generation failed: {e}")
        # Return an error message in the audio output box
        return speech_to_text_output, doctor_response, None


# --- Gradio Interface ---
iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="1. Record Patient's Voice"),
        gr.Image(type="filepath", label="2. Upload Medical Image (Optional)")
    ],
    outputs=[
        gr.Textbox(label="3. Patient's Speech (Text)", lines=3),
        gr.Textbox(label="4. Doctor's Medical Response", lines=5),
        gr.Audio(label="5. Doctor's Voice", value=None) 
    ],
    title="Gemini-Powered Voice-and-Vision AI Doctor (Free-Tier API)",
    description="A medical consultation app using the Gemini API for analysis and open-source libraries (gTTS, SpeechRecognition) for voice I/O.",
)

if __name__ == "__main__":
    iface.launch()