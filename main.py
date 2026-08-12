from fastapi import FastAPI

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing a To-Do list."
)

@app.get("/", summary="Root endpoint providing API info")
def get_root():
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks", "/health", "/stats"]
    }

@app.get("/health", summary="Health check endpoint")
def get_health():
    return {"status": "ok"}
