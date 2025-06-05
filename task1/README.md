## ✅ Task 1 – Jenkins CI Pipeline to Build & Run Flask App with Docker

### 🧱 Step 1: Created Jenkins Docker Setup

I started by writing a `Dockerfile.jenkins` to run Jenkins locally using Docker. This image was based on the official Jenkins LTS and included Docker CLI tools so Jenkins could run Docker commands inside the container.

```dockerfile
FROM jenkins/jenkins:lts

USER root

RUN apt-get update && apt-get install -y docker.io

USER jenkins
```

This allowed Jenkins (running inside a container) to communicate with the **host Docker daemon** via `/var/run/docker.sock`.

---

### ⚙️ Step 2: Wrote a `docker-compose.yml` to Run Jenkins Easily

I added a `docker-compose.yml`:

```yaml
version: '3.8'

services:
  jenkins:
    build:
      context: .
      dockerfile: Dockerfile.jenkins
    ports:
      - "8080:8080"
    volumes:
      - jenkins_home:/var/jenkins_home
      - /var/run/docker.sock:/var/run/docker.sock
    user: root

volumes:
  jenkins_home:
```

* **Ports**: 8080 exposed Jenkins UI.
* **Volume `jenkins_home`**: persisted Jenkins config.
* **Docker socket bind**: allowed Jenkins to run Docker containers.

---

### 🧩 Step 3: Jenkins GUI Setup

After running `docker-compose up`, I:

* Logged in at `http://localhost:8080`
* Installed **recommended plugins** and the **Docker plugin**
* Created a **new Pipeline Job** in Jenkins

---

### 🧪 Step 4: Pipeline Stages via `Jenkinsfile`

Inside my GitHub repo (`task1/Jenkinsfile`), I defined the stages:

```groovy
pipeline {
    agent any

    stages {
        stage('Clone Repo') {
            steps {
                git 'https://github.com/arjunthazhath2001/one-data-solutions.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                dir('task1') {
                    sh 'docker build -t flask-task1-app .'
                }
            }
        }

        stage('Clean Old Containers') {
            steps {
                script {
                    sh 'docker ps -q --filter "publish=5000" | xargs -r docker rm -f'
                }
            }
        }

        stage('Run Docker Container') {
            steps {
                sh 'docker run -d -p 5000:5000 flask-task1-app'
            }
        }
    }
}
```

---

### 🐳 Why I Needed `Dockerfile.jenkins`

Initially, Jenkins builds failed with:

```
docker: command not found
```

I realized:

* The **Jenkins container didn’t include the Docker CLI**
* So I created `Dockerfile.jenkins` to add Docker inside the Jenkins container

> This was crucial: **Jenkins needs Docker CLI to talk to the host Docker daemon via mounted socket.**

---

### 🔁 Clean Deployment Strategy

I added this to avoid *“port already in use”* errors on repeated builds:

```groovy
stage('Clean Old Containers') {
    steps {
        script {
            sh 'docker ps -q --filter "publish=5000" | xargs -r docker rm -f'
        }
    }
}
```

This ensured old containers on port 5000 were **cleaned up before running the new one**.

---

### 🚀 Final Flow

1. I push code to GitHub
2. I hit **“Build Now”** in Jenkins
3. Jenkins:

   * Clones repo
   * Builds Docker image
   * Cleans old containers
   * Runs the new container

> ✅ Changes reflect automatically in browser at `http://localhost:5000`.

---

### 🧠 Key Learnings

* Docker inside Docker: **Jenkins runs inside Docker, but can use host Docker via socket bind**
* `Dockerfile.jenkins`: Used to install Docker CLI inside Jenkins container. Only then Jenkins can run Docker commands
* Container Cleanup: Necessary to prevent **“port already in use”** errors
* CI Flow: I now have a working CI pipeline that rebuilds and runs my app every time I update GitHub.

