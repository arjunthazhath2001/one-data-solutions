FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
#have copied and run pip commands as a build optimisation technique
COPY . .
CMD ["python", "app.py"]
