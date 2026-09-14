import fitz  # PyMuPDF
from docx import Document


def extract_text_from_pdf(file_path):
    document = fitz.open(file_path)

    text = ""

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_text_from_docx(file_path):
    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_text_from_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# dtetct file type 
def extract_text(file_path):
    
    if file_path.lower().endswith(".pdf"):
        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith(".docx"):
        return extract_text_from_docx(file_path)

    elif file_path.lower().endswith(".txt"):
        return extract_text_from_txt(file_path)

    else:
        raise ValueError(
            "Unsupported file type. Please upload PDF, DOCX, or TXT."
        )