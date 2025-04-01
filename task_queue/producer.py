import redis
import json
import time

r = redis.Redis(host='localhost', port=6379, db=0)

def send_task(task_type, data):
    task = {
        'type': task_type,
        'data': data,
        'timestamp': time.time()
    }
    r.rpush('task_queue', json.dumps(task))
    print(f"Sent task: {task}")

if __name__ == "__main__":
    send_task('process_image', {'image_id': 123, 'size': '1024x768'})