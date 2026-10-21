import fitz
from docx import Document


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF resume.
    """

    text = ""

    document = fitz.open(file_path)

    for page in document:
        text += page.get_text()

    document.close()

    return text


def extract_text_from_docx(file_path):
    """
    Extract text from a DOCX resume.
    """

    document = Document(file_path)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_resume_text(file_path):
    """
    Detect the file type and extract resume text.
    """

    if file_path.lower().endswith(".pdf"):

        return extract_text_from_pdf(file_path)

    elif file_path.lower().endswith(".docx"):

        return extract_text_from_docx(file_path)

    else:

        raise ValueError(
            "Unsupported file format. Please upload PDF or DOCX."
        )