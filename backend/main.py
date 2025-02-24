from fastapi import FastAPI, Depends, HTTPException, UploadFile, Form, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from abstract_ai import AIWrapper
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
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

class InputText(BaseModel):
    input_text: str

def read_pdf(file_path):
    """Read the PDF file and extract text."""
    document = pymupdf4llm.to_markdown(file_path)
    return document

def compare_resume_to_job_description(resume_text, job_description, ai_wrapper):
    """Compare the resume text to the job description using AI and return scores in a detailed format."""
    input_text = (
    f"Compare the following resume to the job description for the purpose of hiring the candidate for this role so be very strict about relevance to the role and provide a match score for each section in the format below. "
    f"Critically evaluate each section based on the criteria provided:\n\n"
    
    f"Contact Information (CRITICAL EVALUATION REQUIRED): Assess whether the candidate has provided a professional email, phone number, LinkedIn, or portfolio link. Ensure completeness and correctness.\n\n"
    
    f"Summary or Objective Statement (CRITICAL EVALUATION REQUIRED): Analyze the clarity, relevance, and impact of the summary. Does it align with the job role, highlight strengths, and set the right tone?\n\n"
    
    f"Relevant Experience (CRITICAL EVALUATION REQUIRED): Assess alignment with the job role in terms of:\n"
    f"- Direct relevance of past roles and responsibilities.\n"
    f"- Depth of experience in required technologies, frameworks, and tools.\n"
    f"- Problem-solving ability and demonstrated innovation.\n"
    f"- Scale and impact of previous projects.\n"
    f"- Industry/domain experience.\n\n"
    
    f"Education (CRITICAL EVALUATION REQUIRED): Evaluate whether the candidate’s academic background matches job requirements. Consider:\n"
    f"- Relevance of degree and institution credibility.\n"
    f"- Additional coursework, research, or specialization.\n"
    f"- Academic performance and achievements.\n\n"
    
    f"Skills (CRITICAL EVALUATION REQUIRED): Analyze proficiency in required technical and soft skills. Consider:\n"
    f"- Direct match with job requirements.\n"
    f"- Depth of expertise and breadth of knowledge.\n"
    f"- Any missing essential skills or additional advantageous ones.\n\n"
    
    f"Projects or Portfolio (CRITICAL EVALUATION REQUIRED): Evaluate the candidate’s hands-on experience based on:\n"
    f"- Complexity and relevance of projects.\n"
    f"- Use of cutting-edge technologies and problem-solving approach.\n"
    f"- Contributions, impact, and demonstration of practical expertise.\n\n"
    
    f"Certifications and Training (CRITICAL EVALUATION REQUIRED): Determine relevance to the role. Are they industry-recognized? Do they fill knowledge gaps?\n\n"
    
    f"Volunteer Experience (CRITICAL EVALUATION REQUIRED): Assess relevance and impact. Does it demonstrate leadership, teamwork, or other transferable skills?\n\n"
    
    f"Awards and Recognitions (CRITICAL EVALUATION REQUIRED): Evaluate their credibility and significance in relation to the job.\n\n"
    
    f"Hobbies and Interests (CRITICAL EVALUATION REQUIRED): Assess whether they add value, showcase relevant traits, or indicate cultural fit.\n\n"
    
    f"Resume:\n{resume_text}\n\n"
    f"Job Description:\n{job_description}\n\n"
    
    f"Provide match scores as a percentage for each section along with a detailed explanation of the score."
)

    response = ai_wrapper.get_response(input_text)
    return response

@app.post("/generate-system-design")
async def generate_system_design(input_type: str, context: str = None, ai_wrapper: AIWrapper = Depends(get_ai_wrapper)):
    """Generate system design questions, feedback, or follow-ups."""
    try:
        if input_type == "initial_question":
            prompt = "Generate a challenging system design interview question."
        elif input_type == "feedback":
            prompt = f"Analyze this system design answer and provide feedback:\n\n{context}"
        elif input_type == "follow_up":
            prompt = f"Based on the previous answer:\n{context}\nGenerate a relevant follow-up question."
        
        response = ai_wrapper.get_response(prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation Error: {str(e)}")

@app.post("/submit-form/")
async def submit_form(
    name: str = Form(...),
    email: str = Form(...),
    experience: str = Form(...),
    skills: str = Form(...),
    job_role: str = Form(...),
    resume: UploadFile = File(...)
):
    """Handles job seeker form submission & saves resume file."""
    
    # Validate inputs
    if not name or not email or not resume.filename:
        raise HTTPException(status_code=400, detail="Missing required fields.")

    # Sanitize resume filename
    sanitized_filename = re.sub(r'[^a-zA-Z0-9_.-]', '_', resume.filename)

    # Save the uploaded resume file
    resume_path = os.path.join(UPLOAD_DIR, sanitized_filename)
    try:
        with open(resume_path, "wb") as buffer:
            buffer.write(await resume.read())
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")

    # Read the resume file and extract text using PyMuPDF
    try:
        resume_text = read_pdf(resume_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading resume file: {str(e)}")

    # Read the job description from the text file
    job_description_path = "job_description/jd.pdf"  # Replace with the actual path to your job description file
    job_description = read_pdf(job_description_path)

    # Compare the resume to the job description using AI
    try:
        ai_wrapper = get_ai_wrapper()
        comparison_result = compare_resume_to_job_description(resume_text, job_description, ai_wrapper)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error comparing resume to job description: {str(e)}")

    return {
        "message": "Form submitted successfully!",
        "application": {
            "comparison_result": comparison_result  # Include the comparison result in the response
        }
    }

@app.get("/resume-scores")
async def get_resume_scores(ai_wrapper: AIWrapper = Depends(get_ai_wrapper)):
    """Generate resume scores and explanations using AI."""
    try:
        prompt = (
            "Generate scores and explanations for the following resume sections:\n\n"
            "1. Relevant Skills\n"
            "2. Experience\n"
            "3. Contact Info\n"
            "4. Achievements\n"
            "5. Projects\n\n"
            "Provide the scores as percentages and detailed explanations for each section."
        )
        response = ai_wrapper.get_response(prompt)
        return {"resume_scores": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation Error: {str(e)}")

@app.get("/system-design-scores")
async def get_system_design_scores(ai_wrapper: AIWrapper = Depends(get_ai_wrapper)):
    """Generate system design scores and explanations using AI."""
    try:
        prompt = (
            "Generate scores and explanations for the following system design interview sections:\n\n"
            "1. Problem Understanding\n"
            "2. Solution Design\n"
            "3. Scalability\n"
            "4. Trade-offs\n"
            "5. Communication\n\n"
            "Provide the scores as percentages and detailed explanations for each section."
        )
        response = ai_wrapper.get_response(prompt)
        return {"system_design_scores": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation Error: {str(e)}")

@app.get("/behavioral-scores")
async def get_behavioral_scores(ai_wrapper: AIWrapper = Depends(get_ai_wrapper)):
    """Generate behavioral interview scores and explanations using AI."""
    try:
        prompt = (
            "Generate scores and explanations for the following behavioral interview sections:\n\n"
            "1. Communication\n"
            "2. Teamwork\n"
            "3. Problem-Solving\n"
            "4. Leadership\n"
            "5. Adaptability\n\n"
            "Provide the scores as percentages and detailed explanations for each section."
        )
        response = ai_wrapper.get_response(prompt)
        return {"behavioral_scores": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI Generation Error: {str(e)}")