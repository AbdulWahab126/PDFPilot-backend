from pypdf import PdfReader
import json, os


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extracts and returns text from a PDF file using pypdf.

    Args:
        file_path (str): Path to the PDF file.

    Returns:
        str: Extracted text from all pages combined.
    """
    extracted_text = []

    try:
        reader = PdfReader(file_path)
        for page in reader.pages:
            text = page.extract_text()
            if text:
                extracted_text.append(text)

        return "\n".join(extracted_text).strip()

    except Exception as e:
        raise RuntimeError(f"Failed to extract text from PDF: {e}")


# DB_FILE = "/tmp/pdfpilot_store.json"


# def save_data(data):
#     with open(DB_FILE, "w") as f:
#         json.dump(data, f)


# def load_data():
#     if os.path.exists(DB_FILE):
#         with open(DB_FILE, "r") as f:
#             return json.load(f)
#     return {}
