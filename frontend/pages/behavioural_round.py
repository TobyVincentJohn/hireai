import streamlit as st
import requests

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

# User input area for behavioral interview response
user_input = st.text_area("Your response:", height=150, placeholder="Describe your behavioral response here...")

# Submit button
if st.button("Submit Response"):
    if user_input.strip() == "":
        st.error("Please enter your response before submitting.")
    else:
        # Add user's response to chat
        st.session_state["messages"].append({"role": "user", "text": user_input})
        
        # Get AI feedback
        feedback_response = requests.post(f"{BACKEND_URL}/generate-feedback", json={"input_text": user_input})
        if feedback_response.status_code == 200:
            feedback = feedback_response.json().get("feedback", "No feedback provided.")
            st.session_state["messages"].append({"role": "ai", "text": f"Feedback:\n{feedback}"})
        else:
            st.error("Failed to get feedback.")
        
        # Generate follow-up question
        follow_up_response = requests.post(f"{BACKEND_URL}/generate-follow-up", json={"input_text": user_input})
        if follow_up_response.status_code == 200:
            follow_up_question = follow_up_response.json().get("follow_up", "No follow-up question provided.")
            st.session_state["messages"].append({"role": "ai", "text": follow_up_question})
        else:
            st.error("Failed to get follow-up question.")
        
        st.rerun()

# Button to navigate to results
if st.button("Proceed to Results"):
    st.session_state["page"] = "results"
    st.rerun()

# Check if the page should be switched
if st.session_state.get("page") == "results":
    st.set_query_params(page="results")
    st.rerun()