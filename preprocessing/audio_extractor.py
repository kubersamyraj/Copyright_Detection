import subprocess
import os

def extract_audio(video_path, output_path):
    print("Extracting audio...")
    print("Video:", video_path)
    print("Output:", output_path)

    command = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-ac", "1",
        "-ar", "22050",
        "-acodec","pcm_s16le",
        output_path
    ]
    result = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    print("\n FFmpeg output: \n", result.stderr)

    if result.returncode != 0:
        print("FFmpeg command failed")
        return False
    

    if not os.path.exists(output_path):
        print("Putput file not created")
        return False
    
    print("Audio Extracted:", output_path)
    return True
