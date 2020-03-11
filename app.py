from flask import Flask, request, jsonify, Blueprint, abort
from oc import create_s2i

app = Flask(__name__)


@app.route("/api/app", methods=["POST"])
def create_app():
    """
    {
        "name": "app",
        "source": "https://github.com/sclorg/s2i-ruby-container.git",
        "port": 8080
    }
    """
    fields = ["name", "source", "port"]
    if not request.json or not all(field in request.json for field in fields):
        abort(400)

    create_s2i(request.json["name"], request.json["source"], request.json["port"])
    return jsonify(status="success")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
