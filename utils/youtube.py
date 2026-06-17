import os
from pytubefix import YouTube
from pytubefix.cli import on_progress

def download_audio(video_url):
    """Downloads audio from a YouTube URL using pytubefix."""

    # Clear downloads folder
    for file in os.listdir("downloads"):
        os.remove(os.path.join("downloads", file))

    yt = YouTube(video_url, on_progress_callback=on_progress)

    # Get the best audio stream
    audio_stream = yt.streams.get_audio_only()

    # Download to downloads folder
    output_path = audio_stream.download(output_path="downloads")

    return output_path


def extract_audio_from_video(video_path):
    """
    Extracts audio from an uploaded video file using ffmpeg.
    Returns path to the extracted audio file.
    """
    import subprocess
    output_path = "downloads/extracted_audio.mp3"

    subprocess.run([
        "ffmpeg", "-i", video_path,
        "-vn",                    # no video
        "-acodec", "libmp3lame",  # mp3 codec
        "-q:a", "2",              # high quality
        "-y",                     # overwrite if exists
        output_path
    ], check=True, capture_output=True)

    return output_path