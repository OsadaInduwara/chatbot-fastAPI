from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import openai
import os
from dotenv import load_dotenv
import logging

# Load environment variables from a .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

# Set up logging
logging.basicConfig(level=logging.INFO)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

class Question(BaseModel):
    question: str

@app.post("/chat")
async def chat(question: Question):
    try:
        logging.info(f"Received question: {question.question}")
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": question.question}],
            max_tokens=50,
            n=1,
            temperature=0.7
        )
        answer = response['choices'][0]['message']['content'].strip()
        logging.info(f"Generated answer: {answer}")
        return {"answer": answer}
    except Exception as e:
        logging.error(f"Error processing question: {e}")
        raise HTTPException(status_code=500, detail=f"Error processing question: {e}")

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def get():
    with open("static/index.html") as f:
        return HTMLResponse(content=f.read(), status_code=200)
