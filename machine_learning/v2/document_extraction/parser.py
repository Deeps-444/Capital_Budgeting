"""
Document Parser for the V2 Capital Budgeting DSS.

Purpose
-------
Convert supported project documents into plain text.

Supported formats
-----------------
- PDF
- DOCX
- TXT

This module is intentionally independent of Gemini or any
project-specific extraction logic.

Data flow
---------
Uploaded document
        ↓
    parser.py
        ↓
    Plain text
        ↓
document extractor
        ↓
Structured ProjectDetails
"""

import os

import fitz  # PyMuPDF
from docx import Document


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract text from all pages of a PDF document.

    Parameters
    ----------
    file_path : str
        Path to the PDF file.

    Returns
    -------
    str
        Combined text extracted from all pages.
    """

    document = fitz.open(file_path)

    pages = []

    for page in document:
        pages.append(page.get_text())

    document.close()

    return "\n".join(pages)


def extract_text_from_docx(file_path: str) -> str:
    """
    Extract text from paragraphs of a DOCX document.

    Parameters
    ----------
    file_path : str
        Path to the DOCX file.

    Returns
    -------
    str
        Combined document text.
    """

    document = Document(file_path)

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def extract_text_from_txt(file_path: str) -> str:
    """
    Read plain text from a TXT file.

    Parameters
    ----------
    file_path : str
        Path to the TXT file.

    Returns
    -------
    str
        File contents.
    """

    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def parse_document(file_path: str) -> str:
    """
    Detect the document format and extract its text.

    The parser only handles document-to-text conversion.
    It does not perform any interpretation or extraction of
    project attributes.

    Parameters
    ----------
    file_path : str
        Path to the uploaded document.

    Returns
    -------
    str
        Extracted plain text.

    Raises
    ------
    ValueError
        If the file format is unsupported.
    FileNotFoundError
        If the supplied file does not exist.
    """

    if not os.path.exists(file_path):
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    if extension == ".docx":
        return extract_text_from_docx(file_path)

    if extension == ".txt":
        return extract_text_from_txt(file_path)

    raise ValueError(
        f"Unsupported document format: {extension}"
    )