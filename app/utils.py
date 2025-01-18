import requests
from PyPDF2 import PdfReader
import google.generativeai as genai
import tempfile
import os
from .config import Config

def extract_resume_text(resume_url):
    """
    Fetches the resume from the given S3 URL and extracts text.
    :param resume_url: S3 URL pointing to the uploaded resume (PDF file).
    :return: Extracted text from the resume.
    """
    try:
        # Fetch the resume from the given URL
        response = requests.get(resume_url)
        response.raise_for_status()  # Raise an exception if the request fails

        # Create a temporary file to save the resume content
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_pdf:
            temp_pdf.write(response.content)
            temp_file_path = temp_pdf.name

        # Read the PDF content
        with open(temp_file_path, "rb") as pdf_file:
            pdf_reader = PdfReader(pdf_file)
            resume_text = "".join(page.extract_text() for page in pdf_reader.pages)

        return resume_text

    except Exception as e:
        raise RuntimeError(f"Failed to extract text from resume: {e}")

    finally:
        # Clean up the temporary file
        if 'temp_file_path' in locals() and os.path.exists(temp_file_path):
            os.remove(temp_file_path)

def generate_cover_letter(resume_url, job_description_text):
    """Generates a cover letter using the GenAI API."""
    genai.configure(api_key=Config.GENAI_API_KEY)
    model = genai.GenerativeModel("gemini-1.5-flash")

    # Extract text from the resume
    resume_text = extract_resume_text(resume_url)

    prompt = f"""
    Write a compelling cover letter for a job application based on the following:

    **Resume:**
    {resume_text}

    **Job Description:**
    {job_description_text}

    The cover letter should be concise, professional, and tailored to the specific job requirements. 
    It should highlight relevant skills and experiences from the resume that match the job description.
    """

    response = model.generate_content(prompt)
    return response.text
