# AI Exam Assistant

AI Exam Assistant is a full-stack web application designed to help students study more efficiently by processing uploaded PDF notes and generating AI-powered study resources. The application enables users to interact with their study material through question answering, summaries, revision notes, quizzes, and flashcards.

## Features

- Upload PDF notes
- Ask questions based on uploaded content
- Generate detailed study summaries
- Create concise revision notes
- Generate quizzes and MCQs
- Generate flashcards
- Session-based multi-user support
- Cloud deployment for public access

## Tech Stack

### Frontend
- React
- Axios
- Vercel

### Backend
- FastAPI
- Groq API
- PyPDF
- LangChain Text Splitter
- Railway

## System Architecture

```text
User Uploads PDF
        ↓
PDF Text Extraction
        ↓
Text Chunking and Retrieval
        ↓
Groq LLM Processing
        ↓
Study Material Generation
        ↓
Frontend Display
```

## Workflow

1. Users upload PDF notes
2. The backend extracts text from uploaded documents
3. Content is split into manageable chunks
4. Session IDs isolate content for multiple users
5. Users can generate:
   - Question answers
   - Summaries
   - Revision notes
   - Quizzes
   - Flashcards

## Deployment

Frontend: Vercel

Backend: Railway

## Future Improvements

- Semantic vector search
- User authentication
- Persistent database storage
- Chat history support
- Improved retrieval ranking
- PDF highlighting and annotation

## Screenshots

Add screenshots of the application interface here.

## Author

Madhav Mohan  
Manipal Institute of Technology  
Cyber Physical Systems
