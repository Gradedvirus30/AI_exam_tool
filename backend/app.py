from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb
import requests

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

os.makedirs("uploads", exist_ok=True)

app = FastAPI()

client_groq = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


class FlashcardRequest(BaseModel):
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
# Shared AI Function
# -------------------------

def generate_from_ollama(prompt):

    completion = client_groq.chat.completions.create(

        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],

        model="llama-3.3-70b-versatile"

    )

    return completion.choices[0].message.content


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
        n_results=4
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

Create detailed exam notes.

Rules:
- 10–12 bullet points
- Include definitions
- Include important concepts
- Include important formulas if available
- Include key facts students should remember
- Use only context
- Keep the explanation exam-oriented
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


# -------------------------
# Revision
# -------------------------

@app.post("/revision")
async def generate_revision(data: RevisionRequest):

    results = collection.query(
        query_texts=[data.topic],
        n_results=3
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
- 10–12 bullet points
- Include definitions
- Include important concepts
- Include important formulas if available
- Include key facts students should remember
- Use only context
- Keep the explanation exam-oriented
"""

    revision = generate_from_ollama(
        prompt
    )

    return {

        "topic": data.topic,
        "revision": revision

    }


# -------------------------
# Flashcards
# -------------------------

@app.post("/flashcards")
async def generate_flashcards(data: FlashcardRequest):

    results = collection.query(
        query_texts=[data.topic],
        n_results=2
    )

    if not results["documents"][0]:

        return {
            "error": "No matching notes found"
        }

    context = results["documents"][0][0]

    prompt = f"""
Context:
{context}

Create flashcards.

Format exactly:

Flashcard 1:
Q:
A:

Flashcard 2:
Q:
A:

Flashcard 3:
Q:
A:

Rules:
- Exactly 3 flashcards
- Answers maximum 1 sentence
- Use only context
- Keep concise
"""

    flashcards = generate_from_ollama(
        prompt
    )

    return {

        "topic": data.topic,
        "flashcards": flashcards

    }