import streamlit as st
import requests
import tempfile
from st_audiorec import st_audiorec

# Backend API URL
BACKEND_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Behavioral Interview", page_icon="🗣️")
st.title("🗣️ Behavioral Interview")

# Initialize chat history and question if not present
if "messages" not in st.session_state:
    st.session_state["messages"] = []
    response = requests.post(f"{BACKEND_URL}/generate-question")
    if response.status_code == 200:
        initial_question = response.json().get("question", "No question found.")
        st.session_state["messages"].append({"role": "ai", "text": initial_question})
    else:
        st.error("Failed to fetch the initial question.")

# Display chat messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["text"])

# Audio recording
st.write("Record your answer:")
wav_audio_data = st_audiorec()

if wav_audio_data is not None:
    st.audio(wav_audio_data, format='audio/wav')

# Submit button
if st.button("Submit Response"):
    if wav_audio_data is None:
        st.error("Please record your response before submitting.")
    else:
        # Save audio file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_audio:
            temp_audio.write(wav_audio_data)
            audio_path = temp_audio.name
        
        # Transcribe audio
        with open(audio_path, "rb") as audio_file:
            files = {"file": audio_file}
            transcription_response = requests.post(f"{BACKEND_URL}/transcribe-audio/", files=files)
        
        if transcription_response.status_code == 200:
            transcript = transcription_response.json().get("transcript", "")
            st.session_state["messages"].append({"role": "user", "text": transcript})
            
            # Get AI feedback
            feedback_response = requests.post(f"{BACKEND_URL}/generate-feedback", json={"input_text": transcript})
            if feedback_response.status_code == 200:
                feedback = feedback_response.json().get("feedback", "No feedback provided.")
                st.session_state["messages"].append({"role": "ai", "text": f"Feedback:\n{feedback}"})
            else:
                st.error("Failed to get feedback.")
            
            # Generate follow-up question
            follow_up_response = requests.post(f"{BACKEND_URL}/generate-follow-up", json={"input_text": transcript})
            if follow_up_response.status_code == 200:
                follow_up_question = follow_up_response.json().get("follow_up", "No follow-up question provided.")
                st.session_state["messages"].append({"role": "ai", "text": follow_up_question})
            else:
                st.error("Failed to get follow-up question.")
            
            st.experimental_rerun()
        else:
            st.error("Failed to transcribe audio.")

# Button to navigate to results
if st.button("Proceed to Results"):
    st.session_state["page"] = "results"
    st.experimental_rerun()

# Check if the page should be switched
if st.session_state.get("page") == "results":
    st.experimental_set_query_params(page="results")
    st.experimental_rerun()