import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Set up the page
st.set_page_config(page_title="Resume & Interview Analysis", layout="wide")
st.title("Resume & Interview Performance Analysis")

# Placeholder data for resume eligibility
resume_categories = ["Relevant Skills", "Experience", "Contact Info", "Achievements", "Projects"]
resume_scores = [87, 92, 100, 78, 83]  # Updated scores with varied digits

# Placeholder data for interview performance
system_design_categories = ["Problem Understanding", "Solution Design", "Scalability", "Trade-offs", "Communication"]
system_design_scores = [82, 86, 91, 77, 89]  # Updated scores with varied digits

behavioral_categories = ["Communication", "Teamwork", "Problem-Solving", "Leadership", "Adaptability"]
behavioral_scores = [91, 84, 87, 83, 88]  # Updated scores with varied digits

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

# Resume Eligibility Section
st.header("Resume Eligibility Scores")
create_bar_graph(resume_categories, resume_scores, "Resume Eligibility Breakdown", "Score (out of 100)", "Categories")
st.write(f"**Overall Resume Score:** {sum(resume_scores) / len(resume_scores):.1f}/100")

# Reasons for Resume Categories
st.subheader("Reasons for Scores:")
st.write("""
- **Relevant Skills (87/100):** The candidate demonstrates proficiency in key programming languages (Python, Java, C++) and frameworks (Django, Flask, React.js) required for the role. However, deeper expertise in cloud platforms (AWS, Azure) and DevOps practices could improve this score.
- **Experience (92/100):** With 3+ years of professional experience, including a recent role as a Data Analyst, the candidate has a strong foundation in software development and collaboration. The experience aligns well with the job's requirements.
- **Contact Info (100/100):** The resume provides complete and professional contact information, including email, phone number, and location.
- **Achievements (78/100):** The candidate has notable achievements, such as winning hackathons and optimizing business processes. However, more specific achievements related to software engineering (e.g., building scalable systems) would strengthen this section.
- **Projects (83/100):** The candidate has worked on impressive projects, such as an AI-powered presentation generator and a hybrid stock prediction model. These demonstrate strong technical skills and innovation, but more projects directly related to web development or cloud technologies would be ideal.
""")

# System Design Interview Performance Section
st.header("System Design Interview Performance")
create_bar_graph(system_design_categories, system_design_scores, "System Design Performance Breakdown", "Score (out of 100)", "Categories")
st.write(f"**Overall System Design Score:** {sum(system_design_scores) / len(system_design_scores):.1f}/100")

# Reasons for System Design Categories
st.subheader("Reasons for Scores:")
st.write("""
- **Problem Understanding (82/100):** The candidate demonstrates a good grasp of problem requirements but could improve by asking more clarifying questions to fully understand edge cases.
- **Solution Design (86/100):** The candidate proposes well-structured solutions but could better justify design choices and consider alternative approaches.
- **Scalability (91/100):** The candidate shows a strong understanding of scalability, such as using distributed systems and load balancing, which aligns with the job's focus on high-quality software.
- **Trade-offs (77/100):** The candidate identifies trade-offs but could provide more detailed analysis, such as cost vs. performance or latency vs. consistency.
- **Communication (89/100):** The candidate communicates ideas clearly and effectively, making it easy to follow their thought process. However, they could improve by using more visual aids (e.g., diagrams) to explain complex concepts.
""")

# Behavioral Interview Performance Section
st.header("Behavioral Interview Performance")
create_bar_graph(behavioral_categories, behavioral_scores, "Behavioral Performance Breakdown", "Score (out of 100)", "Categories")
st.write(f"**Overall Behavioral Score:** {sum(behavioral_scores) / len(behavioral_scores):.1f}/100")

# Reasons for Behavioral Categories
st.subheader("Reasons for Scores:")
st.write("""
- **Communication (91/100):** The candidate communicates effectively, providing clear and concise answers. They demonstrate strong interpersonal skills, which are essential for collaborating in a team environment.
- **Teamwork (84/100):** The candidate has experience working in cross-functional teams, as evidenced by their role at Superposition Pvt Ltd. They could further highlight specific examples of resolving conflicts or leading team initiatives.
- **Problem-Solving (87/100):** The candidate showcases excellent problem-solving skills, such as optimizing business processes and automating reports. They could improve by discussing more complex or ambiguous problems they've solved.
- **Leadership (83/100):** The candidate demonstrates leadership potential through hackathon wins and project management. However, they could provide more examples of mentoring peers or driving team success.
- **Adaptability (88/100):** The candidate shows adaptability by working with diverse technologies and teams. They could further highlight how they've adapted to unexpected challenges or changes in project scope.
""")