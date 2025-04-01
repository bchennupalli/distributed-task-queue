from prometheus_client import start_http_server, Gauge

QUEUE_LENGTH = Gauge('redis_queue_length', 'Current length of Redis task queue')

def update_metrics():
    while True:
        length = r.llen('task_queue')
        QUEUE_LENGTH.set(length)
        time.sleep(5)

if __name__ == "__main__":
    start_http_server(8000)
    threading.Thread(target=update_metrics).start()