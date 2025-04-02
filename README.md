💼 Distributed Task Queue System (Celery-like Alternative)
Tech Stack: Python · FastAPI · Redis · Docker · Docker Compose

🔧 Description:
Designed and implemented a lightweight distributed task queue system from scratch to run asynchronous background tasks across multiple worker containers. Inspired by Celery, this system is built using FastAPI and Redis, packaged into Docker containers, and fully orchestrated via Docker Compose for scalable and repeatable deployments.

🌟 Key Features:
Asynchronous Task Execution: Tasks such as sending emails are enqueued via API and processed in the background by dedicated workers, enabling non-blocking request handling.

Redis-Backed Queue: Used Redis as a message broker for storing queued tasks and task statuses (e.g., queued, processing, done, failed).

Custom Worker System: Implemented a robust worker service that polls Redis, executes tasks dynamically, and updates task status and results accordingly.

Retry Mechanism: Built-in support for automatic retries on failure (with retry count tracking and max retry limit).

Real-Time Admin Dashboard: Developed a minimal HTML dashboard with auto-refresh to monitor task IDs, statuses, results, and retry states.

Dockerized Architecture: Fully containerized with Docker; includes Redis, API server, and workers. Ready for deployment using Docker Compose or cloud platforms like Railway/Render.

🔍 Notable Learnings & Outcomes:
Gained a deep understanding of producer-consumer patterns, Pub/Sub queueing, and task reliability in distributed systems.

Applied clean architectural separation between API, task execution logic, and background processing.

Demonstrated ability to re-create foundational infrastructure (Celery-style system) using only open-source, free tools.