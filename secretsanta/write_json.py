import json
from flask import Flask, request

app = Flask(__name__)

@app.route('/', method=['GET'])
def appendEntry():
    with open('ss_submisions.json', 'w, a+') as f:
        json.dump(request.form, f)
        f.close()

if __name__ == "__main__":
    app.run()
