import streamlit as st
import re
from zxcvbn import zxcvbn
import time
import string
import random
import math

# Set page configuration
st.set_page_config(
    page_title="Password Fortress",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for a professional and attractive UI
st.markdown("""
<style>
    :root {
        --primary-color: #4f46e5; /* Indigo */
        --secondary-color: #9333ea; /* Purple */
        --accent-color: #ec4899; /* Pink */
        --bg-color: #f9fafb; /* Light Gray */
        --text-color: #1f2937; /* Dark Gray */
        --glass-bg: rgba(255, 255, 255, 0.9);
        --shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
    }

    body {
        background: linear-gradient(135deg, #f3f4f6 0%, #e5e7eb 100%);
        font-family: 'Inter', sans-serif;
    }

    .main {
        background: var(--glass-bg);
        border-radius: 16px;
        padding: 2rem;
        box-shadow: var(--shadow);
        border: 1px solid rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(10px);
    }

    .stTabs [role="tablist"] {
        display: flex;
        justify-content: center;
        gap: 1rem;
        padding: 1rem 0;
        background: transparent;
    }

    .stTabs [role="tab"] {
        background: #ffffff;
        border-radius: 12px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: var(--text-color);
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }

    .stTabs [role="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.3);
    }

    .password-input-container {
        background: #ffffff;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        transition: all 0.3s ease;
    }

    .password-input-container:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.1);
    }

    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        height: 10px;
        border-radius: 5px;
    }

    .stButton > button {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
        border: none;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(79, 70, 229, 0.3);
    }

    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, var(--primary-color), var(--accent-color));
        -webkit-background-clip: text;
        background-clip: text;
        color: transparent;
        text-align: center;
        margin-bottom: 0.5rem;
    }

    .app-subtitle {
        font-size: 1.1rem;
        color: var(--text-color);
        text-align: center;
        opacity: 0.8;
    }

    .suggestion-item {
        background: #ffffff;
        padding: 1rem;
        border-radius: 8px;
        margin-bottom: 0.75rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
    }

    .suggestion-item:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
    }

    .password-feedback {
        background: var(--glass-bg);
        padding: 1.5rem;
        border-radius: 12px;
        margin-top: 1rem;
        box-shadow: var(--shadow);
    }

    .footer {
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        color: white;
        padding: 1.5rem;
        border-radius: 16px;
        text-align: center;
        margin-top: 2rem;
        font-size: 0.9rem;
        box-shadow: var(--shadow);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    .fade-in {
        animation: fadeIn 0.5s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# App Header
st.markdown("""
    <div class='fade-in'>
        <h1 class='app-title'>🛡️ Password Fortress</h1>
        <p class='app-subtitle'>Secure Your Digital Life with Confidence</p>
    </div>
""", unsafe_allow_html=True)

# Tabs for different features
tabs = st.tabs(["🔍 Check Strength", "🎲 Random Generator", "🛠️ Custom Builder"])

# Function to evaluate password strength (unchanged)
def evaluate_password(password):
    if not password:
        return 0, "Empty", [], ""
    
    result = zxcvbn(password)
    score = result['score']
    feedback = result.get('feedback', {})
    warning = feedback.get('warning', '')
    suggestions = feedback.get('suggestions', [])
    
    char_set_size = 0
    if any(c.isupper() for c in password):
        char_set_size += 26
    if any(c.islower() for c in password):
        char_set_size += 26
    if any(c.isdigit() for c in password):
        char_set_size += 10
    if any(c in string.punctuation for c in password):
        char_set_size += len(string.punctuation)
    
    entropy = 0
    if char_set_size > 0:
        entropy = math.log2(char_set_size) * len(password)
    
    if len(suggestions) < 2:
        default_suggestions = [
            "Mix uppercase, lowercase, numbers, and special characters",
            "Avoid common words or personal info",
            "Aim for at least 12 characters",
            "Use a unique password for each account",
            f"Entropy: {entropy:.1f} bits (higher is better)",
        ]
        suggestions.extend(default_suggestions)
        suggestions = list(dict.fromkeys(suggestions))
    
    if score <= 1:
        strength = "Weak"
        percentage = 25
    elif score <= 3:
        strength = "Moderate"
        percentage = 65
    else:
        strength = "Strong"
        percentage = 100
    
    return percentage, strength, suggestions, warning

# Tab 1: Password Strength Checker
with tabs[0]:
    with st.container():
        st.markdown("<div class='password-input-container fade-in'>", unsafe_allow_html=True)
        st.subheader("Test Your Password")
        password = st.text_input("Enter your password", type="password", key="check_password")
        submit_button = st.button("Analyze Strength")
        st.markdown("</div>", unsafe_allow_html=True)

# Tab 2: Random Password Generator
with tabs[1]:
    with st.container():
        st.markdown("<div class='password-input-container fade-in'>", unsafe_allow_html=True)
        st.subheader("Generate a Random Password")
        password_length = st.slider("Length", 8, 32, 16)
        col1, col2 = st.columns(2)
        with col1:
            use_uppercase = st.checkbox("Uppercase", True)
            use_lowercase = st.checkbox("Lowercase", True)
        with col2:
            use_numbers = st.checkbox("Numbers", True)
            use_special = st.checkbox("Special Characters", True)
        generate_button = st.button("Generate Password")
        
        def generate_random_password(length, use_upper, use_lower, use_nums, use_special):
            if not any([use_upper, use_lower, use_nums, use_special]):
                return "Select at least one character type", False
            chars = []
            if use_upper: chars.append(string.ascii_uppercase)
            if use_lower: chars.append(string.ascii_lowercase)
            if use_nums: chars.append(string.digits)
            if use_special: chars.append(string.punctuation)
            all_chars = ''.join(chars)
            password = []
            if use_upper: password.append(random.choice(string.ascii_uppercase))
            if use_lower: password.append(random.choice(string.ascii_lowercase))
            if use_nums: password.append(random.choice(string.digits))
            if use_special: password.append(random.choice(string.punctuation))
            remaining_length = length - len(password)
            password.extend(random.choices(all_chars, k=remaining_length))
            random.shuffle(password)
            return ''.join(password), True
        
        if generate_button:
            with st.spinner("Generating..."):
                time.sleep(0.5)
                random_password, success = generate_random_password(
                    password_length, use_uppercase, use_lowercase, use_numbers, use_special
                )
            if success:
                st.code(random_password)
                strength_percentage, strength_category, _, _ = evaluate_password(random_password)
                st.markdown(f"**Strength:** {strength_category}")
                st.progress(int(strength_percentage))
            else:
                st.error(random_password)
        st.markdown("</div>", unsafe_allow_html=True)

# Tab 3: Custom Password Generator
with tabs[2]:
    with st.container():
        st.markdown("<div class='password-input-container fade-in'>", unsafe_allow_html=True)
        st.subheader("Enhance Your Password")
        base_password = st.text_input("Enter your password", type="password", key="custom_password")
        enhance_length = st.checkbox("Increase Length", True)
        enhance_complexity = st.checkbox("Add Complexity", True)
        enhance_case = st.checkbox("Mix Case", True)
        enhance_button = st.button("Enhance Password")
        
        def enhance_password(password, add_length, add_complexity, mix_case):
            if not password:
                return "Enter a password", False
            enhanced = password
            if mix_case:
                char_list = list(enhanced)
                for i in range(len(char_list)):
                    if char_list[i].isalpha() and random.random() > 0.5:
                        char_list[i] = char_list[i].swapcase()
                enhanced = ''.join(char_list)
            if add_complexity:
                if not any(c in string.punctuation for c in enhanced):
                    enhanced += random.choice(string.punctuation)
                if not any(c.isdigit() for c in enhanced):
                    enhanced += random.choice(string.digits)
            if add_length and len(enhanced) < 12:
                extra_chars = 12 - len(enhanced)
                enhanced += ''.join(random.choices(string.ascii_letters + string.digits + string.punctuation, k=extra_chars))
            return enhanced, True
        
        if enhance_button and base_password:
            with st.spinner("Enhancing..."):
                time.sleep(0.5)
                enhanced_password, success = enhance_password(
                    base_password, enhance_length, enhance_complexity, enhance_case
                )
            if success:
                st.code(enhanced_password)
                orig_percentage, orig_category, _, _ = evaluate_password(base_password)
                enhanced_percentage, enhanced_category, _, _ = evaluate_password(enhanced_password)
                col1, col2 = st.columns(2)
                with col1:
                    st.markdown(f"**Original:** {orig_category}")
                    st.progress(int(orig_percentage))
                with col2:
                    st.markdown(f"**Enhanced:** {enhanced_category}")
                    st.progress(int(enhanced_percentage))
            else:
                st.error(enhanced_password)
        st.markdown("</div>", unsafe_allow_html=True)

# Main logic for Password Checker
if password and submit_button:
    with st.spinner("Analyzing..."):
        time.sleep(0.8)
    strength_percentage, strength_category, suggestions, warning = evaluate_password(password)
    st.markdown("<div class='password-feedback fade-in'>", unsafe_allow_html=True)
    st.markdown(f"**Strength:** {strength_category}")
    st.progress(int(strength_percentage))
    if warning:
        st.warning(f"⚠️ {warning}")
    if suggestions:
        st.markdown("**Suggestions:**")
        for suggestion in suggestions[:5]:
            st.markdown(f"- {suggestion}", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Security Tips
with st.expander("🔐 Password Security Tips"):
    st.markdown("""
    - Use **unique passwords** for every account
    - Aim for **12+ characters**
    - Include a mix of **letters, numbers, and symbols**
    - Avoid **personal info** (e.g., birthdays)
    - Consider a **password manager**
    """)

# Footer
st.markdown("""
    <div class='footer fade-in'>
        Created with ❤️ by Muhammad Tayyab • Powered by Streamlit
    </div>
""", unsafe_allow_html=True)