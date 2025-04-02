import json
from config import get_redis_connection
from tasks import TASK_MAPPING

redis_client = get_redis_connection()

def start_worker():
    print('Worker started, waiting for tasks...')
    while True:
        _, task_json = redis_client.brpop('task_queue')
        task_data = json.loads(task_json)
        task_type = task_data.get('task')
        payload = task_data.get('payload')

        task_func = TASK_MAPPING.get(task_type)
        if task_func:
            print(f'Processing task: {task_type}')
            task_func(payload)
            print(f'Task {task_type} completed.')
        else:
            print(f'Unknown task type: {task_type}')

if __name__ == '__main__':
    start_worker()
