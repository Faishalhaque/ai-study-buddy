from utils.ai_engine import get_gemini_response
from fpdf import FPDF
import tempfile
import os

def generate_quiz(context):
    """Generates 10 MCQs based on the context."""
    prompt = """
    Generate exactly 10 Multiple Choice Questions (MCQs) based on the provided text. 
    Format requirements:
    - Number each question clearly.
    - Provide 4 options (A, B, C, D) for each.
    - Clearly state the correct answer.
    - Provide a short explanation for the correct answer.
    """
    return get_gemini_response(prompt, context)

def generate_flashcards(context, num_cards=10):
    """Generates Q&A flashcards."""
    prompt = f"""
    Generate exactly {num_cards} flashcards from the provided text focusing on the most important concepts. 
    Format them strictly as follows for easy parsing:
    Q: [The Question]
    A: [The Answer]
    
    Do not use any other formatting. Separate each flashcard with a blank line.
    """
    return get_gemini_response(prompt, context)

def save_as_pdf(title, content):
    """Saves text content as a PDF file and returns the temporary file path."""
    pdf = FPDF()
    pdf.add_page()
    
    # Use built-in Arial or Helvetica to avoid external font file requirements
    pdf.set_font("Helvetica", size=12)
    
    pdf.set_font("Helvetica", style="B", size=16)
    pdf.cell(200, 10, txt=title, ln=True, align='C')
    pdf.ln(10)
    
    pdf.set_font("Helvetica", size=12)
    
    # Handle unicode characters gracefully by replacing them since FPDF standard fonts only support Latin-1
    safe_content = content.encode('latin-1', 'replace').decode('latin-1')
    pdf.multi_cell(0, 10, txt=safe_content)
    
    # Create temp file
    temp_fd, temp_path = tempfile.mkstemp(suffix=".pdf")
    os.close(temp_fd)
    
    pdf.output(temp_path)
    return temp_path
