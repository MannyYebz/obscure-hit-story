import anthropic
import os
from dotenv import load_dotenv

load_dotenv()

def generate_script():
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": """You are a music historian and engaging storyteller for TikTok. 
                Pick a random obscure song from any era (60s through 90s) that most people 
                have never heard of. Write a captivating 60-90 second script (about 150-200 words) 
                telling the story behind the song. 

                Format your response exactly like this:
                SONG: [Song name] by [Artist]
                YEAR: [Year]
                SCRIPT: [Your engaging story script here]"""
            }
        ]
    )

    response = message.content[0].text
    lines = response.strip().split('\n')
    
    song = lines[0].replace("SONG: ", "")
    year = lines[1].replace("YEAR: ", "")
    script = '\n'.join(lines[2:]).replace("SCRIPT: ", "")

    print(f"Song: {song}")
    print(f"Year: {year}")
    print(f"\nScript:\n{script}")
    
    return {"song": song, "year": year, "script": script}

if __name__ == "__main__":
    generate_script()