# ✅ Task 4 — CI/CD with GitHub Actions + Docker Hub + Kubernetes (Kind)

### 🧠 Objective:
To build a real-world CI/CD pipeline using **GitHub Actions**, **Docker**, and **Kubernetes (Kind)** that:
- Builds and pushes a Docker image automatically to Docker Hub
- Deploys the image to a local **Kind** cluster manually
- Demonstrates real-time changes after code updates

---

## 🛠️ What I Did

### 1️⃣ Built a Minimal Flask App
I reused the same basic Flask app from Task 2 (`task4/app.py`) that returns a simple response.

---

### 2️⃣ Dockerized the App
I wrote a `Dockerfile` to containerize the Flask app.

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
```

---

### 3️⃣ Initial CI/CD Strategy (Failed Attempt)
I initially attempted to run a Kind cluster inside the GitHub Actions runner using this setup:
```yaml
- uses: engineerd/setup-kind@v0.5.0
- run: kind create cluster --name github-cicd
```

❌ **Why this failed**:
- GitHub-hosted runners are **ephemeral VMs**, and running Kind inside them requires privileged Docker access, which isn’t allowed for security reasons.
- I couldn’t expose or access the Kind cluster running inside GitHub Actions on my **local browser**, defeating the purpose of the demo.

---

### ✅ Final Strategy (Successful)
I revised the pipeline to:
1. **Use GitHub Actions only to build and push the image to Docker Hub**
2. **Use a local Kind cluster to pull that image and apply Kubernetes manifests**

---

## 🚀 GitHub Actions Workflow

The `.github/workflows/deploy.yml` does the following:

```yaml
- Checkout code
- Log in to Docker Hub using GitHub secrets
- Build the Docker image
- Push the image to Docker Hub
```

📦 The image is tagged and pushed to:
```
arjunta32/flask-k8s-app:latest
```

---

## ⚙️ Kubernetes Setup on Local Machine

I created a local Kind cluster:
```bash
kind create cluster --name flask-cluster
```

Then, deployed the app using:
```bash
kubectl apply -f ./task4/k8s
```

### Kubernetes Manifests:

#### `deployment.yml`
```yaml
image: arjunta32/flask-k8s-app:latest
```

#### `service.yml`
Exposes the Flask app as a `NodePort` service.

---

## 🌐 Port Forwarding

To test the app locally:
```bash
kubectl port-forward service/flask-k8s-service 5001:80
```

Visit: [http://localhost:5001](http://localhost:5001)

---

## 🔁 Updating the App (Code Changes)

If I make any changes to the code:
1. Push to GitHub (this triggers a new image build & push to Docker Hub)
2. Then, on the local machine:
   ```bash
   kubectl delete pod -l app=flask-k8s
   ```
   This forces Kubernetes to **recreate the pod with the updated image**.

✅ Done! The change is now live at `localhost:5001`.

---

## 🔒 Secrets Used in GitHub Actions
I set these in GitHub repository settings:
- `DOCKER_USERNAME`
- `DOCKER_PASSWORD`

---

## 📦 Summary

| Step | Platform               | Action                                      |
|------|------------------------|---------------------------------------------|
| 1    | GitHub Actions         | Build and push Docker image to Docker Hub   |
| 2    | Local (Kind)           | Pull image, apply manifests, run pod        |
| 3    | Local                  | Port forward to access app on localhost     |
| 4    | Local (on code change) | Delete pod to auto-recreate it with updated image |

---

### 🧠 Key Learning:
> CI/CD doesn’t always mean “everything is automatic”. Sometimes a **hybrid workflow** (GitHub runner + local cluster) is best suited for real-world constraints like network isolation, resource access, and debugging ease.