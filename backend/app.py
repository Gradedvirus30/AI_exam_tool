from fastapi import FastAPI, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

os.makedirs("uploads", exist_ok=True)

app = FastAPI()

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------
# Store chunks in memory
# ---------------------

stored_chunks=[]


# ---------------------
# Models
# ---------------------

class Question(BaseModel):
    question:str


class Topic(BaseModel):
    topic:str


# ---------------------
# AI function
# ---------------------

def generate(prompt):

    completion=client.chat.completions.create(

        messages=[
            {
                "role":"user",
                "content":prompt
            }
        ],

        model="llama-3.3-70b-versatile"

    )

    return completion.choices[0].message.content


# ---------------------
# Simple retrieval
# ---------------------

def retrieve(query):

    query_words=set(
        query.lower().split()
    )

    scores=[]

    for chunk in stored_chunks:

        chunk_words=set(
            chunk.lower().split()
        )

        overlap=len(
            query_words.intersection(
                chunk_words
            )
        )

        scores.append(
            (overlap,chunk)
        )

    scores.sort(
        reverse=True
    )

    top_chunks=[
        chunk
        for score,chunk in scores[:4]
    ]

    return "\n".join(
        top_chunks
    )


# ---------------------
# Home
# ---------------------

@app.get("/")
def home():

    return {
        "message":"AI Exam Assistant running"
    }


# ---------------------
# Upload
# ---------------------

@app.post("/upload")
async def upload(file:UploadFile):

    global stored_chunks

    file_path=f"uploads/{file.filename}"

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(
            await file.read()
        )

    reader=PdfReader(
        file_path
    )

    text=""

    for page in reader.pages:

        extracted=page.extract_text()

        if extracted:

            text+=extracted


    splitter=RecursiveCharacterTextSplitter(

        chunk_size=800,
        chunk_overlap=100

    )

    stored_chunks=splitter.split_text(
        text
    )

    return{

        "filename":file.filename,
        "chunks":len(stored_chunks)

    }


# ---------------------
# Ask
# ---------------------

@app.post("/ask")
async def ask(data:Question):

    context=retrieve(
        data.question
    )

    answer=generate(
f"""
Context:
{context}

Question:
{data.question}

Answer using only context.
"""
)

    return{
        "answer":answer
    }


# ---------------------
# Summary
# ---------------------

@app.post("/summary")
async def summary(data:Topic):

    context=retrieve(
        data.topic
    )

    output=generate(
f"""
Context:
{context}

Generate detailed study notes.
"""
)

    return{
        "summary":output
    }


# ---------------------
# Revision
# ---------------------

@app.post("/revision")
async def revision(data:Topic):

    context=retrieve(
        data.topic
    )

    output=generate(
f"""
Context:
{context}

Generate concise revision notes.
"""
)

    return{
        "revision":output
    }


# ---------------------
# Quiz
# ---------------------

@app.post("/quiz")
async def quiz(data:Topic):

    context=retrieve(
        data.topic
    )

    output=generate(
f"""
Context:
{context}

Generate:
3 MCQs
2 short questions
1 long question
"""
)

    return{
        "quiz":output
    }


# ---------------------
# Flashcards
# ---------------------

@app.post("/flashcards")
async def flashcards(data:Topic):

    context=retrieve(
        data.topic
    )

    output=generate(
f"""
Context:
{context}

Generate 3 flashcards.
"""
)

    return{
        "flashcards":output
    }