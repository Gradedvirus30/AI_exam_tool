from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import chromadb
import requests

from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

os.makedirs("uploads", exist_ok=True)

app = FastAPI()

client_groq = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
# HuggingFace Embeddings
# -------------------------

HF_TOKEN = os.getenv("HF_TOKEN")

def get_embedding(text):

    API_URL = (
        "https://api-inference.huggingface.co/pipeline/feature-extraction/"
        "sentence-transformers/all-MiniLM-L6-v2"
    )

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}"
    }

    response = requests.post(
        API_URL,
        headers=headers,
        json={"inputs": text}
    )

    embedding = response.json()

    return embedding[0]


# -------------------------
# Vector Database
# -------------------------

client = chromadb.Client()

collection = client.get_or_create_collection(
    "notes"
)


# -------------------------
# AI Generation
# -------------------------

def generate_from_ai(prompt):

    completion = client_groq.chat.completions.create(
        messages=[
            {
                "role":"user",
                "content":prompt
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
        "message":"Exam Prep Assistant running"
    }


# -------------------------
# Upload PDF
# -------------------------

@app.post("/upload")
async def upload_pdf(file: UploadFile):

    file_path = f"uploads/{file.filename}"

    with open(file_path,"wb") as f:

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

    embeddings = [

        get_embedding(chunk)

        for chunk in chunks

    ]

    existing = collection.get()

    if existing["ids"]:

        collection.delete(
            ids=existing["ids"]
        )

    collection.add(
        documents=chunks,
        embeddings=embeddings,
        ids=[
            f"{file.filename}_{i}"
            for i in range(len(chunks))
        ]
    )

    return {
        "filename":file.filename,
        "total_chunks":len(chunks)
    }


# -------------------------
# Ask
# -------------------------

@app.post("/ask")
async def ask_question(data: Question):

    results = collection.query(
        query_embeddings=[
            get_embedding(data.question)
        ],
        n_results=1
    )

    context = results["documents"][0][0]

    answer = generate_from_ai(
f"""
Context:
{context}

Question:
{data.question}

Maximum 3 sentences.
"""
)

    return {
        "question":data.question,
        "answer":answer
    }


# -------------------------
# Summary
# -------------------------

@app.post("/summary")
async def generate_summary(data: SummaryRequest):

    results = collection.query(
        query_embeddings=[
            get_embedding(data.topic)
        ],
        n_results=4
    )

    context = "\n".join(
        results["documents"][0]
    )

    summary = generate_from_ai(
f"""
Context:
{context}

Create detailed exam notes.

Rules:
- 10–12 bullet points
- Include formulas if present
- Exam-oriented
"""
)

    return {
        "summary":summary
    }


# -------------------------
# Revision
# -------------------------

@app.post("/revision")
async def generate_revision(data: RevisionRequest):

    results = collection.query(
        query_embeddings=[
            get_embedding(data.topic)
        ],
        n_results=3
    )

    context = results["documents"][0][0]

    revision = generate_from_ai(
f"""
Context:
{context}

Create one-night-before-exam revision notes.
"""
)

    return {
        "revision":revision
    }


# -------------------------
# Quiz
# -------------------------

@app.post("/quiz")
async def generate_quiz(data: QuizRequest):

    results = collection.query(
        query_embeddings=[
            get_embedding(data.topic)
        ],
        n_results=3
    )

    context = "\n".join(
        results["documents"][0]
    )

    quiz = generate_from_ai(
f"""
Context:
{context}

Create:
- 3 MCQs
- 2 short questions
- 1 long question

No answers.
"""
)

    return {
        "quiz":quiz
    }


# -------------------------
# Flashcards
# -------------------------

@app.post("/flashcards")
async def generate_flashcards(data: FlashcardRequest):

    results = collection.query(
        query_embeddings=[
            get_embedding(data.topic)
        ],
        n_results=2
    )

    context = results["documents"][0][0]

    flashcards = generate_from_ai(
f"""
Context:
{context}

Create exactly 3 flashcards.

Format:

Flashcard:
Q:
A:
"""
)

    return {
        "flashcards":flashcards
    }