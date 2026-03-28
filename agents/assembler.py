import os
import requests
import tempfile
from PIL import Image
# Patch for Pillow 10+ compatibility with MoviePy 1.0.3
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips

def download_file(url, suffix):
    response = requests.get(url, stream=True)
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
    for chunk in response.iter_content(chunk_size=8192):
        tmp.write(chunk)
    tmp.close()
    return tmp.name

def assemble_video(video_urls, audio_path, output_filename="final_video.mp4"):
    print("Downloading video clips...")
    clip_paths = [download_file(url, ".mp4") for url in video_urls]

    print("Loading and trimming clips...")
    clips = []
    for path in clip_paths:
        clip = VideoFileClip(path).resize((1080, 1920))
        clips.append(clip)

    print("Loading audio...")
    audio = AudioFileClip(audio_path)
    total_duration = audio.duration

    print("Concatenating clips to match audio length...")
    combined = concatenate_videoclips(clips, method="compose")

    if combined.duration < total_duration:
        loops = int(total_duration / combined.duration) + 1
        combined = concatenate_videoclips([combined] * loops, method="compose")
    combined = combined.subclip(0, total_duration)

    print("Adding audio to video...")
    final = combined.set_audio(audio)

    output_path = f"outputs/{output_filename}"
    print(f"Exporting final video to {output_path}...")
    final.write_videofile(output_path, fps=30, codec="libx264", audio_codec="aac")

    for path in clip_paths:
        os.remove(path)

    print(f"Done! Video saved to {output_path}")
    return output_path

if __name__ == "__main__":
    from agents.visuals import fetch_stock_footage

    videos = fetch_stock_footage("vintage music studio 1960s", num_videos=3)
    video_urls = [v["url"] for v in videos]

    assemble_video(video_urls, "outputs/test_voiceover.mp3", "test_final.mp4")