import google.generativeai as genai
import os
import json
import re
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")


def generate_mindmap_data(transcript: str) -> dict:
    """
    Generates mind map data from the transcript using Gemini.
    Returns a dict with a central topic and nested nodes.
    """
    prompt = f"""
    Analyze the transcript and create a SIMPLE mind map.

    Rules:
    - Create EXACTLY 4 main branches.
    - Create MAXIMUM 2 subtopics per branch.
    - Every topic must contain 1-3 words only.
    - Every subtopic must contain 1-3 words only.
    - Do NOT use complete sentences.
    - Use concise keywords.
    - Avoid explanations.
    - Keep labels presentation-friendly.

    Return ONLY valid JSON:

    {{
      "center": "Main Topic",
      "branches": [
        {{
          "topic": "Branch",
          "subtopics": ["Subtopic", "Subtopic"]
        }}
      ]
    }}

    Transcript:
    {transcript}
    """
    response = model.generate_content(prompt)
    raw = response.text.strip()

    # Strip markdown code fences if present
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"\s*```$", "", raw)

    try:
      return json.loads(raw.strip())
    except Exception:
      return {
          "center": "Mind Map",
          "branches": []
      }