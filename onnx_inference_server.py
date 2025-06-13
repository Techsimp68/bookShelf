from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer
import onnxruntime as ort
import numpy as np
import os

from eleven_narration import generate_narration
from dotenv import load_dotenv
load_dotenv()
# Example use
generate_narration("Elara stepped into the ruins...", voice="Rachel", out_path="audio/Elara/intro.mp3")

app = FastAPI()

# 🔁 Load tokenizer and ONNX model
onnx_model_path = "./onnx/gpt2/model.onnx"
tokenizer_path = "./onnx/gpt2"
tokenizer = AutoTokenizer.from_pretrained(tokenizer_path)
session = ort.InferenceSession(onnx_model_path)

# 📤 Request schema
class InferenceRequest(BaseModel):
    prompt: str
    max_length: int = 500
    temperature: float = 1.0
    top_k: int = 50

# 📥 Response schema
class InferenceResponse(BaseModel):
    output: str

# 🧠 Sampling helper
def sample_from_logits(logits, temperature=1.0, top_k=50):
    logits = logits[0] / temperature
    top_k = min(top_k, logits.shape[-1])
    top_k_indices = np.argpartition(logits, -top_k)[-top_k:]
    top_k_logits = logits[top_k_indices]

    # Softmax
    probs = np.exp(top_k_logits - np.max(top_k_logits))
    probs /= np.sum(probs)

    sampled_index = np.random.choice(len(top_k_indices), p=probs)
    return np.array([[top_k_indices[sampled_index]]], dtype=np.int64)

@app.post("/generate", response_model=InferenceResponse)
def generate_text(req: InferenceRequest):
    try:
        input_ids = tokenizer(req.prompt, return_tensors="np")["input_ids"]
        generated_ids = input_ids.copy()
        paragraph_count = 0
        max_paragraphs = 4

        for _ in range(req.max_length):
            attention_mask = np.ones_like(generated_ids)
            position_ids = np.arange(generated_ids.shape[1]).reshape(1, -1).astype(np.int64)

            # Run inference
            outputs = session.run(
                None,
                {
                    "input_ids": generated_ids,
                    "attention_mask": attention_mask,
                    "position_ids": position_ids,
                }
            )

            next_token_logits = outputs[0][:, -1, :]

            # Apply basic repetition penalty
            for token in set(generated_ids[0]):
                next_token_logits[0, token] -= 1.0

            # Sample next token
            next_token_id = sample_from_logits(
                next_token_logits,
                temperature=req.temperature,
                top_k=req.top_k
            )

            # Stop on EOS
            if next_token_id[0][0] == tokenizer.eos_token_id:
                break

            # Append next token
            generated_ids = np.concatenate([generated_ids, next_token_id], axis=1)

            # Optional paragraph break
            if next_token_id[0][0] == tokenizer.encode(".")[0]:
                paragraph_count += 1
                if paragraph_count >= max_paragraphs:
                    break

        # Decode and structure output
        raw_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        paragraphs = raw_text.split(". ")
        structured = "\n\n".join(p.strip() + "." for p in paragraphs if len(p.strip()) > 10)

        return InferenceResponse(output=structured)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))