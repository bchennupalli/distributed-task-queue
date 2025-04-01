from .utils import exponential_backoff
import time
import redis
import json

def process_task(task):
    try:
        print(f"Processing task: {task}")
        time.sleep(2)
        if task['type'] == 'high_priority' and task.get('retries', 0) < 3:
            raise Exception("Simulated failure")
        print(f"Completed task: {task['type']}")
    except Exception as e:
        print(f"Task failed: {e}")
        task['retries'] = task.get('retries', 0) + 1
        delay = exponential_backoff(task['retries'])
        r.rpush('task_queue', json.dumps(task))
        print(f"Retrying task in {delay} seconds...")

        