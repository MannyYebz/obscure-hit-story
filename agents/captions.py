import whisper
import os


def generate_captions(audio_path, video_path, output_path):
    print("Loading Whisper model...")
    model = whisper.load_model("base")

    print("Transcribing audio...")
    result = model.transcribe(audio_path)

    print("Burning captions into video...")
    srt_path = audio_path.replace(".mp3", ".srt")

    # Write SRT file
    with open(srt_path, "w") as f:
        for i, segment in enumerate(result["segments"]):
            start = format_time(segment["start"])
            end = format_time(segment["end"])
            text = segment["text"].strip()
            f.write(f"{i+1}\n{start} --> {end}\n{text}\n\n")

    # Use ffmpeg to burn captions into video
    import subprocess
    captioned_path = output_path.replace(".mp4", "_captioned.mp4")
    subprocess.run([
        "ffmpeg", "-y",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}:force_style='FontSize=18,PrimaryColour=&HFFFFFF,OutlineColour=&H000000,Outline=2,Alignment=2'",
        "-c:a", "copy",
        captioned_path
    ], check=True)

    # Cleanup srt
    os.remove(srt_path)

    print(f"Captioned video saved to {captioned_path}")
    return captioned_path


def format_time(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02}:{m:02}:{s:02},{ms:03}"


if __name__ == "__main__":
    generate_captions(
        "outputs/test_voiceover.mp3",
        "outputs/test_final.mp4",
        "outputs/test_final.mp4"
    )