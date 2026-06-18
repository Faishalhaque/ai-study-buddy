import streamlit as st
import os
import requests
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
from streamlit_lottie import st_lottie

from utils.ai_engine import initialize_ai, get_gemini_response
from utils.pdf_reader import extract_text_and_stats
from utils.quiz_generator import generate_quiz, generate_flashcards, save_as_pdf

# ==========================================
# Configuration & Setup
# ==========================================
st.set_page_config(page_title="AI Study Buddy", page_icon="🎓", layout="wide")

# Load CSS
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        st.error(f"Failed to load CSS: {str(e)}")

load_css("assets/styles.css")

# Lottie Animation Loader
def load_lottieurl(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Initialize AI & Session State
ai_ready, ai_message = initialize_ai()

# Session States
if "pdf_data" not in st.session_state:
    st.session_state.pdf_data = None
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "mcqs" not in st.session_state:
    st.session_state.mcqs = ""
if "flashcards" not in st.session_state:
    st.session_state.flashcards = ""
if "revision_notes" not in st.session_state:
    st.session_state.revision_notes = ""
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "study_streak" not in st.session_state:
    st.session_state.study_streak = 3 # Hardcoded starting streak for UI demonstration
if "exam_mode" not in st.session_state:
    st.session_state.exam_mode = False

# ==========================================
# Sidebar Navigation
# ==========================================
with st.sidebar:
    try:
        logo = Image.open("assets/logo.png")
        st.image(logo, use_column_width=True)
    except:
        st.title("🎓 AI Study Buddy")
        
    st.markdown("---")
    
    st.markdown("### Navigation")
    pages = [
        "🏠 Home Dashboard", 
        "📄 PDF Upload Center", 
        "📝 AI Summary", 
        "🎯 Quiz Generator", 
        "🗂️ Flashcards", 
        "🙋 Doubt Solver", 
        "⚡ Revision Notes"
    ]
    selection = st.radio("Go to", pages, label_visibility="collapsed")
    
    st.markdown("---")
    
    st.markdown("### Settings")
    st.session_state.exam_mode = st.toggle("🚀 Exam Prep Mode", value=st.session_state.exam_mode, help="Turn on for strict grading and advanced questions.")
    
    if not ai_ready:
        st.error(ai_message)
    else:
        st.success("✅ AI Engine Ready (Gemini-2.5-Flash)")

# ==========================================
# Main App Content
# ==========================================
if selection == "🏠 Home Dashboard":
    # 1. Gradient Hero Banner
    st.markdown("""
        <div class="hero-banner">
            <h1>AI Study Buddy 🎓</h1>
            <p>Your Premium Personal AI Learning Platform</p>
        </div>
    """, unsafe_allow_html=True)
    
    # Data for Analytics
    docs = 1 if st.session_state.pdf_data else 0
    summaries = 1 if st.session_state.summary else 0
    q_count = 10 if st.session_state.mcqs else 0
    f_count = 10 if st.session_state.flashcards else 0
    streak = st.session_state.study_streak
    
    # 2. Lottie & Animated Statistics Cards (Glassmorphism)
    colA, colB = st.columns([1, 2])
    
    with colA:
        lottie_url = "https://lottie.host/8c8c7288-faeb-42aa-b883-9b6261f94d07/4nKntcI8fE.json"
        lottie_json = load_lottieurl(lottie_url)
        if lottie_json:
            st_lottie(lottie_json, height=200, key="welcome")
        else:
            st.info("👋 Welcome to the ultimate study experience.")
            
    with colB:
        st.markdown("<br>", unsafe_allow_html=True)
        s1, s2 = st.columns(2)
        with s1:
            st.markdown(f'<div class="glass-card"><h3>📚 {docs}</h3><p>PDFs Processed</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card"><h3>📝 {summaries}</h3><p>Summaries</p></div>', unsafe_allow_html=True)
        with s2:
            st.markdown(f'<div class="glass-card"><h3>🎯 {q_count}</h3><p>Questions Solved</p></div>', unsafe_allow_html=True)
            st.markdown(f'<div class="glass-card"><h3>🔥 {streak}</h3><p>Day Study Streak</p></div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # 3. Plotly Analytics Dashboard
    st.markdown("### 📈 Intelligent Analytics")
    
    c1, c2 = st.columns(2)
    
    # Exam Readiness Gauge
    readiness = 0
    if docs: readiness += 25
    if summaries: readiness += 25
    if q_count: readiness += 25
    if f_count: readiness += 25
    
    with c1:
        fig_gauge = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = readiness,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Exam Readiness Score", 'font': {'color': '#e2e8f0', 'size': 20}},
            gauge = {
                'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': "darkblue"},
                'bar': {'color': "#8b5cf6"},
                'bgcolor': "rgba(0,0,0,0)",
                'borderwidth': 2,
                'bordercolor': "rgba(255,255,255,0.1)",
                'steps': [
                    {'range': [0, 33], 'color': "rgba(239, 68, 68, 0.3)"},
                    {'range': [33, 66], 'color': "rgba(234, 179, 8, 0.3)"},
                    {'range': [66, 100], 'color': "rgba(34, 197, 94, 0.3)"}],
            }
        ))
        fig_gauge.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': "#e2e8f0"}, height=350)
        st.plotly_chart(fig_gauge, use_container_width=True)
        
    # Quiz & Flashcard Performance Chart
    with c2:
        labels = ['Content Extraction', 'Summary Mastery', 'Quiz Performance', 'Flashcard Progress']
        values = [docs*100, summaries*100, (q_count/10)*100 if q_count else 0, 100 if f_count else 0]
        
        fig_bar = px.bar(x=labels, y=values, labels={'x':'Category', 'y':'Completion %'}, title="Module Completion Matrix")
        fig_bar.update_traces(marker_color='#3b82f6', marker_line_color='#8b5cf6', marker_line_width=1.5, opacity=0.8)
        fig_bar.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", font={'color': "#e2e8f0"}, height=350)
        st.plotly_chart(fig_bar, use_container_width=True)

