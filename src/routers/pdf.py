from fastapi import APIRouter, UploadFile, File, HTTPException, Query
import uuid as uuid_pkg
import os

import data_store

router = APIRouter()


@router.post("/upload/{uuid}", status_code=201)
def upload_pdf(uuid: uuid_pkg.UUID, file: UploadFile = File):
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
    
    

    return
