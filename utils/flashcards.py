import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_flashcards(transcript: str) -> list[dict]:
    """
    Generates 10 flashcards from the transcript using Gemini.
    Returns a list of dicts with 'front' and 'back' keys.
    """
    prompt = f"""
Analyze the following transcript and generate exactly 10 flashcards for studying.
Each flashcard should have a concise question on the front and a clear answer on the back.
Cover the most important concepts, terms, and ideas from the content.

Return ONLY a valid JSON array in this exact format, nothing else:
[
  {{"front": "Question here?", "back": "Answer here."}},
  {{"front": "Question here?", "back": "Answer here."}}
]

Transcript:
{transcript}
"""
    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    flashcards = json.loads(raw.strip())
    return flashcards