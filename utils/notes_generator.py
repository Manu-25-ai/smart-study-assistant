import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generate_notes(transcript):

    prompt = f"""
    Analyze the following transcript and generate:

    1. Summary
    2. Key Points
    3. Important Concepts
    4. 5 Quiz Questions with Answers

    Transcript:
    {transcript}
    """

    response = model.generate_content(prompt)

    return response.text