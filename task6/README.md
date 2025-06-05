# 📊 Monitoring Stack with Prometheus + Grafana

## 🎯 Objective

Deploy and configure local monitoring for a containerized Flask application using **Prometheus** and **Grafana**.

This project demonstrates how to:
- Expose Prometheus-compatible metrics from a sample app
- Scrape and visualize those metrics using Prometheus and Grafana
- Create and export a custom Grafana dashboard

---

## 🏗️ Project Structure

```

project6-monitoring/
├── sample-app/                    # Flask app exposing /metrics
│   ├── app.py
│   ├── Dockerfile
│   └── requirements.txt
├── prometheus/
│   └── prometheus.yml            # Prometheus config
├── grafana/
│   └── sample-dashboard.json     # Exported Grafana dashboard
├── docker-compose.yml            # Orchestrates all services
└── README.md

````

---

## 🚀 How to Run

Make sure Docker and Docker Compose are installed.

```bash
docker-compose build
docker-compose up
````

Then access:

* 📦 Sample App: [http://localhost:5000](http://localhost:5000)
* 📊 Prometheus: [http://localhost:9090](http://localhost:9090)
* 📈 Grafana: [http://localhost:3000](http://localhost:3000)

> Grafana login: `admin` / `admin`

---

## 📊 Metrics Visualization

### Prometheus:

* Scrapes metrics from `sample-app:5000/metrics`
* Try this query in Prometheus UI:

  ```
  http_requests_total
  ```

### Grafana:

* Add Prometheus as a data source with URL: `http://prometheus:9090`
* Import `grafana/sample-dashboard.json` to load the pre-built dashboard
* Visualizes `http_requests_total` over time
* Auto-refresh interval: `5s`

---

## 📤 Dashboard Export

The Grafana dashboard is saved as `grafana/sample-dashboard.json`.
You can import it anytime using:

1. Go to Grafana → Dashboards → Import
2. Upload the JSON file or paste the content
3. Select Prometheus as the data source

---

## ✅ Tasks Completed

* [x] Set up a sample app with `/metrics` endpoint (Prometheus format)
* [x] Deploy Prometheus + Grafana using Docker Compose
* [x] Visualize custom metrics in Grafana
* [x] Create and export a dashboard

---

## 🙌 Demo & Testing

To simulate traffic:

```bash
while true; do curl http://localhost:5000; sleep 0.1; done
```

Watch the request count graph in Grafana auto-update in real-time!

---
