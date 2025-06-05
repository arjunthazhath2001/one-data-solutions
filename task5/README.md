# ✅ Task 5 — Infrastructure Automation with Shell + Docker Compose

### 🧠 Objective:
To simulate DevOps infrastructure automation **locally without using any cloud services**, by:
- Automating the setup of multiple services using Docker Compose
- Managing the environment with a shell script
- Using health checks and logs to monitor service status

---

## 🛠️ What I Did

### 1️⃣ Defined Multiple Services in `docker-compose.yml`
I set up the following services:
- **Jenkins** for CI
- **Redis** as a data store
- **Flask App** to simulate a microservice
- **NGINX** as a reverse proxy for the Flask App

Each service includes a `healthcheck` and mapped ports for accessibility.

---

### 2️⃣ Built a Minimal Flask App with Redis
The app increments a counter on each page visit/health check, stored in Redis.

```python
@app.route('/')
def index():
    r.incr('hits')
    return f"This page has been viewed {r.get('hits').decode('utf-8')} times!"
````

Located at:

```
/task5/sample-app/app.py
```

---

### 3️⃣ Dockerized the Flask App

#### `sample-app/Dockerfile`

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

#### `requirements.txt`

```
flask
redis
```

---

### 4️⃣ Configured NGINX as Reverse Proxy

#### `nginx/default.conf`

```nginx
server {
    listen 80;
    location / {
        proxy_pass http://sample-app:5000;
    }
}
```

This forwards `localhost:8081` → Flask app on port `5000`.

---

### 5️⃣ Wrote `setup.sh` Shell Script

```bash
#!/bin/bash

echo "Preparing environment..."
docker-compose down

echo "Building Docker images..."
docker-compose build

echo "Starting up containers..."
docker-compose up -d

echo "Waiting 5 seconds for containers to stabilize..."
sleep 5

echo "Current container status:"
docker-compose ps

echo "All services are up and running!"
echo "Tailing logs (Press Ctrl+C to exit)..."
docker-compose logs -f
```

---

## ⚙️ Health Checks (Bonus Feature)

Each service uses a Docker `healthcheck` to validate it's running properly:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000"]
  interval: 30s
  timeout: 10s
  retries: 5
```

> 🧠 This was causing the hit counter to increase **even without refreshing**, since the healthcheck pings the `/` route.

### ✅ Fix:

* Added a separate `/health` route to the Flask app
* Changed healthcheck to use `/health` instead

---

## 🐳 Volumes

* Jenkins uses a named volume `jenkins_home` to persist job config
* Redis by default does **not persist**, but I can enable it using:

```yaml
volumes:
  - redis_data:/data
```

```yaml
volumes:
  jenkins_home:
  redis_data:
```

---

## 🚀 How to Run

```bash
chmod +x setup.sh
./setup.sh
```

This will:

1. Tear down any old containers
2. Build everything fresh
3. Start containers
4. Show status
5. Tail logs

---

## 🌐 Access URLs

| Service     | URL                                            |
| ----------- | ---------------------------------------------- |
| Jenkins     | [http://localhost:8080](http://localhost:8080) |
| Flask App   | [http://localhost:5000](http://localhost:5000) |
| NGINX Proxy | [http://localhost:8081](http://localhost:8081) |

---

## 🔁 On Code Update

Just re-run:

```bash
./setup.sh
```

If you added volume for Redis, view count persists across runs.

---

## 📦 Summary

| Component     | Technology          |
| ------------- | ------------------- |
| Orchestration | Docker Compose      |
| App           | Flask + Redis       |
| Reverse Proxy | NGINX               |
| CI Tool       | Jenkins             |
| Scripting     | Shell (`setup.sh`)  |
| Monitoring    | Docker healthchecks |

---
