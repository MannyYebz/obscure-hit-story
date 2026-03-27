import os
import requests
from dotenv import load_dotenv

load_dotenv()

def generate_voiceover(script, filename="voiceover.mp3"):
    api_key = os.getenv("ELEVENLABS_API_KEY")
    
    # Voice ID for "George" - a great storytelling voice
    voice_id = "JBFqnCBsd6RMkjVDRZzb"
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "text": script,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }
    
    response = requests.post(url, headers=headers, json=data)
    
    if response.status_code == 200:
        output_path = f"outputs/{filename}"
        with open(output_path, "wb") as f:
            f.write(response.content)
        print(f"Voiceover saved to {output_path}")
        return output_path
    else:
        print(f"Error: {response.status_code} - {response.text}")
        return None

if __name__ == "__main__":
    test_script = "In 1968, a guy alone in a studio at 2 AM accidentally created one of the most hypnotic songs ever recorded. And the record label absolutely hated it."
    generate_voiceover(test_script, "test_voiceover.mp3")