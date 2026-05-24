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


class QuizRequest(BaseModel):
    topic: str

class RevisionRequest(BaseModel):
    topic: str


# -------------------------
# Embedding Model
# -------------------------

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# -------------------------
# Vector Database
# -------------------------

client = chromadb.Client()

collection = client.get_or_create_collection(
    "notes"
)


# -------------------------
# Shared Ollama Function
# -------------------------

def generate_from_ollama(prompt):

    try:

        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:mini",
                "prompt": prompt,
                "stream": False,
                "keep_alive": "10m"
            },
            timeout=60
        )

        response.raise_for_status()

        result = response.json()

        return result["response"]

    except Exception as e:

        return f"Error from Ollama: {str(e)}"


# -------------------------
# Home
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

    with open(file_path, "wb") as f:
        f.write(await file.read())

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        extracted = page.extract_text()

        if extracted:
            text += extracted

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100
    )

    chunks = splitter.split_text(text)

    embeddings = embedding_model.encode(
        chunks
    )

    existing = collection.get()

    if existing["ids"]:

        collection.delete(
            ids=existing["ids"]
        )

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

    if not results["documents"][0]:

        return {
            "error": "No matching notes found"
        }

    context = results["documents"][0][0]

    prompt = f"""
Context:
{context}

Question:
{data.question}

Rules:
- Maximum 3 sentences
- Answer only from context
"""

    answer = generate_from_ollama(
        prompt
    )

    return {

        "question": data.question,
        "answer": answer

    }


# -------------------------
# Summary
# -------------------------

@app.post("/summary")
async def generate_summary(data: SummaryRequest):

    results = collection.query(
        query_texts=[data.topic],
        n_results=2
    )

    if not results["documents"][0]:

        return {
            "error": "No matching notes found"
        }

    context = "\n".join(
        results["documents"][0]
    )

    prompt = f"""
Context:
{context}

Generate short exam notes.

Rules:
- Maximum 6 bullet points
- Use only information from context
- Keep concise
"""

    summary = generate_from_ollama(
        prompt
    )

    return {

        "topic": data.topic,
        "summary": summary

    }


# -------------------------
# Quiz
# -------------------------

@app.post("/quiz")
async def generate_quiz(data: QuizRequest):

    results = collection.query(
        query_texts=[data.topic],
        n_results=2
    )

    if not results["documents"][0]:

        return {
            "error": "No matching notes found"
        }

    context = "\n".join(
        results["documents"][0]
    )

    prompt = f"""
Context:
{context}

You MUST generate exactly:

MCQ 1:
Question:
A)
B)
C)
D)

MCQ 2:
Question:
A)
B)
C)
D)

MCQ 3:
Question:
A)
B)
C)
D)

Short Question 1:

Short Question 2:

Long Question:

IMPORTANT:
- Do not skip any section
- Create all 6 questions
- No answers
- Use only context information
- If context is limited, still create all sections
"""

    quiz = generate_from_ollama(
        prompt
    )

    return {
        "topic": data.topic,
        "quiz": quiz
    }

@app.post("/revision")
async def generate_revision(data: RevisionRequest):

    results = collection.query(
        query_texts=[data.topic],
        n_results=1
    )

    if not results["documents"][0]:

        return {
            "error": "No matching notes found"
        }

    context = results["documents"][0][0]

    prompt = f"""
Context:
{context}

Create a one-night-before-exam revision sheet.

Rules:
- Important concepts
- Must remember points
- Exam tips
- Maximum 6 bullet points
- Keep concise
- Use only context
"""

    revision = generate_from_ollama(
        prompt
    )

    return {

        "topic": data.topic,
        "revision": revision

    }