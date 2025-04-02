from fastapi import FastAPI
from pydantic import BaseModel
from app.config import get_redis_connection
import json
import uuid

app = FastAPI()
redis_client = get_redis_connection()

class TaskRequest(BaseModel):
    task_type: str
    payload: dict

@app.post('/enqueue-task')
async def enqueue_task(task: TaskRequest):
    task_id = str(uuid.uuid4())  # Generate a unique task ID (optional, not used in this example)
    task_data = {
        'id': task_id,
        'type': task.task_type,
        'payload': task.payload
    }

    redis_client.hset(f'task:{task_id}', mapping={
        'status': 'queued',
        'result': ''
    })

    redis_client.lpush('task_queue', json.dumps(task_data))
    return {'task_id': task_id, 'status': 'queued'}


@app.get('/task-status/{task_id}')
def get_task_status(task_id: str):
    data = redis_client.hgetall(f'task:{task_id}')
    if not data:
        return {'error': 'Task not found'}
    return {
        'status': data.get(b'status', b'').decode(),
        'result': data.get(b'result', b'').decode()
    }