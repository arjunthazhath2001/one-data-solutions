# 🛠️ Task 7 - Simulated Production Incident & RCA

## 🔍 Objective

Simulate a problem in a local application, debug it using logs, and create a Root Cause Analysis (RCA).

---

## 📦 Application Overview

A simple Flask app that:
- Returns "Hello! Everything is fine." on success
- Fails randomly with a 50% chance due to an intentional exception

This simulates real-world flaky behavior to test incident handling skills.

---

## 📄 Logs Captured

(See `logs.txt` file)

Sample excerpt:

```

Traceback (most recent call last):
File "/home/linux/Desktop/onedata-assignment/venv/lib/python3.12/site-packages/flask/app.py", line 1536, in **call**
return self.wsgi\_app(environ, start\_response)
...
File "/home/linux/Desktop/onedata-assignment/task7/app.py", line 15, in home
raise Exception("Random failure")
Exception: Random failure

````

---

## 🔁 Steps to Reproduce

1. Run the app using: `python app.py`
2. Visit `http://127.0.0.1:5000` in a browser or run `curl http://127.0.0.1:5000`
3. Refresh several times
4. Observe that about 50% of requests raise a server error (`500 Internal Server Error`)

---

## 💥 Root Cause Analysis

### ❌ Issue:
The application randomly raises an exception:

```python
if random.random() < 0.5:
    raise Exception("Random failure")
````

There is no error handling around this block. When the exception is raised, Flask (running in debug mode) crashes the request with a full traceback.

### 🎯 Root Cause:

**Uncaught Exception in Production Path**

In real-world applications, such unhandled exceptions can lead to downtime or expose sensitive stack traces. This is a simulation of such behavior.

---

## ✅ Proposed Fix

### ✔️ Code Fix:

Wrap the risky code inside a `try-except` block to gracefully handle the error:

```python
@app.route("/")
def home():
    try:
        time.sleep(1)
        if random.random() < 0.5:
            raise Exception("Random failure")
        return "Hello! Everything is fine."
    except Exception as e:
        return f"Internal Error: {e}", 500
```

### ✅ Benefit:

* Prevents application crash
* Gives a controlled response to users
* Avoids exposing raw traceback in production

---
