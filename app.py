import gradio as gr
import os
import requests
from PyPDF2 import PdfReader
from docx import Document
import pyperclip
from fpdf import FPDF
import tempfile
from datetime import date

# Ensure the API key is set up appropriately
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

from fpdf import FPDF

def sanitize_text(text):
    return text.encode('latin-1', 'ignore').decode('latin-1')

class PDFGenerator:
    def __init__(self):
        self.pdf = FPDF(format='A4')
        self.pdf.add_page()
        self.pdf.set_auto_page_break(auto=True, margin=15)
        self.pdf.set_font("Arial", size=11)
        self.pdf.set_left_margin(20)
        self.pdf.set_right_margin(20)
        self.pdf.set_top_margin(20)

    def add_text(self, cover_letter_content):
        self.pdf.set_font("Arial", "B", size=11)
        self.pdf.ln(10)
        
        self.pdf.cell(w=0, h=10, txt="Cover Letter", align='C')
        self.pdf.ln(20)
        
        self.pdf.set_font("Helvetica", size=11)
        paragraphs = cover_letter_content.split("\n\n")
    
        for paragraph in paragraphs:
            sanitized_paragraph = sanitize_text(paragraph)  # Sanitize each paragraph
            self.pdf.multi_cell(0, 5, sanitized_paragraph)
            self.pdf.ln(2)

    def save_pdf(self, file_path):
        self.pdf.output(file_path)


def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def extract_text_from_docx(docx_file):
    doc = Document(docx_file)
    text = ""
    for para in doc.paragraphs:
        text += para.text + "\n"
    return text

def analyze_and_generate(resume, job_description):
    file_type = resume.split('.')[-1].lower()
    if file_type == 'pdf':
        resume_text = extract_text_from_pdf(resume)
    elif file_type == 'docx':
        resume_text = extract_text_from_docx(resume)
    else:
        return "Unsupported file type. Please upload a PDF or DOCX file."

    # Ensure the API key is set
    if not GOOGLE_API_KEY:
        return "Google API Key is not set."

    # Perform resume analysis and cover letter generation
    analysis_prompt = f"""
        Please analyze the following resume in the context of the job description provided. 
        Strictly check every single line in the job description and analyze my resume to see whether there is a match. 
        Maintain high ATS standards and give scores only for the correct matches. 
        Focus on hard skills and soft skills that are missing, and provide the following details:
        1. The match percentage of the resume to the job description. You *MUST* Display the match percentage as "*Match Percentage:__.__%*".
        2. A list of missing keywords that are accurate.
        3. Final thoughts on the resume's overall match with the job description in three lines.
        4. Recommendations on how to add the missing keywords and improve the resume in 3-4 points with examples.
        Display the results in the order specified and do not mention the numbers explicitly. 
        Job Description: {job_description}
        Resume: {resume_text}
    """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {"role": "user", "parts": [{"text": analysis_prompt}]}
        ]
    }

    # Make the POST request to the AI model
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()


    analysis_result = ""
    if "candidates" in response_data:
        for candidate in response_data["candidates"]:
            if "content" in candidate and "parts" in candidate["content"]:
                for part in candidate["content"]["parts"]:
                    analysis_result = part["text"]  # Return the analysis result

    # Now generate the cover letter text
    coverletter_prompt = f"""
        Your task is to generate a personalized cover letter tailored for a specific job application using the candidate's resume and the job description provided. The cover letter should be engaging, relevant, and highlight key skills and experiences that align with the job requirements.

        Please fill in all details directly from the resume and job description, avoiding any placeholders such as [Your Name] or [Company Address]. If any specific information, such as the recruiter's name or company address, is not provided, infer typical names or leave them blank in a natural way, ensuring no brackets are included in the output.
        
        **Do not include this "as advertised on [Platform where you saw the job posting] or (Address inferred, not available in provided text)" sentence at all.** Do not include this line at any cost.

        *Candidate Information Extraction*:
        Analyze the candidate’s resume to extract:
        - Full name, address, phone number, and email.
        - Key skills and experiences related to the job.
        - Notable achievements and contributions.
        - Relevant education and certifications.
        - Professional values and career aspirations.
        
        *Job Description Analysis*:
        Examine the job description to identify:
        - Company name, role title, and main recruiter’s name if available.
        - Core skills and qualifications required.
        - Primary responsibilities and expectations.
        - Company’s mission and values that resonate with the candidate's profile.
        
        Structure the cover letter using the following sections:
        - Introduction: Craft a strong opening that captures attention and specifically mentions the position title and the company’s name.
        - Body: Discuss how the candidate’s skills and experiences make them an ideal fit for the job. Highlight specific technical and soft skills that align with the job requirements.
        - Conclusion: Reiterate interest in the position, express desire for an interview, and include a professional closing statement.

        Ensure clarity, coherence, and brevity throughout the letter. Do not leave any placeholders. Always mention the current date as {date.today()}.
        
        Data to generate the cover letter:
        - Resume: {resume_text}
        - Job Description: {job_description}
        """

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key={GOOGLE_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [
            {"role": "user", "parts": [{"text": coverletter_prompt}]}
        ]
    }

    # Make the POST request to the AI model
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()


    coverletter_result = ""
    if "candidates" in response_data:
        for candidate in response_data["candidates"]:
            if "content" in candidate and "parts" in candidate["content"]:
                for part in candidate["content"]["parts"]:
                    coverletter_result = part["text"]  # Return the analysis result

    # Format results with headings
    coverletter_result = coverletter_result.replace("\u2019", "'").replace("\u2018", "'")
    
    formatted_analysis = f"**Analysis:**\n\n{analysis_result}"
    formatted_cover_letter = f"**Cover Letter:**\n\n{coverletter_result}"

    # Temporary file for the cover letter PDF
    temp_file = os.path.join(tempfile.gettempdir(), "cover_letter.pdf")
    pdf_generator = PDFGenerator()
    pdf_generator.add_text(coverletter_result)
    pdf_generator.save_pdf(temp_file)

    return formatted_analysis, formatted_cover_letter, temp_file

def paste_clipboard_content():
    try:
        return pyperclip.paste()
    except pyperclip.PyperclipException as e:
        print("Error accessing clipboard:", e)
        return ""

def create_ui():
    with gr.Blocks() as ui:
        gr.Markdown("# ATS Resume Analysis and Cover Letter Generator")

        with gr.Row():
            with gr.Column():
                job_description = gr.Textbox(
                    label="Job Description",
                    placeholder="Enter the job description here...",
                    lines=3, max_lines=3
                )
                #paste_button = gr.Button("Paste")

                #paste_button.click(fn=paste_clipboard_content,inputs=None,outputs=job_description)

            with gr.Column():
                resume_input = gr.File(
                    label="Upload your resume (PDF or DOCX)",
                    type="filepath"
                )

        analyze_button = gr.Button("Analyze Resume and Generate Cover Letter", size="lg")
        analysis_result_output = gr.Markdown(label="Analysis Result")
        cover_letter_output = gr.Markdown(label="Generated Cover Letter")
        download_button = gr.File(label="Download Cover Letter as PDF", show_label=True)

        analyze_button.click(
            fn=analyze_and_generate,
            inputs=[resume_input, job_description],
            outputs=[analysis_result_output, cover_letter_output, download_button]
        )

    return ui

if __name__ == "__main__":
    ui = create_ui()
    ui.launch()