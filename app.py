from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Flask 서버가 정상 작동 중입니다."

@app.route("/spell", methods=["GET"])
def get_spell():
    q = request.args.get("q", "")
    return jsonify({
        "result": f"🔮 '{q}' 주문 정보를 불러왔습니다 (테스트용)."
    })

if __name__ == "__main__":
    app.run(debug=True)
