from fastapi import FastAPI, UploadFile
from pydantic import BaseModel
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
import requests

app = FastAPI()


# -------------------------
# Request Models
# -------------------------

class Question(BaseModel):
    question: str


class SummaryRequest(BaseModel):
    topic: str


# -------------------------
# Load Embedding Model
# -------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -------------------------
# Create Vector Database
# -------------------------

client = chromadb.Client()

collection = client.get_or_create_collection(
    "notes"
)


# -------------------------
# Home Route
# -------------------------

@app.get("/")
def home():

    return {
        "message": "Exam Prep Assistant running"
    }


# -------------------------
# Upload PDF
# -------------------------

@app.post("/upload")
async def upload_pdf(file: UploadFile):

    file_path = f"uploads/{file.filename}"

    # Save uploaded file
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # Read PDF
    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    # Split text into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    # Create embeddings
    embeddings = embedding_model.encode(
        chunks
    )

    # Clear previous notes
    existing = collection.get()

    if existing["ids"]:

        collection.delete(
            ids=existing["ids"]
        )

    # Store new notes
    collection.add(
        documents=chunks,
        embeddings=embeddings.tolist(),
        ids=[
            f"{file.filename}_{i}"
            for i in range(len(chunks))
        ]
    )

    return {

        "filename": file.filename,
        "total_chunks": len(chunks),
        "embeddings_created": len(embeddings)

    }


# -------------------------
# Ask Questions
# -------------------------

@app.post("/ask")
async def ask_question(data: Question):

    results = collection.query(
        query_texts=[data.question],
        n_results=1
    )

    context = results["documents"][0][0]

    prompt = f"""
Context:
{context}

Question:
{data.question}

Rules:
- Answer only from context
- Maximum 3 sentences
- Keep concise
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
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


# -------------------------
# Generate Summary
# -------------------------

@app.post("/summary")
async def generate_summary(data: SummaryRequest):

    results = collection.query(
        query_texts=[data.topic],
        n_results=2
    )

    context = "\n".join(
        results["documents"][0]
    )

    prompt = f"""
Context:
{context}

Generate short exam notes.

Rules:
- Maximum 6 bullet points
- Use ONLY information from context
- Do not add outside knowledge
- Keep concise
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "phi3:mini",
            "prompt": prompt,
            "stream": False,
            "keep_alive": "10m"
        }
    )

    summary = response.json()["response"]

    return {
        "topic": data.topic,
        "summary": summary
    }