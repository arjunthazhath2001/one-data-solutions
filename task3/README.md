# 🚀 Task 3: GitOps-Style Local Workflow with Argo CD

## 📌 Objective

Simulate a GitOps workflow by managing Kubernetes deployments through Git and Argo CD (locally via kind). This includes pushing manifests to Git, syncing changes via Argo CD, and observing live rollout behavior in Kubernetes.

---

## ✅ What I Did

### 🔧 1. Set up Local Kubernetes and Argo CD

* Created a local Kubernetes cluster using **kind**
* Installed **Argo CD** in its own `argocd` namespace via official manifest
* Port-forwarded Argo CD UI to access it via `https://localhost:8080`

### 📂 2. Prepared Kubernetes Manifests

Created:

* `deployment.yaml` with `nginx:1.25` initially
* `service.yaml` to expose the pod using a `ClusterIP` service

### 📝 3. Version-Controlled via Git

* Pushed manifests to a public GitHub repo: `one-data-solutions`
* Structured as:

```
task3/
└── k8s/
    ├── deployment.yaml
    └── service.yaml
```

### ⚙️ 4. Connected Argo CD to Git

* Created an Argo CD application pointing to:

  * Repo: `https://github.com/arjunthazhath2001/one-data-solutions`
  * Path: `task3/k8s`
  * Destination: `https://kubernetes.default.svc`
  * Namespace: `default`

### 🔄 5. Triggered GitOps Cycle

* Updated image version in `deployment.yaml`:
  `nginx:1.25` → `1.24` → `1.26`
* Committed and pushed changes to Git
* Argo CD detected diffs and applied changes
* Observed rolling updates with multiple revisions and pod transitions

---

## 🔍 Key Learnings

### ✅ What GitOps Is:

* Git is the **single source of truth**
* Any change to infrastructure (e.g., manifest files) is done **through Git**
* Argo CD automatically **syncs the Git state** with the Kubernetes cluster

### ❌ What GitOps Is Not:

* GitOps **does not manage your app code directly**
* Code changes (like Python or React) require **CI pipelines** to:

  1. Build new Docker image
  2. Push image to registry
  3. Update the image tag in deployment YAML
  4. Push updated YAML to Git → Argo CD then deploys it

### 🔁 What "rev" Means in Argo CD:

* `rev:1`, `rev:2` are **Deployment revisions**
* Each represents a **new rollout version** (e.g., new image or config)
* Argo CD keeps old ReplicaSets around for **rollback and audit history**

---

## 📸 Observations

* **ReplicaSets** are retained even with `replicas: 1` (for rollback)
* **Rolling updates** momentarily create two pods to ensure zero downtime
* Argo CD UI is very helpful to visualize app state, diffs, and rollout history

---

## 🧪 Demo It Again — Steps to Recreate from Scratch

### ✅ 1. Create kind cluster

```bash
kind create cluster --name argocd
```

### ✅ 2. Install Argo CD

```bash
kubectl create namespace argocd

kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml
```

### ✅ 3. Access Argo CD UI

```bash
kubectl port-forward svc/argocd-server -n argocd 8080:443
```

Visit [https://localhost:8080](https://localhost:8080)

### ✅ 4. Log in to Argo CD

```bash
# Get admin password
kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d
```

Use username: `admin` and the password above.

### ✅ 5. Create Argo CD app (via UI or CLI)

Example CLI:

```bash
argocd app create demo-app \
  --repo https://github.com/arjunthazhath2001/one-data-solutions \
  --path task3/k8s \
  --dest-server https://kubernetes.default.svc \
  --dest-namespace default
```

Then:

```bash
argocd app sync demo-app
```

### ✅ 6. Port-forward your app to test

```bash
kubectl port-forward service/demo-service 8081:80
```

Visit: [http://localhost:8081](http://localhost:8081)

---

