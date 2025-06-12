from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
import os
import shutil
from PIL import Image
import pytesseract


# Funtion for load Documents and Save it into Vector Stores
def embed_and_store(user_id: str):
    # Setup user directories
    base_dir = os.path.join("docs", user_id)
    pdf_dir = os.path.join(base_dir, "pdfs")
    image_dir = os.path.join(base_dir,"images")
    faiss_dir = os.path.join(base_dir, "faiss_index")

    #Using Pytesseract for extracting Image texts
    image_texts = []
    for filename in os.listdir(image_dir):
        if filename.lower().endswith((".png", ".jpg", ".jpeg")):
            image_path = os.path.join(image_dir, filename)
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            image_texts.append((filename, text))
    doc_images = [Document(page_content=text, metadata={"source": fname}) for fname, text in image_texts] 
    
    # Loade Pdfs using PyPDFDirectoryLoader
    loader = PyPDFDirectoryLoader(pdf_dir)
    docs = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=2000,chunk_overlap=200)
    document = splitter.split_documents(docs)
    documents = document + doc_images
    updated_documents = []
    for i, doc in enumerate(documents):
        meta = doc.metadata.copy()
    
        meta["doc_id"] = meta.get("source", f"doc_{i}")  # Use filename or fallback
        meta["chunk_id"] = i

    # If page number available (for PDF)
        if "page" in meta:
            meta["citation"] = f"{meta['source']} - page {meta['page']}, chunk {i}"
        else:
            meta["citation"] = f"{meta['source']} - chunk {i}"

        updated_documents.append(Document(page_content=doc.page_content, metadata=meta))
    # Load HuggingFace Embedding model 
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')

     #Load existing FAISS index if exists
    if os.path.exists(os.path.join(faiss_dir, "index.faiss")):
        vectorstore = FAISS.load_local(faiss_dir, embeddings, allow_dangerous_deserialization=True)
        vectorstore.add_documents(updated_documents)
    else:
        vectorstore = FAISS.from_documents(updated_documents, embeddings)

    vectorstore.save_local(faiss_dir)
    print(f"✅ FAISS updated for user: {user_id}")

