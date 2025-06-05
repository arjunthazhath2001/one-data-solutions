from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
    return "HI ONE DATA SOLUTIONS! From TASK1 in CI/CD pipeline! See u"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
