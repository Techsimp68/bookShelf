import requests
import os
from dotenv import load_dotenv
load_dotenv()
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