import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def process_task(task):
    print(f"Processing task: {task}")
    time.sleep(2)  # Simulate some processing time
    print(f"Completed task: {task['type']}")

if __name__ == "__main__":
    while True:
        task_json = r.blpop('task_queue', timeout=0)[1]
        task = json.loads(task_json)
        process_task(task)

        