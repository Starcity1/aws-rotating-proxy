import io
import pickle

from flask import Flask, request, send_file
import requests

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    data = request.form
    r = requests.get(data['url'])
    pickled_respone = pickle.dumps(r)
    return send_file(io.BytesIO(pickled_respone), mimetype="application/octet-stream")


if __name__ == "__main__":
    app.run(debug=True)