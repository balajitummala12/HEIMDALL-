from flask import Flask, request, jsonify
from flask_cors import CORS

from core.services.chat_service import chat


app = Flask(__name__)

CORS(app)


@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "online",
        "system": "HEIMDALL",
        "version": "5.0.0"
    })


@app.route("/api/chat", methods=["POST"])
def chat_endpoint():

    try:

        data = request.get_json(silent=True)

        if not data:
            return jsonify({
                "error": "No JSON data received"
            }), 400


        message = str(
            data.get("message", "")
        ).strip()


        if not message:
            return jsonify({
                "error": "Message cannot be empty"
            }), 400


        response = chat(message)


        return jsonify({
            "response": response
        })


    except Exception as e:

        print("[SERVER ERROR]")
        print(e)

        return jsonify({
            "error": str(e)
        }), 500