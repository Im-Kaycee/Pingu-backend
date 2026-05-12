import hashlib
import json
import os
import time

CACHE_DIR = os.path.join(os.path.dirname(__file__), '..', '.cache')
CACHE_TTL = 60 * 60 * 24 * 7  # 7 days

def _key(query: str, error_context: str = None) -> str:
    raw = f"{query.strip().lower()}:{error_context or ''}"
    return hashlib.md5(raw.encode()).hexdigest()

def _path(key: str) -> str:
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, f"{key}.json")

def get(query: str, error_context: str = None) -> dict | None:
    if error_context:
        return None  # never cache error responses
    p = _path(_key(query))
    if not os.path.exists(p):
        return None
    with open(p) as f:
        entry = json.load(f)
    if time.time() - entry['ts'] > CACHE_TTL:
        os.remove(p)
        return None
    return entry['data']

def set(query: str, data: dict, error_context: str = None) -> None:
    if error_context:
        return  # never cache error responses
    p = _path(_key(query))
    with open(p, 'w') as f:
        json.dump({'ts': time.time(), 'data': data}, f)