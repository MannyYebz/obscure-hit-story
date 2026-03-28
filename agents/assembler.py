import os
import requests
import tempfile
import subprocess
import random
from PIL import Image

# Patch for Pillow 10+ compatibility with MoviePy 1.0.3
if not hasattr(Image, 'ANTIALIAS'):
    Image.ANTIALIAS = Image.LANCZOS

from moviepy.editor import VideoFileClip, AudioFileClip, concatenate_videoclips


BACKGROUND_TRACKS = [
    "https://archive.org/download/Free_20s_Jazz_Collection/hotlips.mp3",
    "https://archive.org/download/Free_20s_Jazz_Collection/sheik.mp3",
    "https://archive.org/download/Free_20s_Jazz_Collection/panama.mp3",
    "https://archive.org/download/Free_20s_Jazz_Collection/copenhag.mp3",
    "https://archive.org/download/Free_20s_Jazz_Collection/jazzdanc.mp3",
    "https://archive.org/download/Free_20s_Jazz_Collection/lowdown.mp3",
    "https://archive.org/download/Free_20s_Jazz_Collection/spanlove.mp3",
    "https://archive.org/download/Free_20s_Jazz_Collection/changes.mp3",
]


def get_background_music():
    track_url = random.choice(BACKGROUND_TRACKS)
    print(f"Downloading background music...")
    try:
        response = requests.get(track_url, stream=True, timeout=30)
        if response.status_code == 200:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            for chunk in response.iter_content(chunk_size=8192):
                tmp.write(chunk)
            tmp.close()
            print(f"Background music downloaded successfully")
            return tmp.name
    except Exception as e:
        print(f"Could not download background music: {e}")
    return None


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
    audio.close()

    print("Concatenating clips to match audio length...")
    combined = concatenate_videoclips(clips, method="compose")

    if combined.duration < total_duration:
        loops = int(total_duration / combined.duration) + 1
        combined = concatenate_videoclips([combined] * loops, method="compose")
    combined = combined.subclip(0, total_duration)

    print("Exporting video without audio...")
    temp_video = "outputs/temp_video.mp4"
    combined.write_videofile(temp_video, fps=30, codec="libx264", audio=False)
    combined.close()
    for clip in clips:
        clip.close()

    output_path = f"outputs/{output_filename}"
    music_path = get_background_music()

    if music_path:
        print("Merging voiceover, background music and video with ffmpeg...")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", temp_video,
            "-i", audio_path,
            "-i", music_path,
            "-filter_complex",
            "[1:a]volume=1.0[voice];[2:a]volume=0.08[music];[voice][music]amix=inputs=2:duration=first[aout]",
            "-map", "0:v",
            "-map", "[aout]",
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ], check=True)
        try:
            os.remove(music_path)
        except Exception:
            pass
    else:
        print("No background music, merging without it...")
        subprocess.run([
            "ffmpeg", "-y",
            "-i", temp_video,
            "-i", audio_path,
            "-c:v", "copy",
            "-c:a", "aac",
            "-shortest",
            output_path
        ], check=True)

    print("Cleaning up temp files...")
    try:
        os.remove(temp_video)
    except Exception:
        pass
    for path in clip_paths:
        try:
            os.remove(path)
        except Exception:
            pass

    print(f"Done! Video saved to {output_path}")
    return output_path


if __name__ == "__main__":
    from agents.visuals import fetch_stock_footage

    videos = fetch_stock_footage("vintage music studio 1960s", num_videos=3)
    video_urls = [v["url"] for v in videos]

    assemble_video(video_urls, "outputs/test_voiceover.mp3", "test_final.mp4")