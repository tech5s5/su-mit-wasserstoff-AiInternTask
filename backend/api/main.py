from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import os
import shutil
from typing import List
from backend.models.embed import embed_and_store  # Import from embed.py
from backend.models.app import chat_with_user

app = FastAPI()

# CORS setup for frontend communication(Streamlit)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# PDF Upload endpoint
@app.post("/upload/")
async def upload_pdfs(user_id: str = Form(...), files: List[UploadFile] = File(...)):
    # Create directories for the user
    base_dir = os.path.join("docs", user_id)
    pdf_dir = os.path.join(base_dir, "pdfs")
    image_dir = os.path.join(base_dir,"images")
    faiss_dir = os.path.join(base_dir, "faiss_index")

    os.makedirs(pdf_dir, exist_ok=True)
    os.makedirs(image_dir,exist_ok=True)
    os.makedirs(faiss_dir, exist_ok=True)

    # Save uploaded PDFs to the user's directory
    for file in files:
        filename_lower = file.filename.lower()

        # First check filename extensions
        if filename_lower.endswith(".pdf"):
            file_path = os.path.join(pdf_dir, file.filename)
           
        elif any(filename_lower.endswith(ext) for ext in [".png", ".jpg", ".jpeg"]):
            file_path = os.path.join(image_dir, file.filename)
        # Then fall back to content-type if extension not recognized
        elif file.content_type == "application/pdf":
            file_path = os.path.join(pdf_dir, file.filename)
        elif file.content_type and file.content_type.startswith("image/"):
            file_path = os.path.join(image_dir, file.filename)
        else:
           return {"error": f"Unsupported file type: {file.filename} ({file.content_type})"}
        with open(file_path, "wb") as f:
           f.write(await file.read())

    # Process the PDFs and embed them into FAISS
    try:
        embed_and_store(user_id=user_id)
        return {"message": f"Documents uploaded and embedded successfully for user {user_id}"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

# Chat endpoint
@app.post("/chat/")
async def chat(user_id: str = Form(...), query: str = Form(...)):
    # Load the user's vectorstore and perform the query
    try:
        response = chat_with_user(user_id, query)
        return {"response": response}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
