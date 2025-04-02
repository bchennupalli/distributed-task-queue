# app/worker.py



import json
from app.config import get_redis_connection
from app.tasks import TASK_MAPPING

redis_client = get_redis_connection()

MAX_RETRIES = 3

def start_worker():
    print('Worker started, waiting for tasks...', flush=True)
    
    while True:
        _, task_json = redis_client.brpop('task_queue')
        task_data = json.loads(task_json)

        task_id = task_data.get('id')  # Unique task ID from producer
        task_type = task_data.get('type')
        payload = task_data.get('payload')
        retries = task_data.get('retries', 0)

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
                if retries < MAX_RETRIES:
                    task_data['retries'] = retries + 1
                    redis_client.lpush('task_queue', json.dumps(task_data))
                    print(f'Retrying task {task_id} (Attempt {retries + 1})', flush=True)
                    redis_client.hset(f"task:{task_id}", mapping={
                        'status': f'retrying ({retries + 1})',
                        'result': str(e)
                    })
                else:
                    redis_client.hset(f"task:{task_id}", mapping={
                        'status': 'failed',
                        'result': str(e)
                    })
                    print(f'Task {task_type} permanently failed after {MAX_RETRIES} retries.', flush=True)
        else:
            print(f'Unknown task type: {task_type}', flush=True)

start_worker()
