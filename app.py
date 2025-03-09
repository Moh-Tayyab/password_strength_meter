import streamlit as st
import re
from zxcvbn import zxcvbn
import time

# Set page configuration
st.set_page_config(
    page_title="Password Strength Meter",
    page_icon="🔒",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        padding: 2rem;
        border-radius: 10px;
        background-color: #f8f9fa;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .stProgress > div > div > div > div {
        background-image: linear-gradient(to right, #ff0000, #ffaa00, #ffff00, #00ff00);
    }
    .password-feedback {
        padding: 1.5rem;
        border-radius: 8px;
        margin-top: 1.5rem;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        transition: all 0.3s ease;
    }
    .password-feedback:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }
    .weak {
        background-color: rgba(255, 0, 0, 0.1);
        border-left: 5px solid #ff0000;
    }
    .normal {
        background-color: rgba(255, 165, 0, 0.1);
        border-left: 5px solid #ffa500;
    }
    .strong {
        background-color: rgba(0, 128, 0, 0.1);
        border-left: 5px solid #008000;
    }
    .header {
        text-align: center;
        margin-bottom: 2rem;
        color: #2c3e50;
    }
    .suggestion-item {
        margin-bottom: 0.8rem;
        transition: transform 0.2s ease;
    }
    .suggestion-item:hover {
        transform: translateX(5px);
    }
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
        border-radius: 30px;
        padding: 0.5rem 2rem;
        border: none;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.2);
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #45a049;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        transform: translateY(-2px);
    }
    .password-input-container {
        background-color: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        margin-bottom: 1.5rem;
    }
    .result-container {
        animation: fadeIn 0.5s ease-in-out;
    }
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    .footer {
        margin-top: 2rem;
        text-align: center;
        color: #7f8c8d;
        font-size: 0.9rem;
    }
    .app-title {
        font-size: 2.5rem;
        background: linear-gradient(45deg, #2c3e50, #4CAF50);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .app-subtitle {
        color: #7f8c8d;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# App header with enhanced styling
st.markdown("<h1 class='header app-title'>🔒 Password Strength Meter</h1>", unsafe_allow_html=True)
st.markdown("<p class='header app-subtitle'>Create and verify secure passwords with instant feedback</p>", unsafe_allow_html=True)

# Create a container for the password input section
with st.container():
    st.markdown("<div class='password-input-container'>", unsafe_allow_html=True)
    
    # Password input
    password = st.text_input("Enter your password", type="password")
    
    # Submit button
    submit_button = st.button("Check Password Strength")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Function to evaluate password strength
def evaluate_password(password):
    if not password:
        return 0, "Empty", []
    
    # Use zxcvbn for comprehensive password analysis
    result = zxcvbn(password)
    score = result['score']  # 0-4 score
    
    # Get feedback from zxcvbn
    feedback = result.get('feedback', {})
    warning = feedback.get('warning', '')
    suggestions = feedback.get('suggestions', [])
    
    # Add our own suggestions if zxcvbn doesn't provide enough
    if len(suggestions) < 2:
        default_suggestions = [
            "Use a mix of characters (uppercase, lowercase, numbers, and special characters)",
            "Avoid common words or phrases",
            "Don't use personal information",
            "Make it at least 12 characters long for better security",
            "Consider using a passphrase (a sequence of random words)"
        ]
        suggestions.extend(default_suggestions)
        # Remove duplicates while preserving order
        suggestions = list(dict.fromkeys(suggestions))
    
    # Simplify to three strength categories
    if score <= 1:
        strength = "Weak"
        percentage = 25
    elif score <= 3:
        strength = "Normal"
        percentage = 65
    else:
        strength = "Strong"
        percentage = 100
    
    return percentage, strength, suggestions, warning

# Main app logic
if password and submit_button:
    # Add a small delay to simulate processing and create a smoother experience
    with st.spinner("Analyzing password strength..."):
        time.sleep(0.8)
    
    # Evaluate the password
    strength_percentage, strength_category, suggestions, warning = evaluate_password(password)
    
    # Create a container for results with animation
    st.markdown("<div class='result-container'>", unsafe_allow_html=True)
    
    # Display strength meter
    st.markdown(f"<h3>Password Strength: {strength_category}</h3>", unsafe_allow_html=True)
    st.progress(int(strength_percentage))
    
    # Display strength feedback with appropriate styling
    css_class = strength_category.lower().replace(" ", "-")
    
    with st.container():
        st.markdown(f"<div class='password-feedback {css_class}'>", unsafe_allow_html=True)
        
        # Display warning if any
        if warning:
            st.markdown(f"<h4>Warning:</h4>", unsafe_allow_html=True)
            st.markdown(f"<p class='suggestion-item'>• {warning}</p>", unsafe_allow_html=True)
        
        # Display improvement suggestions
        st.markdown("<h4>Suggestions to improve:</h4>", unsafe_allow_html=True)
        for suggestion in suggestions[:5]:  # Limit to 5 suggestions
            st.markdown(f"<p class='suggestion-item'>• {suggestion}</p>", unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Password security information
with st.expander("Learn about password security"):
    st.markdown("""
    ### Why Password Strength Matters
    
    Strong passwords are your first line of defense against unauthorized access to your accounts and personal information.
    
    ### Best Practices for Password Security:
    
    1. **Use unique passwords** for each account
    2. **Create long passwords** - aim for at least 12 characters
    3. **Mix character types** - include uppercase, lowercase, numbers, and symbols
    4. **Avoid personal information** like names, birthdays, or common words
    5. **Consider using a password manager** to generate and store complex passwords
    6. **Enable two-factor authentication** when available
    7. **Change passwords periodically**, especially for critical accounts
    
    Remember: The most secure password is one that you can remember but others cannot guess.
    """)

# Footer
st.markdown("---")
st.markdown("<div class='footer'>Created with ❤️ by Muhammad Tayyab using Streamlit • Secure Password Checker</div>", unsafe_allow_html=True)
