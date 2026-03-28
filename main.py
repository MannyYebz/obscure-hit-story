import os
import re
from datetime import datetime
from agents.script_writer import generate_script
from agents.voiceover import generate_voiceover
from agents.visuals import fetch_stock_footage
from agents.assembler import assemble_video
from agents.captions import generate_captions


def clean_filename(text):
    # Remove any character that isn't alphanumeric, space, underscore or hyphen
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
    video_filename = f"{song_slug}_{story['year'][:3]}0s.mp4"
    output_path = assemble_video(video_urls, audio_path, video_filename)

    # Step 5: Add captions
    print("\n[5/5] Adding captions...")
    final_path = generate_captions(audio_path, output_path, output_path)

    print("\n" + "=" * 50)
    print(f"DONE! Your video is ready: {final_path}")
    print(f"Song: {story['song']}")
    print("=" * 50)


if __name__ == "__main__":
    generate_video()