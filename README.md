
# 🤖 Chat with Your Documents – LangChain-powered AI Assistant

Welcome to **Chat with Your Documents** — an intelligent, document-aware chatbot application that allows users to upload PDFs and images, extract content (with OCR support), and **interact with the documents using natural language**.

> 🔗 **Live App**: [https://tech5-chatbot-frontend.hf.space](https://tech5-chatbot-frontend.hf.space)

---

## 🌟 Features

✨ Upload **multiple documents** (PDFs and images)  
✨ Automatically extract and index text using **OCR and NLP**  
✨ Query documents using **natural language questions**  
✨ Get **contextual, accurate responses** with citations  
✨ Powered by **LangChain**, **FAISS**, and **HuggingFace Embeddings**

---

## 🧰 Tech Stack

| Layer       | Technology                |
|-------------|----------------------------|
| 🧠 LLM Logic | LangChain + Groq (or any LLM API) |
| 🔍 Embedding | HuggingFace Transformers (`all-MiniLM-L6-v2`) |
| 📚 Vector DB | FAISS (per-user vector store) |
| 📝 OCR       | Pytesseract + PIL (image to text) |
| ⚙️ Backend   | FastAPI (document upload, indexing, chat API) |
| 🖥 Frontend  | Streamlit (file upload + chatbot UI) |
| 🌐 Hosting   | Hugging Face Spaces (Frontend + Backend Dockerized separately) |

---

## 📁 Folder Structure

```bash
chatbot/
├── backend/           # FastAPI backend
│   ├── api/
│   │   └── main.py
│   └── models/
│       ├── embed.py   # Embedding logic
│       └── app.py     # Chat function
├── frontend/
│   └── streamlit.py         # Streamlit app
