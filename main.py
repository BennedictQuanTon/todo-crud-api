from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Any, Optional

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

class TaskCreate(BaseModel):
    title: str = Field(..., description="Title of the task")

    @field_validator("title")
    def title_must_not_be_empty(cls, value: str):
        if not value or not value.strip():
            raise ValueError("Task title cannot be empty or blank")
        return value.strip()

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

@app.post("/tasks", status_code=status.HTTP_201_CREATED, summary="Create a new task")
def create_task(task_in: TaskCreate):
    if not task_in.title or not task_in.title.strip():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Task title cannot be empty or blank"
        )
    next_id = max([t["id"] for t in tasks_db], default=0) + 1
    new_task = {
        "id": next_id,
        "title": task_in.title.strip(),
        "done": False
    }
    tasks_db.append(new_task)
    return new_task
