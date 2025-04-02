from fastapi import FastAPI
from pydantic import BaseModel
from .config import get_redis_connection
import json
import uuid

app = FastAPI()
redis_client = get_redis_connection()

class TaskRequest(BaseModel):
    task_type: str
    payload: dict

@app.post('/enqueue-task')
async def enqueue_task(task: TaskRequest):
    task_data = {
        'task': task.task_type,
        'payload': task.payload
    }
    redis_client.lpush('task_queue', json.dumps(task_data))
    return {'status': 'Task submitted successfully'}
