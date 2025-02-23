import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="HireAI - AI-Powered Hiring", page_icon="🤖", layout="wide")

# Custom HTML for styling
html_code = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HireAI</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            background: linear-gradient(135deg, #1F1C2C, #928DAB);
            color: white;
            text-align: center;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
        }
        .container {
            max-width: 600px;
            padding: 40px;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 12px;
            box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.3);
        }
        h1 {
            font-size: 42px;
            font-weight: 700;
            margin-bottom: 10px;
        }
        p {
            font-size: 18px;
            margin-bottom: 20px;
            opacity: 0.9;
        }
        .tagline {
            font-size: 22px;
            font-weight: 500;
            color: #FFD700;
            margin-bottom: 20px;
        }
        .button-container {
            margin-top: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🚀 Welcome to HireAI</h1>
        <p class="tagline">AI-Powered Hiring Made Simple</p>
        <p>Automate your job applications, get AI-driven resume screening, and advance your career effortlessly.</p>
        <div class="button-container">
            <!-- Streamlit button placeholder -->
            <div id="streamlit-button"></div>
        </div>
    </div>
</body>
</html>
"""

# Render the HTML with a placeholder for the Streamlit button
components.html(html_code, height=600)

# Apply button (Streamlit native for navigation)
if st.button("Start Your Application"):
    st.switch_page("pages/application.py")