elif selection == "📄 PDF Upload Center":
    st.title("📄 PDF Upload Center")
    st.write("Upload your study materials here to begin.")
    
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])
    
    if uploaded_file is not None:
        if st.button("Process Document", use_container_width=True):
            with st.spinner("Extracting text and calculating statistics..."):
                result = extract_text_and_stats(uploaded_file)
                if result["success"]:
                    st.session_state.pdf_data = result
                    st.success("PDF successfully processed!")
                else:
                    st.error(f"Error: {result['error']}")
                    
    if st.session_state.pdf_data:
        st.markdown("### Document Statistics")
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Pages", st.session_state.pdf_data["pages"])
        c2.metric("Word Count", st.session_state.pdf_data["words"])
        c3.metric("Key Topics Found", len(st.session_state.pdf_data["topics"]))
        
        st.markdown("**Detected Topics:**")
        for t in st.session_state.pdf_data["topics"]:
            st.markdown(f"- {t}")

elif selection == "📝 AI Summary":
    st.title("📝 AI Summary Generator")
    if not st.session_state.pdf_data:
        st.warning("Please upload a PDF first in the 'PDF Upload Center'.")
    elif not ai_ready:
        st.error("AI Engine not initialized. Check your .env file.")
    else:
        st.write("Generate intelligent summaries tailored to your needs.")
        summary_type = st.radio("Summary Depth:", ["Short & Sweet", "Detailed Breakdown", "Bullet Key Points"], horizontal=True)
        
        if st.button("Generate Summary", use_container_width=True):
            with st.spinner(f"AI is generating your {summary_type} summary..."):
                prompt = f"Provide a {summary_type} summary of the text."
                if st.session_state.exam_mode:
                    prompt += " IMPORTANT: The user is in Exam Prep Mode. Focus only on highly testable facts, formulas, and critical concepts."
                st.session_state.summary = get_gemini_response(prompt, st.session_state.pdf_data["text"])
                
        if st.session_state.summary:
            st.markdown("### Your Summary")
            st.info(st.session_state.summary)
            
            # Download as PDF
            if st.button("📥 Download as PDF"):
                pdf_path = save_as_pdf("AI Generated Summary", st.session_state.summary)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button("Click to Download PDF", pdf_file, file_name="summary.pdf", mime="application/pdf")

