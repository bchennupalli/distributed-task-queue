import time

def send_email(payload):
    email = payload.get('email')
    print(f"Sending email to {email}...", flush=True)
    time.sleep(5)
    print(f"Email sent to {email}!", flush=True)
    return f"Email sent to {email}!"

TASK_MAPPING = {
    'send_email': send_email,
}

