import anthropic
import os
import json
from dotenv import load_dotenv

load_dotenv()

SONGS_LOG = "songs_used.json"

def load_used_songs():
    if os.path.exists(SONGS_LOG):
        with open(SONGS_LOG, "r") as f:
            return json.load(f)
    return []

def save_used_song(song):
    songs = load_used_songs()
    songs.append(song)
    with open(SONGS_LOG, "w") as f:
        json.dump(songs, f, indent=2)

def generate_script():
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    used_songs = load_used_songs()
    used_songs_text = ""
    if used_songs:
        used_songs_text = f"\n\nDo NOT pick any of these songs as they have already been used:\n" + "\n".join(used_songs)

    message = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""You are a music historian and engaging storyteller for TikTok.
                Pick a random obscure song from any era (60s through 90s) that most people
                have never heard of. Write a captivating 60-90 second script (about 150-200 words)
                telling the story behind the song.{used_songs_text}

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

    # Save to log
    save_used_song(song)

    print(f"Song: {song}")
    print(f"Year: {year}")
    print(f"\nScript:\n{script}")

    return {"song": song, "year": year, "script": script}

if __name__ == "__main__":
    generate_script()