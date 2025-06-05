from flask import Flask
import redis

app = Flask(__name__)
r = redis.Redis(host='redis', port=6379)

@app.route('/')
def index():
    r.incr('hits')
    return f'This page has been viewed {r.get("hits").decode("utf-8")} times!'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
