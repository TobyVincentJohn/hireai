import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import requests

# Set up the page
st.set_page_config(page_title="Resume & Interview Analysis", layout="wide")
st.title("Resume & Interview Performance Analysis")

# Function to create a smaller bar graph
def create_bar_graph(categories, scores, title, xlabel, ylabel):
    fig, ax = plt.subplots(figsize=(6, 3))  # Smaller figure size
    y_pos = np.arange(len(categories))
    ax.barh(y_pos, scores, color='skyblue')
    ax.set_yticks(y_pos)
    ax.set_yticklabels(categories)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    for i, score in enumerate(scores):
        ax.text(score, i, f" {score}", va='center', ha='left')
    st.pyplot(fig)

# Fetch resume scores from backend
resume_response = requests.get("http://127.0.0.1:8000/resume-scores")
if resume_response.status_code == 200:
    resume_data = resume_response.json().get("resume_scores", {})
    resume_categories = list(resume_data.keys())
    resume_scores = [int(score.split("/")[0]) for score in resume_data.values()]
else:
    st.error("Failed to fetch resume scores.")
    resume_categories = []
    resume_scores = []

# Fetch system design scores from backend
system_design_response = requests.get("http://127.0.0.1:8000/system-design-scores")
if system_design_response.status_code == 200:
    system_design_data = system_design_response.json().get("system_design_scores", {})
    system_design_categories = list(system_design_data.keys())
    system_design_scores = [int(score.split("/")[0]) for score in system_design_data.values()]
else:
    st.error("Failed to fetch system design scores.")
    system_design_categories = []
    system_design_scores = []

# Fetch behavioral scores from backend
behavioral_response = requests.get("http://127.0.0.1:8000/behavioral-scores")
if behavioral_response.status_code == 200:
    behavioral_data = behavioral_response.json().get("behavioral_scores", {})
    behavioral_categories = list(behavioral_data.keys())
    behavioral_scores = [int(score.split("/")[0]) for score in behavioral_data.values()]
else:
    st.error("Failed to fetch behavioral scores.")
    behavioral_categories = []
    behavioral_scores = []

# Resume Eligibility Section
st.header("Resume Eligibility Scores")
create_bar_graph(resume_categories, resume_scores, "Resume Eligibility Breakdown", "Score (out of 100)", "Categories")
st.write(f"**Overall Resume Score:** {sum(resume_scores) / len(resume_scores):.1f}/100")

# Reasons for Resume Categories
st.subheader("Reasons for Scores:")
for category, explanation in resume_data.items():
    st.write(f"- **{category} ({explanation.split('/')[0]}/100):** {explanation.split(': ')[1]}")

# System Design Interview Performance Section
st.header("System Design Interview Performance")
create_bar_graph(system_design_categories, system_design_scores, "System Design Performance Breakdown", "Score (out of 100)", "Categories")
st.write(f"**Overall System Design Score:** {sum(system_design_scores) / len(system_design_scores):.1f}/100")

# Reasons for System Design Categories
st.subheader("Reasons for Scores:")
for category, explanation in system_design_data.items():
    st.write(f"- **{category} ({explanation.split('/')[0]}/100):** {explanation.split(': ')[1]}")

# Behavioral Interview Performance Section
st.header("Behavioral Interview Performance")
create_bar_graph(behavioral_categories, behavioral_scores, "Behavioral Performance Breakdown", "Score (out of 100)", "Categories")
st.write(f"**Overall Behavioral Score:** {sum(behavioral_scores) / len(behavioral_scores):.1f}/100")

# Reasons for Behavioral Categories
st.subheader("Reasons for Scores:")
for category, explanation in behavioral_data.items():
    st.write(f"- **{category} ({explanation.split('/')[0]}/100):** {explanation.split(': ')[1]}")