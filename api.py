from flask import Flask, request, jsonify
import random

app = Flask(__name__)

@app.route("/card", methods=["POST"])
def card_check():
    data = request.json
    card = data.get("card")
    if not card:
        return jsonify({"status": "error", "message": "No card provided"}), 400

    outcomes = [
        "3D-Authentication successful ☑️",
        "3D-Authentication failed ❌",
        "3D Secure challenge ✅"
    ]
    result = random.choice(outcomes)
    return jsonify({"status": "success", "result": result})

@app.route("/check", methods=["POST"])
def check():
    return jsonify({
        "status": "success",
        "user_id": "1427023555",
        "name": "لين.",
        "username": "GenshimImpact",
        "requests_left": "∞",
        "message": "API is valid"
    })

if __name__ == "__main__":
    app.run(debug=True)