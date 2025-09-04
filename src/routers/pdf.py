from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import uuid as uuid_pkg
import os

from src.data_store import data_store
from src.utils.extract_text_from_pdf import extract_text_from_pdf
from src.utils.llm_client import query_llm

router = APIRouter()

UPLOAD_DIR = "/tmp/cag_uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@router.post("/upload/{uuid}", status_code=201)
def upload_pdf(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):
    """
    Upload a new PDF under a specific UUID: the endpoint ingests the file, extracts its full text, persists both the original bytes and the text against the provided UUID, and returns a summary of the stored document; if the UUID is already taken, it immediately responds with 409 Conflict to prevent accidental overwrites.
    """

    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDF accepted."
        )

    uuid_str = str(uuid)

    if uuid_str in data_store:
        raise HTTPException(status_code=409, detail="This file is already exists")

    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_{file.filename}")

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        extracted_text = extract_text_from_pdf(file_path)

        if extracted_text is None:
            raise HTTPException(
                status_code=500, detail="Extraction failed. File is empty"
            )

        data_store[uuid_str] = extracted_text

        return {
            "message": "File uploaded and text extracted successfully",
            "uuid": uuid_str,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {e}")


@router.put("/update/{uuid}", status_code=201)
def update_pdf(uuid: uuid_pkg.UUID, file: UploadFile = File(...)):
    """
    Appends the new data in the existing pdf
    """
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid file type. Only PDF accepted."
        )

    uuid_str = str(uuid)

    if uuid_str not in data_store:
        raise HTTPException(status_code=404, detail="This file does not exists.")

    file_path = os.path.join(UPLOAD_DIR, f"{uuid_str}_{file.filename}")

    try:
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        new_text = extract_text_from_pdf(file_path)

        if new_text is None:
            raise HTTPException(
                status_code=500, detail="Extraction failed. File is empty"
            )

        data_store[uuid_str] += new_text
        return {
            "message": "File updated successfully",
            "uuid": uuid_str,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to extract text: {e}")


@router.get("/query/{uuid}")
def get_pdf(uuid: uuid_pkg.UUID, query: str = Query(..., min_length=1)):
    """
    Get the stored text against a given uuid and send it along with a query to a placeholder LLM service. Returns the placeholder response
    """
    uuid_str = str(uuid)

    if uuid_str not in data_store:
        raise HTTPException(status_code=404, detail="This file does not exists.")

    stored_text = data_store[uuid_str]

    # Combine context with user query
    prompt = f"Context:\n{stored_text}\n\nUser query: {query}\nAnswer:"

    llm_response = query_llm(prompt)

    return {"uuid": uuid_str, "query": query, "response": llm_response}
