import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from pathlib import Path
import uuid

# Load environment variables
load_dotenv()

app = FastAPI()

# Load models once and reuse them
MISTRAL_PATH = "./Mistral-7B-v0.1"
LLAMA_PATH = "./Meta-Llama-3.1-8B-Instruct"

print("🔁 Loading models... This may take a moment.")

try:
    mistral_tokenizer = AutoTokenizer.from_pretrained(MISTRAL_PATH, local_files_only=True)
    mistral_model = AutoModelForCausalLM.from_pretrained(MISTRAL_PATH, local_files_only=True)
    mistral_model.eval()
    print("✅ Mistral model loaded")
except Exception as e:
    mistral_tokenizer = None
    mistral_model = None
    print(f"❌ Failed to load Mistral model: {e}")

try:
    llama_tokenizer = AutoTokenizer.from_pretrained(LLAMA_PATH, local_files_only=True)
    llama_model = AutoModelForCausalLM.from_pretrained(LLAMA_PATH, local_files_only=True)
    llama_model.eval()
    print("✅ LLaMA model loaded")
except Exception as e:
    llama_tokenizer = None
    llama_model = None
    print(f"❌ Failed to load LLaMA model: {e}")


class GenerationRequest(BaseModel):
    prompt: str
    model: str  # 'llama' or 'mistral'
    max_tokens: int = 512
    temperature: float = 0.7


def save_story_locally(text: str, output_dir: str = "books") -> str:
    story_id = uuid.uuid4().hex
    story_folder = Path(output_dir) / f"story_{story_id}"
    story_folder.mkdir(parents=True, exist_ok=True)
    output_path = story_folder / "chapter_1.txt"
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)
    return str(output_path)


@app.post("/generate")
async def generate_story(req: GenerationRequest):
    if req.model == "mistral":
        if not mistral_model or not mistral_tokenizer:
            raise HTTPException(status_code=500, detail="Mistral model not loaded.")

        inputs = mistral_tokenizer(req.prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = mistral_model.generate(
                **inputs,
                max_new_tokens=req.max_tokens,
                temperature=req.temperature,
                do_sample=True
            )
        text = mistral_tokenizer.decode(outputs[0], skip_special_tokens=True)

    elif req.model == "llama":
        if not llama_model or not llama_tokenizer:
            raise HTTPException(status_code=500, detail="LLaMA model not loaded.")

        inputs = llama_tokenizer(req.prompt, return_tensors="pt")
        with torch.no_grad():
            outputs = llama_model.generate(
                **inputs,
                max_new_tokens=req.max_tokens,
                temperature=req.temperature,
                do_sample=True
            )
        text = llama_tokenizer.decode(outputs[0], skip_special_tokens=True)

    else:
        raise HTTPException(status_code=400, detail="Model must be 'llama' or 'mistral'")

    path = save_story_locally(text)
    return {"story_path": path, "preview": text[:500]}