# 🛡️ Password Fortress

A modern, interactive web application that helps users create secure passwords by providing real-time strength analysis, random password generation, and password enhancement capabilities.

![Password Strength Meter](https://img.shields.io/badge/Security-Password%20Strength-brightgreen)
![Streamlit](https://img.shields.io/badge/Built%20with-Streamlit-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Features

- **Real-time Password Strength Evaluation**: Instantly analyze password security using the robust zxcvbn algorithm
- **Visual Strength Indicator**: Color-coded progress bar shows password strength at a glance
- **Detailed Feedback**: Receive specific warnings about password vulnerabilities
- **Personalized Suggestions**: Get actionable tips to improve your password security
- **Random Password Generator**: Create strong, customizable random passwords with various character options
- **Password Enhancer**: Strengthen existing passwords by adding complexity, length, and mixed case
- **Entropy Calculation**: View the mathematical entropy of your passwords for security assessment
- **Beautiful UI/UX**: Enjoy a clean, responsive interface with smooth animations and a modern design

## 🚀 Installation

### Prerequisites

- Python 3.9 or higher
- pip (Python package installer)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/password-fortress.git
   cd password-fortress
   ```

2. Create a virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Usage

1. Start the Streamlit application:
   ```bash
   streamlit run app.py
   ```

2. Open your web browser and navigate to the URL displayed in your terminal (typically http://localhost:8501)

3. Use the tabbed interface to access different features:
   - **🔍 Check Strength**: Enter a password and analyze its security level
   - **🎲 Random Generator**: Create strong random passwords with customizable options
   - **🛠️ Custom Builder**: Enhance existing passwords by adding complexity and length

## 🔧 How It Works

The application uses the zxcvbn library, developed by Dropbox, which employs pattern matching and frequency lists to evaluate password strength. The strength assessment considers factors such as:

- Password length
- Character variety (uppercase, lowercase, numbers, symbols)
- Common patterns and sequences
- Dictionary words and names
- Known leaked passwords

Additionally, the app calculates password entropy, which is a mathematical measure of password unpredictability based on the character set size and password length.

Based on this analysis, the app provides:

1. A strength score (Weak, Moderate, Strong)
2. Visual feedback with color-coded indicators
3. Specific warnings about detected vulnerabilities
4. Customized suggestions for improving password security

## 🛠️ Technologies Used

- **Streamlit**: For the web application framework and interactive UI components
- **zxcvbn-python**: For advanced password strength analysis
- **Python**: Core programming language
- **HTML/CSS**: For custom styling and animations

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👨‍💻 Author

Created with ❤️ by Muhammad Tayyab

---

### 🔐 Remember

The most secure password is one that you can remember but others cannot guess. Use this tool to create strong, unique passwords for all your accounts!