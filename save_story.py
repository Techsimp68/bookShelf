import os
import subprocess
import sqlite3
import uuid
from pathlib import Path
import requests

# 📥 Narration API call
def generate_narration(text, voice="Rachel", out_path="audio/test.mp3"):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice}"

    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }

    response = requests.post(url, headers=headers, json={
        "text": text,
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.7
        }
    })

    if response.ok:
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        with open(out_path, "wb") as f:
            f.write(response.content)
        print(f"✅ Narration saved: {out_path}")
    else:
        print(f"❌ Error: {response.status_code} {response.text}")

# 💾 Store story in database
def save_to_database(book_id, user_id, author, file_path, content):
    conn = sqlite3.connect("stories.db")
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS stories
                 (book_id TEXT, user_id TEXT, author TEXT, file_path TEXT, content TEXT)''')
    c.execute("INSERT INTO stories VALUES (?, ?, ?, ?, ?)",
              (book_id, user_id, author, file_path, content))
    conn.commit()
    conn.close()

# 🧠 Story generation & saving
def generate_and_save_story(prompt: str, book_id: str, user_id: str, author: str,
                            book_title: str,
                            temperature: float = 0.8,
                            top_k: int = 50,
                            model_path: str = "models/mistral/mistral-7b-instruct-v0.1.Q4_K_M.gguf",
                            llama_bin: str = "./build/bin/main",
                            output_dir: str = "books",
                            max_tokens: int = 512):

    # 🗂️ Set up story folder
    story_folder = Path(output_dir) / book_id
    story_folder.mkdir(parents=True, exist_ok=True)

    txt_path = story_folder / "chapter_1.txt"
    audio_path = story_folder / "chapter_1.mp3"

    # 🧠 Build the llama.cpp command
    command = [
        llama_bin,
        "-m", model_path,
        "-p", prompt,
        "-n", str(max_tokens),
        "--temp", str(temperature),
        "--top-k", str(top_k)
    ]

    try:
        # 🚀 Run subprocess to generate text
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        generated_text = result.stdout.strip()

        # 💾 Save text to file
        with open(txt_path, "w", encoding="utf-8") as f:
            f.write(generated_text)

        # 🔊 Narrate with ElevenLabs (cap input to avoid token overflow)
        generate_narration(generated_text[:2500], out_path=str(audio_path))

        # 🗃️ Save story metadata to SQLite
        save_to_database(book_id, user_id, author, str(txt_path), generated_text)

        print(f"✅ Story saved to {txt_path}")
        return str(txt_path), str(audio_path)

    except subprocess.CalledProcessError as e:
        print("❌ Error during story generation:", e.stderr)
        return "", ""