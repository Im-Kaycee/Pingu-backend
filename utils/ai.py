import os
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = """You are a Linux terminal assistant for Ubuntu users.

Rules:
- Return step-by-step terminal instructions only
- Each step must have: a short title, a brief explanation, and the exact command
- Never guess or generate GPG keys, signing keys, or repository URLs — say 'visit the official site' instead
- Always use commands appropriate for Ubuntu/apt
- If given an error, diagnose it and provide corrected commands
- Be concise. No waffle.

Return your response as JSON in this exact format:
{
  "summary": "one line description of what you're doing",
  "steps": [
    {
      "title": "Step title",
      "explanation": "Why this step is needed",
      "command": "the exact command to run"
    }
  ],
  "source": "official | community | ai",
  "warning": "optional warning string or null"
}

Return only the JSON object. No markdown, no backticks, no extra text."""

async def ask_gemini(query: str, system_info: dict, error_context: str = None) -> tuple:
    context = f"""
User system:
- OS: {system_info.get('os_name')} {system_info.get('os_version')} ({system_info.get('os_codename')})
- Architecture: {system_info.get('architecture')}
- Package manager: {system_info.get('package_manager')}
- Has snap: {system_info.get('has_snap')}
- Has flatpak: {system_info.get('has_flatpak')}
- Has docker: {system_info.get('has_docker')}

User query: {query}
"""
    if error_context:
        context += f"\nError the user encountered:\n{error_context}"

    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=f"{SYSTEM_PROMPT}\n\n{context}",
            config=types.GenerateContentConfig(
                response_mime_type="application/json"
            )
        )
        return json.loads(response.text), "gemini"
    except Exception as e:
        return {
            "summary": "Something went wrong",
            "steps": [],
            "source": "ai",
            "warning": str(e)
        }, "gemini"
        
#model = genai.GenerativeModel("gemini-3.1-flash-lite")
#model = genai.GenerativeModel("gemini-3.1-flash-preview")