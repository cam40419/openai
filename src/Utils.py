import os
from Client import *
from Utils import *
from Logger import Logger

logger = Logger()

context = "UTILS --> "

def extract_text_from_file(file_path: str) -> str:
    try:
        logger.log(f"{context}Extracting text from file: {file_path}")
        # Check if the file exists
        if not os.path.exists(file_path):
            logger.error(f"File does not exist: {file_path}")
            raise FileNotFoundError(f"The file {file_path} does not exist.")
        
        # Get the file extension
        file_extension = os.path.splitext(file_path)[1].lower()

        if file_extension == ".pdf":
            logger.log(f"{context}Detected file as PDF: {file_path}")
            return extract_text_from_pdf(file_path)
        elif file_extension == ".docx":
            logger.log(f"{context}Detected file as DOCX: {file_path}")
            return extract_text_from_docx(file_path)
        else:
            logger.error(f"Unsupported file type: {file_extension}")
            raise ValueError("Unsupported file type. Please provide a .pdf or .docx file.")
    except Exception as e:
        logger.error(f"An error occurred while extracting text from file: {str(e)}")
        raise e

def extract_text_from_pdf(pdf_path: str) -> str:
    try:
        logger.log(f"{context}Starting PDF text extraction: {pdf_path}")
        # Creating a PDF reader object
        reader = PdfReader(pdf_path)
        
        # Extracting text from all pages
        text = ""
        for page_num, page in enumerate(reader.pages):
            logger.log(f"{context}Extracting text from page {page_num + 1}")
            text += page.extract_text() + "\n"
        
        logger.log(f"{context}PDF text extraction complete: {pdf_path}")
        return text
    except Exception as e:
        logger.error(f"An error occurred during PDF text extraction: {str(e)}")
        raise e

def extract_text_from_docx(docx_path: str) -> str:
    try:
        logger.log(f"{context}Starting DOCX text extraction: {docx_path}")
        # Creating a docx reader object
        doc = docx.Document(docx_path)
        
        # Extracting text from all paragraphs
        text = "\n".join([para.text for para in doc.paragraphs])
        
        logger.log(f"{context}DOCX text extraction complete: {docx_path}")
        return text
    except Exception as e:
        logger.error(f"{context}An error occurred during DOCX text extraction: {str(e)}")
        raise e
