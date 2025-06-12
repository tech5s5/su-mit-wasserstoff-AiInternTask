from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
load_dotenv()

#Loade LLM
os.environ['GROQ_API_KEY'] = os.getenv('GROQ_API_KEY')
llm = ChatGroq(model='llama-3.3-70b-versatile')

#Funtion for load Vector data
def load_user_vectorstore(user_id: str):
    faiss_path = os.path.join("docs", user_id, "faiss_index")
    if not os.path.exists(faiss_path):
        raise ValueError(f"No FAISS index found for user '{user_id}'")
    
    embeddings = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
    return FAISS.load_local(faiss_path, embeddings,allow_dangerous_deserialization=True)

prompt = ChatPromptTemplate.from_template("""
You are a highly skilled document research assistant.

Your task is to read the extracted document snippets provided in <context> and respond to the user's question using the following structure:

### Step 1: Document-Level Answers
Identify relevant content from each document that helps answer the question. Present the findings in a markdown table with **three columns**:
- `Document ID`: A unique identifier (e.g., DOC001, DOC002)
- `Extracted Answer`: A short but meaningful excerpt from the document (max 2–3 lines)
- `Citation`: Include "Page X, Paragraph Y" or "Page X, Sentence Y" based on metadata

Format:
Extract the document id and citation from documents and show in this format below:
---
**Document Answers Table**

| Document ID | Extracted Answer | Citation |
|-------------|------------------|----------|
| DOC001 | The company was fined under section 15A for non-compliance… | Page 3, Para 2 |
| DOC002 | The delay in reporting was noted as a violation of Clause 49… | Page 5, Para 1 |
---

### Step 2: Synthesized Summary
Next, synthesize key **themes or insights** found across the extracted answers. Group the responses by theme (e.g., "Regulatory Non-Compliance", "Disclosure Failures"). For each theme, follow this format:

**Theme Name – Short Description:**  
DOC IDs involved: Summarized insight based on their content.

Example:
**Theme 1 – Regulatory Non-Compliance:**  
DOC001, DOC002: Highlighted breaches of SEBI Act and LODR regulations.

Return the final response **in markdown format** so it can be rendered on-screen or exported to PDF.

<context>
{context}
</context>

User Question:  
{input}
""")

# Funtion for Asking any Query related to uploaded Documents
def chat_with_user(user_id:str,query:str):
    vectors = load_user_vectorstore(user_id)
    retriever = vectors.as_retriever()
    # Get top relevant documents
    retrieved_docs = retriever.get_relevant_documents(query)

    # Chaining and Retrieving the Answer from documents
    stuff_documents = create_stuff_documents_chain(llm,prompt)
    retrieval_chain = create_retrieval_chain(retriever,stuff_documents)
    response = retrieval_chain.invoke({'input':query})
    return response['answer']

