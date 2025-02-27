import streamlit as st
import requests
import tempfile
from st_audiorec import st_audiorec  # Make sure to use the correct audio recorder package

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="AI Coding Interview", page_icon="💬")
st.title("💬 AI Coding Interview")

# Initialize chat history and question if not present
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    response = requests.get(f"{BACKEND_URL}/get-question/")  # Fetch the initial question from FastAPI
    if response.status_code == 200:
        initial_question = response.json().get("question", "No question found.")
        st.session_state["messages"].append({"role": "ai", "text": initial_question})
    else:
        st.error("Failed to fetch the initial question.")

# Display chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# User input area for code response
code_input = st.text_area("Your code response:", height=150, placeholder="Write your Python function here...")

# Fetch follow-up questions from backend
follow_up_response = requests.get(f"{BACKEND_URL}/get-follow-ups/")  # Assuming there's an endpoint for follow-ups
follow_up_questions = []
if follow_up_response.status_code == 200:
    follow_up_questions = follow_up_response.json().get("follow_ups", [])
else:
    st.error("Failed to fetch follow-up questions.")

# Display follow-up questions
st.write("Consider these follow-up questions:")
for question in follow_up_questions:
    st.markdown(f"- {question}")

# Audio recording placeholder
st.write("Record your explanation:")
audio_data = st_audiorec()  # Ensure the st_audiorec package is installed and imported correctly

# Submit button
if st.button("Submit Response"):
    if code_input.strip() == "":
        st.error("Please enter some code before submitting.")
    else:
        # Save audio file if recorded
        audio_path = None
        if audio_data is not None:
            with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                temp_audio.write(audio_data)
                audio_path = temp_audio.name

        # Prepare payload
        files = {"audio": open(audio_path, "rb")} if audio_path else {}
        data = {"code": code_input}
        
        # Send request to FastAPI
        response = requests.post(f"{BACKEND_URL}/submit-code-explanation/", files=files, data=data)
        
        if response.status_code == 200:
            feedback = response.json().get("feedback", "No feedback provided.")
            st.session_state["messages"].append({"role": "user", "text": f"Code Submitted:```python\n{code_input}\n```"})
            st.session_state["messages"].append({"role": "ai", "text": "Response received!"})
            st.session_state["messages"].append({"role": "ai", "text": f"Feedback: {feedback}"})
            st.session_state["messages"].append({"role": "ai", "text": "Please revise your code based on the feedback."})
            st.experimental_rerun()
        else:
            st.error("Failed to submit response. Please try again.")

# If there's feedback, allow user to modify their submission
if st.session_state.get("messages"):
    last_message = st.session_state["messages"][-1]
    if last_message["role"] == "ai" and "Feedback:" in last_message["text"]:
        st.text_area("Revise your code response:", height=150, placeholder="Modify your Python function here...", key="revised_code_input")
        if st.button("Resubmit Revised Response"):
            revised_code = st.session_state["revised_code_input"]
            if revised_code.strip() == "":
                st.error("Please enter your revised code before resubmitting.")
            else:
                # Save audio file if recorded
                audio_path = None
                if audio_data is not None:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
                        temp_audio.write(audio_data)
                        audio_path = temp_audio.name

                # Prepare payload for resubmission
                files = {"audio": open(audio_path, "rb")} if audio_path else {}
                data = {"code": revised_code}
                
                # Send request to FastAPI
                response = requests.post(f"{BACKEND_URL}/submit-code-explanation/", files=files, data=data)
                
                if response.status_code == 200:
                    feedback = response.json().get("feedback", "No feedback provided.")
                    st.session_state["messages"].append({"role": "user", "text": f"Revised Code Submitted:```python\n{revised_code}\n```"})
                    st.session_state["messages"].append({"role": "ai", "text": "Revised response received!"})
                    st.session_state["messages"].append({"role": "ai", "text": f"Feedback: {feedback}"})
                    st.experimental_rerun()
                else:
                    st.error("Failed to resubmit response. Please try again.")

# Button to navigate to system_design.py
if st.button("Go to System Design"):
    st.session_state["page"] = "system_design"
    st.experimental_rerun()

# Check if the page should be switched
if st.session_state.get("page") == "system_design":
    st.experimental_set_query_params(page="system_design")
    st.experimental_rerun()