from fastapi import FastAPI, UploadFile, File, Form, HTTPException
import os
import shutil
import uuid
from dissect_runner.run_dissect import run_dissect
from parser.parse_output import parse_and_store

app = FastAPI()

UPLOAD_DIR = "uploads"
DISSECT_OUTPUT_DIR = "dissected"

@app.post("/upload_replay/")
async def upload_replay(
    zip_file: UploadFile = File(...),
    match_type: str = Form(...)
):
    # Ensure server upload directory exists
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Save uploaded ZIP file with unique name
    file_id = uuid.uuid4().hex
    upload_filename = f"{file_id}_{zip_file.filename}"
    upload_path = os.path.join(UPLOAD_DIR, upload_filename)
    with open(upload_path, "wb") as f:
        shutil.copyfileobj(zip_file.file, f)

    # Validate ZIP archive
    if not upload_path.lower().endswith(".zip"):
        raise HTTPException(status_code=400, detail="Uploaded file must be a .zip archive containing .rec files")

    # Unpack ZIP to a temporary directory
    tmp_dir = os.path.join(UPLOAD_DIR, file_id)
    try:
        shutil.unpack_archive(upload_path, tmp_dir)
    except shutil.ReadError as e:
        raise HTTPException(status_code=400, detail=f"Invalid ZIP archive: {e}")

    # Handle case where ZIP contains a top-level folder
    entries = os.listdir(tmp_dir)
    if len(entries) == 1:
        single_path = os.path.join(tmp_dir, entries[0])
        match_dir = single_path if os.path.isdir(single_path) else tmp_dir
    else:
        match_dir = tmp_dir

    # Run the dissect tool on the match directory
    try:
        json_path = run_dissect(match_dir, DISSECT_OUTPUT_DIR)
        await parse_and_store(json_path, match_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {e}")

    return {"message": "Match processed successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
