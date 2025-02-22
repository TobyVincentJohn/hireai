import streamlit as st

# Initialize session state
if 'page' not in st.session_state:
    st.session_state.page = 'home'

def navigate_to(page):
    st.session_state.page = page

if st.session_state.page == 'home':
    st.html('''
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');

    body {
        font-family: 'Inter', sans-serif;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        margin: 0;
        background-color: #f8f9fa;
    }

    .container {
        text-align: center;
    }

    .title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1a1a1a;
        margin-bottom: 1rem;
    }

    .subtitle {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 0.5rem;
        font-weight: 400;
    }

    .button {
        margin-top: 2rem;
        padding: 0.8rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        color: white;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        border: none;
        border-radius: 8px;
        cursor: pointer;
        transition: transform 0.2s, box-shadow 0.2s;
    }

    .button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.2);
    }
    </style>
    </head>
    <body>
        <div class="container">
            <h1 class="title">Welcome to Our Platform</h1>
            <p class="subtitle">Transforming the way you work</p>
            <p class="subtitle">Start your journey with us today</p>
            <button class="button" onclick="window.location.href='/recruiters'">Get Started</button>
        </div>
    </body>
    </html>
    ''')
    if st.button('Get Started'):
        navigate_to('recruiters')

elif st.session_state.page == 'recruiters':
    import pages.for_recruiters as for_recruiters
    for_recruiters.show()

elif st.session_state.page == 'job_seekers':
    import pages.for_job_seekers as for_job_seekers
    for_job_seekers.show()