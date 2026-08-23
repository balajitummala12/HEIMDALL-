import os

from flask import Flask, request, jsonify
from flask_cors import CORS

from core.services.chat_service import chat


# ============================================================
# HEIMDALL 5.0 — API SERVER
# ============================================================

app = Flask(__name__)

# Allow frontend requests
CORS(app)


# ============================================================
# HEALTH CHECK
# ============================================================

@app.route("/api/health", methods=["GET"])
def health():

    return jsonify({
        "status": "online",
        "system": "HEIMDALL",
        "version": "5.0.0"
    })


# ============================================================
# CHAT ENDPOINT
# ============================================================

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

        print("\n" + "=" * 60)
        print("[USER]")
        print(message)

        # Send message to the actual HEIMDALL brain
        response = chat(message)

        print("\n[HEIMDALL]")
        print(response)
        print("=" * 60)

        return jsonify({
            "response": response
        })

    except Exception as e:

        print("\n[SERVER ERROR]")
        print(e)

        return jsonify({
            "error": str(e)
        }), 500


# ============================================================
# LOCAL START
# ============================================================

if __name__ == "__main__":

    port = int(
        os.environ.get("PORT", 5000)
    )

    print("=" * 60)
    print("⚔️ HEIMDALL 5.0 API SERVER")
    print("=" * 60)
    print("Status : ONLINE")
    print(f"Port   : {port}")
    print("=" * 60)

    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )