import os
import logging
import mimetypes 
from google import genai
from google.genai import types

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Step 1: Configuration and API Key (FIXED to use your key directly) ---

# 🚨 IMPORTANT: Your actual Gemini API key is hardcoded here.
MY_ACTUAL_GEMINI_KEY = "AIzaSyB0CoveY1xaxELlq3wRDp3BjHi2EWBXR2I"

# CRITICAL FIX: Assign the key directly to bypass environment variable errors.
GEMINI_API_KEY = MY_ACTUAL_GEMINI_KEY
VISION_MODEL = "gemini-2.5-flash"

if not GEMINI_API_KEY or "YOUR_GEMINI_API_KEY_HERE" in GEMINI_API_KEY:
    # This check remains as a final safeguard against an empty string
    logging.error("❌ FATAL: GEMINI_API_KEY is missing or invalid. The service will fail.")


# --- Step 2: Multimodal LLM Analysis Function (CRITICAL FILE FIX) ---

def analyze_image_with_query(query: str, image_path: str, system_prompt: str) -> str:
    """
    Analyzes an image and a text query using the Gemini API.
    Uses raw bytes to bypass the problematic 'from_file' path error.
    """
    
    # 1. Handle Missing/Invalid API Key
    if not GEMINI_API_KEY:
        return f"Service Error: Gemini API Key not configured."
    
    # 2. Check for file existence before attempting to read
    if not os.path.exists(image_path):
        logging.error(f"Image file not found at path: {image_path}")
        return f"File Error: The image file was not found. Please ensure the file is correctly uploaded."
        
    try:
        # Initialize the client
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # 3. Determine MIME type robustly
        mime_type, _ = mimetypes.guess_type(image_path)
        if not mime_type or not mime_type.startswith('image/'):
            mime_type = "image/jpeg" # Default to common type if detection fails
        
        logging.info(f"Processing image: {os.path.basename(image_path)} with MIME type: {mime_type}")
        
        # 4. 🌟 CRITICAL FIX: Read the file content into memory (bytes) manually
        # This resolves the persistent 'from_file' error.
        with open(image_path, "rb") as f:
            image_data = f.read()

        # Pass the bytes directly to the API
        image_part = types.Part.from_bytes(data=image_data, mime_type=mime_type)
        
        prompt_parts = [
            image_part,
            query
        ]

        # 5. Call the Gemini API
        response = client.models.generate_content(
            model=VISION_MODEL,
            contents=prompt_parts,
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
            ),
        )
        
        return response.text.replace('\n', ' ').strip()
        
    except Exception as e:
        # Log and return the error detail for continued debugging
        logging.error(f"Gemini API call failed. Detail: {e}")
        return f"API Call Error: The external LLM service failed. Detail: {e}"