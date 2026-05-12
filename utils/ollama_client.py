import ollama
import json

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

async def ask_ollama(query: str, system_info: dict, error_context: str = None) -> dict:
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
        response = ollama.chat(
            model='phi3:mini',
            messages=[
                {'role': 'system', 'content': SYSTEM_PROMPT},
                {'role': 'user', 'content': context},
            ],
            options={'temperature': 0.2}
        )

        raw = response['message']['content'].strip()

        # Strip markdown fences if model adds them
        if raw.startswith('```'):
            raw = raw.split('```')[1]
            if raw.startswith('json'):
                raw = raw[4:]

        return json.loads(raw.strip())

    except json.JSONDecodeError:
        return {
            "summary": "Could not parse response",
            "steps": [],
            "source": "ai",
            "warning": "The local model returned an unexpected format. Try again."
        }
    except Exception as e:
        return {
            "summary": "Ollama error",
            "steps": [],
            "source": "ai",
            "warning": str(e)
        }