from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from save_story import generate_and_save_story  # <- Your generation logic

app = FastAPI()

# 🧾 Request body schema
class StoryRequest(BaseModel):
    prompt: str
    book_title: str
    author: str
    user_id: int
    temperature: Optional[float] = 0.8
    top_k: Optional[int] = 50

# 📥 Response schema
class StoryResponse(BaseModel):
    book_id: str
    book_path: str
    audio_path: str

@app.post("/generate-story", response_model=StoryResponse)
def generate_story(req: StoryRequest):
    try:
        book_id = str(uuid.uuid4())[:8]  # Generate story folder ID like 'a4f8c9e2'

        # 🧠 Generate + Save text/audio/story data
        text_path, audio_path = generate_and_save_story(
            prompt=req.prompt,
            book_id=book_id,  # ✅ Pass the correct ID
            user_id=req.user_id,
            author=req.author,
            book_title=req.book_title,
            temperature=req.temperature,
            top_k=req.top_k
        )

        return StoryResponse(
            book_id=book_id,
            book_path=text_path,
            audio_path=audio_path
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))