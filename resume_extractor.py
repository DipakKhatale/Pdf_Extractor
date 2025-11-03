import fitz  # PyMuPDF
import pytesseract
from PIL import Image
import io
import re
import pandas as pd
import os

# Set Tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# ---------- Extract text from PDF (scanned or digital) ----------
def extract_text_from_pdf(pdf_path):
    text = ""
    doc = fitz.open(pdf_path)

    for page in doc:
        # Try to extract text normally
        page_text = page.get_text("text")
        if page_text.strip():
            text += page_text
        else:
            # If no text found, convert to image and use OCR
            pix = page.get_pixmap()
            img = Image.open(io.BytesIO(pix.tobytes("png")))
            text += pytesseract.image_to_string(img)
    return text

# ---------- Example Test ----------
#if __name__ == "__main__":
#    text = extract_text_from_pdf("test.pdf")   # <---- your test file here
#    print(text)

# ---------- Extract structured info ----------
def extract_info(text):
    info = {}
    
    # Name (basic pattern)
    name_pattern = re.compile(r"([A-Z][a-z]+(?: [A-Z][a-z]+)+)")
    info['Name'] = name_pattern.findall(text)[0] if name_pattern.findall(text) else "Not Found"

    # Email
    email_pattern = re.compile(r"[\w\.-]+@[\w\.-]+\.\w+")
    info['Email'] = email_pattern.findall(text)[0] if email_pattern.findall(text) else "Not Found"

    # Mobile
    phone_pattern = re.compile(r'(\+?\d{1,3}[-.\s]?\d{10})')
    info['Mobile'] = phone_pattern.findall(text)[0] if phone_pattern.findall(text) else "Not Found"

    # Education
    education_pattern = re.compile(r"(B\.?Tech|B\.?E\.?|M\.?Tech|M\.?E\.?|B\.?Sc|M\.?Sc|MBA|Ph\.?D)", re.IGNORECASE)
    educations = education_pattern.findall(text)
    info['Education'] = ', '.join(set(educations)) if educations else "Not Found"

    # Experience
    exp_pattern = re.compile(r'(\d+)\s*(?:years?|yrs?)', re.IGNORECASE)
    exp = exp_pattern.findall(text)
    info['Experience'] = exp[0] + " years" if exp else "Not Found"

    return info

# ---------- Process all PDFs in folder ----------
def process_resumes(input_folder):
    data = []
    for file in os.listdir(input_folder):
        if file.endswith(".pdf"):
            pdf_path = os.path.join(input_folder, file)
            print(f"Processing: {file}")
            text = extract_text_from_pdf(pdf_path)
            info = extract_info(text)
            info['Filename'] = file
            data.append(info)

    df = pd.DataFrame(data)
    df.to_excel("extracted_resumes.xlsx", index=False)
    print("\n✅ Extraction Completed! Results saved in extracted_resumes.xlsx")

# ---------- Run ----------
if __name__ == "__main__":
    folder = "resumes"  # create this folder and put your test PDFs
    process_resumes(folder)
