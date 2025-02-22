import streamlit as st

def show():
    st.header("For Job Seekers")
    st.write("Content for job seekers goes here.")
    if st.button('Go to Recruiters'):
        st.session_state.page = 'recruiters'
        st.experimental_rerun()