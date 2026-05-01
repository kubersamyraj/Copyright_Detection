import subprocess
import os

def convert_to_mp4(input_path):
    output_path = os.path.abspath(os.path.join("uploads", "converted.mp4"))

    command = [
        "ffmpeg",
        "-y",
        "-i", input_path,
        "-vcodec", "libx264",
        "-acodec", "aac",
        output_path
    ]

    subprocess.run(command)

    print("converted video:", output_path)

    return output_path