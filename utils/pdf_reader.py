from pypdf import PdfReader
import io

def extract_text_and_stats(pdf_file):
    """
    Extracts text and calculates basic statistics from an uploaded PDF.
    Returns a dictionary with 'text', 'pages', 'words', 'topics'.
    """
    try:
        reader = PdfReader(pdf_file)
        text = ""
        num_pages = len(reader.pages)
        
        for page in reader.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"
                
        # Basic Statistics
        word_count = len(text.split())
        
        # Simple heuristic for topics (lines that look like headings)
        lines = text.split('\n')
        topics = [line.strip() for line in lines if 0 < len(line.strip()) < 50 and line.strip().istitle()][:5]
        
        return {
            "success": True,
            "text": text,
            "pages": num_pages,
            "words": word_count,
            "topics": topics if topics else ["General Concepts"]
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
