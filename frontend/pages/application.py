import streamlit as st
import os
import requests

# Set the page configuration
st.set_page_config(page_title="Job Application Form", page_icon="📝")

# Ensure the 'resumes' directory exists
os.makedirs("resumes", exist_ok=True)

# Custom form UI
st.title("📝 Job Application Form")

with st.form(key="job_application"):
    name = st.text_input("Full Name", placeholder="John Doe")
    email = st.text_input("Email", placeholder="johndoe@example.com")
    experience = st.selectbox("Experience Level", ["Fresher", "1-2 years", "3-5 years", "5+ years"])
    skills = st.text_area("Skills", placeholder="Python, AI, SQL...")
    
    # Replace text input with a dropdown for niche job roles
    niche_job_roles = [
        "Data Scientist",
        "Machine Learning Engineer",
        "AI Researcher",
        "Deep Learning Engineer",
        "NLP Specialist",
        "Computer Vision Engineer",
        "Data Engineer",
        "Big Data Specialist",
        "Research Scientist"
    ]
    job_role = st.selectbox("Preferred Job Role", options=niche_job_roles, index=0)
    
    resume = st.file_uploader("Upload Resume", type=["pdf", "docx"])

    submit_button = st.form_submit_button("Submit Application")

# Handle form submission
if submit_button:
    if not name or not email or not resume:
        st.error("⚠️ Please fill in all required fields!")
    else:
        # Prepare data for submission
        application_data = {
            "name": name,
            "email": email,
            "experience": experience,
            "skills": skills,
            "job_role": job_role
        }
        
        # Send data to the FastAPI backend
        files = {"resume": (resume.name, resume.getbuffer(), resume.type)}
        
        try:
            response = requests.post("http://localhost:8000/submit-form/", data=application_data, files=files)
            response_data = response.json()
            if response.status_code == 200:
                st.success(response_data["message"])
                st.switch_page("pages/coding_task.py")
            else:
                st.error("⚠️ An error occurred while submitting your application.")
        except Exception as e:
            st.error(f"⚠️ Error: {str(e)}")
