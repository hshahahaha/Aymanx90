from flask import Flask, request, jsonify
import random
import os

app = Flask(__name__)

# نقطة فحص البطاقة
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

    return jsonify({
        "status": "success",
        "result": result
    })

# نقطة فحص صلاحية API
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

# تشغيل فحص البطاقات من الملف
def process_cards():
    CARDS_FILE = "cc.txt"
    if not os.path.exists(CARDS_FILE):
        print("❌ File cc.txt not found.")
        return

    with open(CARDS_FILE, 'r') as file:
        cards = [line.strip() for line in file if line.strip()]

    print(f"\n📦 Total cards to check: {len(cards)}\n" + "-"*40)

    for i, card in enumerate(cards, 1):
        res = app.test_client().post("/card", json={"card": card})
        result = res.get_json().get("result", "Unknown")
        print(f"[{i}] {card} → {result}")

# تشغيل الخادم وفحص البطاقات
if __name__ == "__main__":
    process_cards()
    # ✅ هذا هو التعديل المهم لتشغيله على Railway
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
