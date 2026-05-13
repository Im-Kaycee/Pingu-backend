# Pingu Backend 🐧

The Python backend service for [Pingu](https://github.com/Im-kaycee/pingu-ui) — a sleek Linux terminal assistant for Ubuntu.

Handles AI queries, recipe matching, query caching, and system detection. Exposes a FastAPI HTTP server that the Electron frontend communicates with.

---

## Stack

- [FastAPI](https://fastapi.tiangolo.com/) — API framework
- [Uvicorn](https://www.uvicorn.org/) — ASGI server
- [google-genai](https://github.com/googleapis/python-genai) — Gemini AI client
- [rapidfuzz](https://github.com/maxbachmann/RapidFuzz) — fuzzy recipe matching
- [PyYAML](https://pyyaml.org/) — recipe file parsing

---

## Requirements

- Ubuntu 22.04 or later
- Python 3.10+
- A free [Gemini API key](https://aistudio.google.com)

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/Im-kaycee/pingu-backend.git
cd pingu-backend
```

### 2. Create a virtual environment

```bash
python3 -m venv backend
source backend/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Add your Gemini API key

```bash
cp backend/App/.env.example backend/App/.env
```

Edit `backend/App/.env`:

```env
GEMINI_API_KEY=your_key_here
```

Get a free key at [aistudio.google.com](https://aistudio.google.com) — no credit card required.

### 5. Start the server

```bash
source backend/bin/activate
cd backend/App
python main.py
```

The server runs at `http://127.0.0.1:8765`.

---

## How it works

Every query goes through a three-tier routing system:

```
Query
  │
  ├── 1. Recipe match?     → instant, verified, no AI
  │
  ├── 2. Cached before?    → instant, saved from previous query
  │
  └── 3. Ask Gemini        → AI answer, cached for next time
```

### Recipes

Recipes are YAML files in `backend/App/recipes/`. Each recipe has a list of trigger phrases, verified steps, and an official source URL.

Currently included:
- Docker, VS Code, Spotify, Chrome, Slack, Discord, Postman, DBeaver
- Node.js via NVM, PostgreSQL, Redis, Nginx
- Git configuration, SSH keys, Python virtual environments
- UFW firewall, Fail2ban, hostname change
- Fix broken apt packages, fix permission denied errors

### Cache

Successful AI responses are cached locally for 7 days. Same query twice — second response is instant with zero API calls.

### System detection

On every query the backend detects:
- Ubuntu version and codename
- CPU architecture
- Package manager
- Installed tools (snap, flatpak, docker, git, node, python3)

This context is sent to Gemini so answers are specific to your machine.

---

## API

### `POST /query`

Ask a Linux question.

**Request:**
```json
{
  "query": "install docker",
  "error_context": null
}
```

**Response:**
```json
{
  "summary": "Installing Docker Engine on Ubuntu",
  "steps": [
    {
      "title": "Update package list",
      "explanation": "Sync package index before installation",
      "command": "sudo apt update"
    }
  ],
  "source": "official",
  "warning": null,
  "provider": "recipe"
}
```

`provider` is one of: `recipe`, `cache`, `gemini`

---

### `GET /health`

Returns `{"status": "ok"}` when the server is running.

---

### `GET /status`

Returns the current AI provider.

```json
{"provider": "gemini"}
```

---

### `POST /toggle`

Signals the Electron frontend to show or hide the window. Called by the system hotkey script.

---

### `GET /poll-toggle`

Polled by the Electron frontend every 100ms to check for toggle signals.

---

## Adding recipes

Create a new YAML file in `backend/App/recipes/`:

```yaml
id: install-myapp
triggers:
  - install myapp
  - setup myapp
  - myapp install
name: Install MyApp
summary: Installing MyApp on Ubuntu
source: official
url: https://myapp.com/install
steps:
  - title: Step title
    explanation: Why this step is needed
    command: the exact command
```

No code changes needed — recipes are loaded automatically on startup.

---

## Related

- [pingu-ui](https://github.com/Im-kaycee/pingu-ui) — Electron frontend

---

## License

MIT