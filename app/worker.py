# app/worker.py
import json
from app.config import get_redis_connection
from app.tasks import TASK_MAPPING

redis_client = get_redis_connection()

def start_worker():
    print('Worker started, waiting for tasks...', flush=True)
    
    while True:
        _, task_json = redis_client.brpop('task_queue')
        task_data = json.loads(task_json)

        task_id = task_data.get('id')  # Unique task ID from producer
        task_type = task_data.get('type')
        payload = task_data.get('payload')

        task_func = TASK_MAPPING.get(task_type)

        if task_func:
            print(f'Processing task: {task_type}', flush=True)
            
            # Update status to processing
            redis_client.hset(f"task:{task_id}", 'status', 'processing')

            try:
                result = task_func(payload)

                # On success: mark as done and store result
                redis_client.hset(f"task:{task_id}", mapping={
                    'status': 'done',
                    'result': str(result)
                })

                print(f'Task {task_type} completed successfully.', flush=True)

            except Exception as e:
                # On failure: mark as failed and store error
                redis_client.hset(f"task:{task_id}", mapping={
                    'status': 'failed',
                    'result': str(e)
                })

                print(f'Task {task_type} failed: {e}', flush=True)
        else:
            print(f'Unknown task type: {task_type}', flush=True)

start_worker()
