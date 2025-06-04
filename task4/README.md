## ✅ Task 2 – Deploying Flask App on Local Kubernetes using `kind`

---

### 🧱 Step 1: Created a Simple Flask App

We began by creating a minimal **Flask application** (`app.py`) that returns a basic response on the root route `/`.

---

### 🐳 Step 2: Dockerized the Flask App

We wrote a `Dockerfile` for the Flask app:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

CMD ["python", "app.py"]
```

We built the image:

```bash
docker build -t flask-k8s-app .
```

---

### ☸️ Step 3: Set Up Local Kubernetes with kind

We installed and used [**kind**](https://kind.sigs.k8s.io/) to spin up a Kubernetes cluster inside Docker:

```bash
kind create cluster --name flask-cluster
```

---

### 📦 Step 4: Load Docker Image into kind Cluster

Because `kind` runs inside its own Docker environment, we explicitly loaded the image:

```bash
kind load docker-image flask-k8s-app --name flask-cluster
```

---

### 📁 Step 5: Created Kubernetes Manifests

We created a folder named `k8s/` with two manifest files:

#### 🧱 `deployment.yml` – Defines how to run the pods

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: flask-k8s-deployment
spec:
  replicas: 1
  selector:
    matchLabels:
      app: flask-app
  template:
    metadata:
      labels:
        app: flask-app
    spec:
      containers:
        - name: flask-container
          image: flask-k8s-app
          imagePullPolicy: Never
          ports:
            - containerPort: 5000
```

#### 🌐 `service.yml` – Exposes the deployment

```yaml
apiVersion: v1
kind: Service
metadata:
  name: flask-k8s-service
spec:
  selector:
    app: flask-app
  type: NodePort
  ports:
    - port: 80
      targetPort: 5000
```

> **Note:** We used `imagePullPolicy: Never` to ensure Kubernetes uses our **local Docker image** instead of pulling from an external registry.

---

### 🚀 Step 6: Applied the Kubernetes Configs

We deployed everything using:

```bash
kubectl apply -f k8s/
```

---

### 🔍 Step 7: Verified Deployment

We checked the status of our pods and services:

```bash
kubectl get pods
kubectl get services
```

Result:

* ✅ Pod running your Flask app
* ✅ Two services visible:

  * `flask-k8s-service`: Your exposed Flask service (`NodePort`)
  * `kubernetes`: Default internal cluster service (`ClusterIP`)

---

### 🌐 Step 8: Accessed the App via Port Forwarding

Since `kind` runs inside a container, we used `kubectl port-forward` to access the app on localhost:

```bash
kubectl port-forward service/flask-k8s-service 5001:80
```

This made your app accessible at:

```
http://localhost:5001
```

---

### 🧠 Key Learnings

* `kind` enables you to simulate a real Kubernetes environment **entirely locally**
* Docker image needs to be **manually loaded** into `kind`
* `imagePullPolicy: Never` ensures the image is used from the local machine
* Port forwarding helps expose services from Kubernetes to your host machine

---
