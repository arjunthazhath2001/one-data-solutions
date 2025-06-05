from flask import Flask
import random
import time

app= Flask(__name__)

@app.route("/")
def home():
    
    # # simulate processing delay
    # time.sleep(1)
    
    # #random failure
    # if random.random() < 0.5: #random.random generates a num between 0 and 1
    #     raise Exception("Random failure")
    # return "Hello! Everything is fine"

    # PROPOSED FIX(error handling via try-except):
    
    
    try:
        time.sleep(1)
        if random.random()<0.5:
                    raise Exception("Random failure")
        return "Hello! Everything is fine"
    except Exception as e:
        return f"Internal Error: {e}",500
    
        

if __name__== "__main__":
    app.run(debug=True)        

    