elif selection == "🎯 Quiz Generator":
    st.title("🎯 Quiz Generator")
    if not st.session_state.pdf_data:
        st.warning("Please upload a PDF first.")
    elif not ai_ready:
        st.error("AI Engine not initialized.")
    else:
        if st.button("Generate 10 MCQs", use_container_width=True):
            with st.spinner("AI is crafting challenging questions..."):
                st.session_state.mcqs = generate_quiz(st.session_state.pdf_data["text"])
                
        if st.session_state.mcqs:
            st.markdown("### Interactive Quiz")
            st.write(st.session_state.mcqs)
            
            if st.button("📥 Download Quiz as PDF"):
                pdf_path = save_as_pdf("Practice Quiz", st.session_state.mcqs)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button("Click to Download PDF", pdf_file, file_name="quiz.pdf", mime="application/pdf")

elif selection == "🗂️ Flashcards":
    st.title("🗂️ Flashcards")
    if not st.session_state.pdf_data:
        st.warning("Please upload a PDF first.")
    elif not ai_ready:
        st.error("AI Engine not initialized.")
    else:
        num_cards = st.slider("Number of cards to generate:", 5, 20, 10)
        if st.button("Generate Flashcards", use_container_width=True):
            with st.spinner("Building your flashcard deck..."):
                st.session_state.flashcards = generate_flashcards(st.session_state.pdf_data["text"], num_cards)
                
        if st.session_state.flashcards:
            st.markdown("### Your Deck")
            cards = st.session_state.flashcards.strip().split("\n\n")
            for i, card in enumerate(cards):
                if "Q:" in card and "A:" in card:
                    try:
                        q = card.split("A:")[0].replace("Q:", "").strip()
                        a = card.split("A:")[1].strip()
                        with st.expander(f"**Card {i+1}:** {q}"):
                            st.success(f"**Answer:** {a}")
                    except:
                        pass

elif selection == "🙋 Doubt Solver":
    st.title("🙋 Doubt Solver")
    if not st.session_state.pdf_data:
        st.warning("Please upload a PDF first.")
    elif not ai_ready:
        st.error("AI Engine not initialized.")
    else:
        user_q = st.text_input("Ask a question about your study material:")
        if st.button("Ask AI", use_container_width=True):
            if user_q:
                with st.spinner("Thinking..."):
                    prompt = f"Answer this question using only the provided context. Question: {user_q}"
                    ans = get_gemini_response(prompt, st.session_state.pdf_data["text"])
                    st.session_state.chat_history.append((user_q, ans))
                    
        for q, a in reversed(st.session_state.chat_history):
            st.markdown(f"**You:** {q}")
            st.info(f"**AI:** {a}")
            st.markdown("---")

elif selection == "⚡ Revision Notes":
    st.title("⚡ One-Click Revision Notes")
    if not st.session_state.pdf_data:
        st.warning("Please upload a PDF first.")
    elif not ai_ready:
        st.error("AI Engine not initialized.")
    else:
        st.write("Generate ultra-condensed notes designed for last-minute exam revision.")
        if st.button("Generate Cheat Sheet", use_container_width=True):
            with st.spinner("Compressing knowledge..."):
                prompt = "Create a highly condensed 'cheat sheet' or 'revision notes' from the provided text. Use bullet points, bold text for key terms, and keep it extremely brief."
                st.session_state.revision_notes = get_gemini_response(prompt, st.session_state.pdf_data["text"])
                
        if st.session_state.revision_notes:
            st.markdown(st.session_state.revision_notes)
            if st.button("📥 Download Revision Notes as PDF"):
                pdf_path = save_as_pdf("Revision Cheat Sheet", st.session_state.revision_notes)
                with open(pdf_path, "rb") as pdf_file:
                    st.download_button("Click to Download PDF", pdf_file, file_name="revision_notes.pdf", mime="application/pdf")
