from fastapi import APIRouter, HTTPException
from app.schemas import CreateTask, UpdateTask

router = APIRouter(prefix="/task", tags=["task"])

tasks = []

@router.get("/")
async def all_tasks():
    return tasks

@router.get("/{task_id}")
async def task_by_id(task_id: int):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.post("/create", response_model=dict)
async def create_task(task: CreateTask):
    task_id = len(tasks) + 1
    new_task = task.dict()
    new_task["id"] = task_id
    tasks.append(new_task)
    return new_task

@router.put("/update/{task_id}", response_model=dict)
async def update_task(task_id: int, task: UpdateTask):
    for t in tasks:
        if t["id"] == task_id:
            t.update(task.dict())
            return t
    raise HTTPException(status_code=404, detail="Task not found")

@router.delete("/delete/{task_id}", response_model=dict)
async def delete_task(task_id: int):
    for t in tasks:
        if t["id"] == task_id:
            tasks.remove(t)
            return t
    raise HTTPException(status_code=404, detail="Task not found")