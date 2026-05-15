import PyPDF2

def extract_text_from_pdf(file_obj) -> str:
    """Extracts text from an uploaded PDF file object."""
    try:
        reader = PyPDF2.PdfReader(file_obj)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def read_file_content(uploaded_file) -> str:
    """Reads content from an uploaded Streamlit file."""
    if uploaded_file.name.endswith(".pdf"):
        return extract_text_from_pdf(uploaded_file)
    else:
        # Assume it's a text file
        return uploaded_file.getvalue().decode("utf-8")
