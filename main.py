from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import socket
from routes.query import router as query_router
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(query_router)
toggle_requested = False

@app.post("/toggle")
async def toggle():
    global toggle_requested
    toggle_requested = True
    return {"ok": True}

@app.get("/poll-toggle")
async def poll_toggle():
    global toggle_requested
    if toggle_requested:
        toggle_requested = False
        return {"should_toggle": True}
    return {"should_toggle": False}

@app.get("/status")
async def status():
    return {"provider": "gemini"}

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    port = 8765
    print(f"READY:{port}", flush=True)
    uvicorn.run("main:app", host="127.0.0.1", port=port, reload=True)