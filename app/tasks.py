import time
import random

def send_email(payload):
    email = payload.get('email')
    print(f"Sending email to {email}...", flush=True)
    time.sleep(5)
    if random.random() < 0.4:
        raise Exception("Simualated email sending failure.")  # Simulate a failure 20% of the time
    print(f"Email sent to {email}!", flush=True)
    return f"Email sent to {email}!"

TASK_MAPPING = {
    'send_email': send_email,
}

