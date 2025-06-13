# api.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
from generate_story import generate_next_chapter

app = FastAPI()

class StoryPrompt(BaseModel):
    prompt: str

@app.post("/generate_chapter")
async def generate_chapter(prompt: StoryPrompt):
    chapter_text = generate_next_chapter(prompt.prompt)
    return {"content": chapter_text}
