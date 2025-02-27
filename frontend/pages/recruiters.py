import streamlit as st
from app import navigate_to

def show():
    st.title("Recruiters Page")
    st.write("Welcome to the Recruiters page. Here you can find tools and resources to help you find the best candidates.")

    st.header("Job Postings")
    st.write("Create and manage your job postings here.")

    st.header("Candidate Search")
    st.write("Search for candidates that match your job requirements.")

    st.header("Analytics")
    st.write("View analytics and reports on your job postings and candidate searches.")

    if st.button('Go to Home'):
        navigate_to('home')