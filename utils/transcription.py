# import whisper

# def transcribe_audio(audio_path):
#     model = whisper.load_model("base")

#     result = model.transcribe(audio_path)

#     return result["text"]

import whisper

def transcribe_audio(audio_path):
    """
    Transcribes audio using Whisper with automatic language detection.
    Returns a dict with 'text' and 'language' keys.
    """
    model = whisper.load_model("base")

    # detect_language=True is default — Whisper auto detects
    result = model.transcribe(audio_path)

    return {
        "text": result["text"],
        "language": result.get("language", "unknown")
    }