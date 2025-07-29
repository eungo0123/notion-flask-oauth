import os
from flask import Flask, request, jsonify
from notion_client import Client

app = Flask(__name__)

NOTION_TOKEN = os.environ.get("INTERNAL_TOKEN")
DATABASE_ID = os.environ.get("DATABASE_ID")

notion = Client(auth=NOTION_TOKEN)

@app.route("/")
def home():
    return "✅ Flask 서버가 정상 작동 중입니다."

@app.route("/spell", methods=["GET"])
def get_spell():
    q = request.args.get("q", "")
    response = notion.databases.query(
        **{
            "database_id": DATABASE_ID,
            "filter": {
                "or": [
                    {"property": "이름", "rich_text": {"contains": q}},
                    {"property": "원문", "rich_text": {"contains": q}}
                ]
            }
        }
    )
    results = response.get("results", [])
    if not results:
        return jsonify({"result": f"❌ '{q}' 주문을 찾을 수 없습니다."})
    prop = results[0]["properties"]
    def get_text(key):
        v = prop.get(key)
        if not v: return ""
        if "rich_text" in v:
            return "".join([t.get("plain_text", "") for t in v["rich_text"]])
        if "select" in v and v["select"]:
            return v["select"]["name"]
        if "multi_select" in v:
            return ", ".join([m["name"] for m in v["multi_select"]])
        return ""
    formatted = f"""이름: {get_text('이름')}
원문: {get_text('원문')}
주문 레벨: {get_text('주문 레벨')}
직업: {get_text('직업')}
마법유형: {get_text('마법유형')}
시전 시간: {get_text('시전 시간')}
사거리: {get_text('사거리')}
구성 요소: {get_text('구성 요소')}
물질: {get_text('물질')}
지속시간: {get_text('지속시간')}
집중 여부: {get_text('집중 여부')}
설명: {get_text('설명')}
고레벨에서: {get_text('고레벨에서')}"""
    return jsonify({"result": formatted})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
