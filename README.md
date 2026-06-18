# AI-Powered Study Buddy (Premium Edition) 🎓✨

A highly aesthetic, multi-modular AI study assistant built with Streamlit and the Google Gemini API. This version is inspired by Notion and ChatGPT, featuring a premium glassmorphic UI, structured project architecture, and advanced document processing capabilities.

## 🌟 Premium Features
- **Strictly Gemini-2.5-Flash**: Uses the requested state-of-the-art model.
- **Glassmorphic UI**: Custom CSS with gradients, blurring, and modern typography.
- **PDF Generation**: Download your AI summaries and quizzes as properly formatted PDF files.
- **Study Progress & Streaks**: Track your mastery and stay motivated.
- **Exam Prep Mode**: A toggle that modifies the AI's prompts to focus on highly testable materials.
- **Secure Architecture**: API keys are securely loaded from a `.env` file instead of being exposed in the UI.

## 📁 Project Architecture
```
study_buddy/
│
├── app.py                  # Main Dashboard and UI Routing
├── .env                    # Environment variables (GEMINI_API_KEY)
├── requirements.txt        # Python dependencies
├── assets/
│   ├── logo.png            # Generated app icon
│   └── styles.css          # Premium Custom CSS
├── utils/
│   ├── pdf_reader.py       # PyPDF extraction & text statistics
│   ├── ai_engine.py        # Gemini API wrapper
│   └── quiz_generator.py   # PDF generation and prompt templating
└── README.md               # Documentation
```

## 🛠️ Setup Guide (Local Development)

1. **Clone the Repository**
   ```bash
   git clone <your-repo-url>
   cd study_buddy
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Open the `.env` file and replace `your_api_key_here` with your actual Google Gemini API key.
   ```env
   GEMINI_API_KEY=AIzaSy...
   ```

5. **Run the Application**
   ```bash
   streamlit run app.py
   ```

## 🚀 Deployment Guide (Streamlit Cloud)
1. Push this entire repository (excluding `.env` and `venv`) to GitHub.
2. Log into [Streamlit Community Cloud](https://share.streamlit.io/).
3. Connect your GitHub and deploy `app.py`.
4. **CRITICAL**: Go to **App Settings > Secrets** on the Streamlit dashboard and add your API key there:
   ```toml
   GEMINI_API_KEY="AIzaSy..."
   ```

---
*Built with ❤️ and Generative AI*
