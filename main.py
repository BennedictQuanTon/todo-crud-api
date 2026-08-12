from fastapi import FastAPI, HTTPException, status
from typing import List, Dict, Any

app = FastAPI(
    title="Task API",
    version="1.0",
    description="A simple CRUD API for managing a To-Do list."
)

# In-memory database
tasks_db: List[Dict[str, Any]] = [
    {"id": 1, "title": "Buy milk", "done": False},
    {"id": 2, "title": "Read FastAPI docs", "done": True},
    {"id": 3, "title": "Build CRUD API assignment", "done": False},
]

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

@app.get("/tasks", summary="List all tasks")
def get_tasks():
    return tasks_db

@app.get("/tasks/{task_id}", summary="Get a single task by ID")
def get_task(task_id: int):
    for task in tasks_db:
        if task["id"] == task_id:
            return task
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Task {task_id} not found"
    )
