FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY task_queue /app/task_queue
CMD ["python", "-m", "task_queue.worker"]