from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
import requests

app = FastAPI()


# Request model
class Question(BaseModel):
    question: str


# Load embedding model
embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Create/load vector database
client = chromadb.Client()

collection = client.get_or_create_collection(
    "notes"
)


@app.get("/")
def home():

    return {
        "message": "Exam Prep Assistant running"
    }


@app.post("/upload")
async def upload_pdf(file: UploadFile):

    # Save uploaded PDF
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Read PDF
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    # Split text
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    # Create embeddings
    embeddings = embedding_model.encode(
        chunks
    )

    # Store in database
    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=[str(i) for i in range(len(chunks))]
    )

    return {
        "filename": file.filename,
        "total_chunks": len(chunks),
        "embeddings_created": len(embeddings)
    }


@app.post("/ask")
async def ask_question(data: Question):

    # Find relevant chunks
    results = collection.query(
        query_texts=[data.question],
        n_results=3
    )

    context = "\n".join(
        results["documents"][0]
    )

    # Prompt for Ollama
    prompt = f"""
Context:
{context}

Question:
{data.question}

Explain clearly for an engineering student.
"""

    # Send to Ollama
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False,
            "keep_alive": "10m"
        }
    )

    answer = response.json()["response"]

    return {
        "question": data.question,
        "answer": answer
    }