from fastapi import FastAPI, Depends, HTTPException, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from abstract_ai import AIWrapper
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from ibm_watson import SpeechToTextV1
from dotenv import load_dotenv
import os
import re
import pymupdf4llm  # Importing the pymupdf4llm library

# Load environment variables
load_dotenv()

app = FastAPI()

# Enable CORS (to allow Streamlit frontend to communicate with this API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Directory to store uploaded resumes
UPLOAD_DIR = "resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# AI Wrapper Dependency
def get_ai_wrapper():
    """Initialize IBM Granite AIWrapper with authentication."""
    api_key = os.getenv("WATSON_KEY")
    
    if not api_key:
        raise HTTPException(status_code=500, detail="IBM Watson API key is missing.")
    
    try:
        authenticator = IAMAuthenticator(api_key)
        access_token = authenticator.token_manager.get_token()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Authentication Error: {str(e)}")

    api_url = "https://us-south.ml.cloud.ibm.com/ml/v1/text/generation?version=2023-05-29"
    model_id = "ibm/granite-3-8b-instruct"
    project_id = "3d9b8852-34e2-4b58-a164-622856e19e5a"

    return AIWrapper(api_url, model_id, project_id, access_token)

# IBM Speech to Text Dependency
def get_speech_to_text():
    """Initialize IBM Speech to Text with authentication."""
    api_key = os.getenv("IBM_STT_API_KEY")
    url = os.getenv("IBM_STT_URL")
    
    if not api_key or not url:
        raise HTTPException(status_code=500, detail="IBM Speech to Text API key or URL is missing.")
    
    try:
        authenticator = IAMAuthenticator(api_key)
        stt = SpeechToTextV1(authenticator=authenticator)
        stt.set_service_url(url)
        return stt
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Speech to Text Authentication Error: {str(e)}")

class InputText(BaseModel):
    input_text: str

@app.post("/transcribe-audio/")
async def transcribe_audio(file: UploadFile = File(...), stt: SpeechToTextV1 = Depends(get_speech_to_text)):
    """Transcribe audio file using IBM Speech to Text."""
    try:
        audio = file.file.read()
        response = stt.recognize(audio=audio, content_type='audio/wav').get_result()
        transcript = response['results'][0]['alternatives'][0]['transcript']
        return {"transcript": transcript}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription Error: {str(e)}")

@app.post("/generate-question")
async def generate_question(ai_wrapper: AIWrapper = Depends(get_ai_wrapper)):
    """Generate a system design interview question."""
    try:
        prompt = "Generate a challenging system design interview question."
        response = ai_wrapper.get_response(prompt)
        return {"question": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation Error: {str(e)}")

@app.post("/generate-feedback")
async def generate_feedback(answer: InputText, ai_wrapper: AIWrapper = Depends(get_ai_wrapper)):
    """Generate feedback for a system design answer."""
    try:
        prompt = f"Analyze this system design answer and provide feedback:\n\n{answer.input_text}"
        response = ai_wrapper.get_response(prompt)
        return {"feedback": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation Error: {str(e)}")

@app.post("/generate-follow-up")
async def generate_follow_up(context: InputText, ai_wrapper: AIWrapper = Depends(get_ai_wrapper)):
    """Generate a follow-up question based on the previous answer."""
    try:
        prompt = f"Based on the previous answer:\n{context.input_text}\nGenerate a relevant follow-up question."
        response = ai_wrapper.get_response(prompt)
        return {"follow_up": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation Error: {str(e)}")