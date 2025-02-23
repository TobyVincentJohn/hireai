import streamlit as st
import time

# Initialize session state for interview progression
if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.messages = []
    st.session_state.follow_up_index = 0
    st.session_state.recording = False  # Initialize recording status

# Define the main question, simulated answer, and follow-up questions with answers
interview_data = {
    "question": "How would you design a scalable system to handle millions of users? Walk me through your thought process.",
    "answer": "I would adopt a microservices architecture allowing each service to scale independently. Hmm, implementing load balancers to evenly distribute requests and utilizing horizontal scaling for application servers are crucial. Also, using caching mechanisms like Redis can enhance response times significantly. Finally, considering a cloud solution with auto-scaling to manage peak traffic efficiently is essential.",
    "follow_ups": [
        {
            "question": "What specific technologies or platforms would you consider for implementing this architecture?",
            "answer": "Um, I think using Kubernetes for container orchestration, AWS or Google Cloud for infrastructure, along with Docker for packaging services would be ideal."
        },
        {
            "question": "How would you approach the challenges of service communication in such a system?",
            "answer": "I'd implement an API gateway to route requests to the appropriate microservice and use asynchronous messaging tools like RabbitMQ or Kafka for reliable communication. Hmm."
        }
    ]
}

# Hard-coded speech-to-text simulation
def simulate_speech_to_text(index):
    """Return simulated speech-to-text responses based on the index."""
    simulated_responses = [
        interview_data["answer"],
        interview_data["follow_ups"][0]["answer"],
        interview_data["follow_ups"][1]["answer"]
    ]
    return simulated_responses[index]

# Streamlit page configuration
st.set_page_config(page_title="AI System Design Interview", page_icon="🤖")
st.title("🤖 AI-Powered System Design Interview")

# Display the current question at the top
if st.session_state.step == 0:
    st.markdown(f"**AI:** {interview_data['question']}")

# Display chat history
for role, message in st.session_state.messages:
    with st.chat_message(role):
        st.markdown(message)

# Simulate recording process
if st.button("🎤 Start Recording"):
    st.session_state.recording = True  # Set recording status to True
    # st.session_state.messages.append(("ai", "Recording started. Please respond!"))
    st.rerun()  # Refresh to show the message immediately

if st.session_state.recording:
    st.markdown("**Status:** 🎤 Recording in progress... Please respond!")

if st.button("⏹ Stop Recording") and st.session_state.recording:
    st.session_state.recording = False  # Set recording status to False
    time.sleep(7)  # Simulate waiting for the response
    simulated_answer = simulate_speech_to_text(st.session_state.follow_up_index)  # Get the appropriate simulated response
    st.session_state.messages.append(("user", simulated_answer))
    st.session_state.messages.append(("ai", "Thank you for your response!"))

    # Handle follow-up questions one by one
    if st.session_state.follow_up_index < len(interview_data["follow_ups"]):
        follow_up = interview_data["follow_ups"][st.session_state.follow_up_index]
        st.session_state.messages.append(("ai", follow_up["question"]))
        st.session_state.follow_up_index += 1  # Move to the next follow-up
        st.rerun()  # Refresh to show the next question
    else:
        # All questions have been answered, show thank you message
        st.session_state.messages.append(("ai", "Thank you for taking the time to go through this system design interview with me. This concludes your interview. Have a great day! 🚀"))
        # Reset for potential next run
        st.session_state.follow_up_index = 0
        st.session_state.step += 1  # Move to the next main question (if any, but none in this case)

# Ensure thank you message is shown after all questions
if st.session_state.follow_up_index >= len(interview_data["follow_ups"]) and st.session_state.step > 0:
    st.session_state.messages.append(("ai", "Thank you for taking the time to go through this system design interview with me. This concludes your interview. Have a great day! 🚀"))
