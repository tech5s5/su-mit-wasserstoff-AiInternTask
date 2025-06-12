import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "https://document-research-and-theme-7fmd.onrender.com")

# Full API endpoints
BACKEND_URL_UPLOAD = f"{BACKEND_URL}/upload/"
BACKEND_URL_CHAT = f"{BACKEND_URL}/chat/"
# Streamlit UI setup
st.title("Chat with your documents")

# Get user ID 
user_id = st.text_input("Enter your User ID")

# PDF file and Images upload
uploaded_files = st.file_uploader("Upload PDF(s) and Images", type=["pdf", "png", "jpg", "jpeg"], accept_multiple_files=True)

# Handling PDF upload
if st.button("Upload PDFs and Images"):
    if user_id and uploaded_files:
        try:
            # Prepare the files for uploading
            files = [("files", (file.name, file, "application/pdf")) for file in uploaded_files]
            data = {"user_id": user_id}

            # Send the uploaded files to FastAPI for processing and embedding
            response = requests.post(BACKEND_URL_UPLOAD, data=data, files=files)

            if response.status_code == 200:
                st.success(f"Successfully uploaded and processed {len(uploaded_files)} Documents.")
            else:
                st.error(f"Failed to upload PDFs. Status code: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter a User ID and upload PDFs.")

# Query input
query = st.text_area("Ask a question")

# Handling chat functionality
if st.button("Send Query"):
    if user_id and query:
        try:
            # Send the user query to FastAPI for chat processing
            response = requests.post(BACKEND_URL_CHAT, data={"user_id": user_id, "query": query})
            
            if response.status_code == 200:
                response_json = response.json()
                st.write(f"Response: {response_json['response']}")
            else:
                st.error("Failed to get a response from the backend.")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    else:
        st.warning("Please enter both User ID and a query.")
