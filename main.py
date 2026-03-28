import os
from datetime import datetime
from agents.script_writer import generate_script
from agents.voiceover import generate_voiceover
from agents.visuals import fetch_stock_footage
from agents.assembler import assemble_video


def generate_video():
    print("=" * 50)
    print("OBSCURE HIT STORY - VIDEO GENERATOR")
    print("=" * 50)

    # Step 1: Generate script
    print("\n[1/4] Generating script...")
    story = generate_script()
    print(f"Song: {story['song']}")

    # Step 2: Generate voiceover
    print("\n[2/4] Generating voiceover...")
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    audio_filename = f"voiceover_{timestamp}.mp3"
    audio_path = generate_voiceover(story["script"], audio_filename)

    # Step 3: Fetch visuals
    print("\n[3/4] Fetching stock footage...")
    search_query = f"vintage music {story['year'][:3]}0s"
    videos = fetch_stock_footage(search_query, num_videos=5)
    video_urls = [v["url"] for v in videos]

    # Step 4: Assemble video
    print("\n[4/4] Assembling final video...")
    video_filename = f"video_{timestamp}.mp4"
    output_path = assemble_video(video_urls, audio_path, video_filename)

    print("\n" + "=" * 50)
    print(f"DONE! Your video is ready: {output_path}")
    print(f"Song: {story['song']}")
    print("=" * 50)


if __name__ == "__main__":
    generate_video()