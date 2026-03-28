import os
import re
from datetime import datetime
from agents.script_writer import generate_script
from agents.voiceover import generate_voiceover
from agents.visuals import fetch_stock_footage
from agents.assembler import assemble_video
from agents.captions import generate_captions


def clean_filename(text):
    return re.sub(r'[^\w\s-]', '', text).strip().replace(' ', '_')[:50]


def generate_video():
    print("=" * 50)
    print("OBSCURE HIT STORY - VIDEO GENERATOR")
    print("=" * 50)

    # Step 1: Generate script
    print("\n[1/5] Generating script...")
    story = generate_script()
    print(f"Song: {story['song']}")

    # Step 2: Generate voiceover
    print("\n[2/5] Generating voiceover...")
    song_slug = clean_filename(story['song'])
    audio_filename = f"voiceover_{song_slug}.mp3"
    audio_path = generate_voiceover(story["script"], audio_filename)

    # Step 3: Fetch visuals
    print("\n[3/5] Fetching stock footage...")
    search_query = f"vintage music {story['year'][:3]}0s"
    videos = fetch_stock_footage(search_query, num_videos=5)
    video_urls = [v["url"] for v in videos]

    # Step 4: Assemble video
    print("\n[4/5] Assembling final video...")
    temp_filename = f"temp_{song_slug}.mp4"
    temp_path = assemble_video(video_urls, audio_path, temp_filename)

    # Step 5: Add captions and save as final file
    print("\n[5/5] Adding captions...")
    final_filename = f"{song_slug}_{story['year'][:3]}0s.mp4"
    final_path = f"outputs/{final_filename}"
    generate_captions(audio_path, temp_path, final_path)

    # Remove the temp video without captions
    try:
        os.remove(temp_path)
    except Exception:
        pass

    print("\n" + "=" * 50)
    print(f"DONE! Your video is ready: {final_path}")
    print(f"Song: {story['song']}")
    print("=" * 50)


if __name__ == "__main__":
    generate_video()