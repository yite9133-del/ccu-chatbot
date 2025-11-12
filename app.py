import os
import openai
import logging
from flask import Flask, render_template, request, jsonify

# 安全日誌：只顯示是否存在，不會輸出金鑰
logging.basicConfig(level=logging.INFO)
logging.info("OPENAI_API_KEY present: %s", bool(os.getenv("OPENAI_API_KEY")))

app = Flask(__name__)

# 嘗試讀取 API 金鑰
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if not openai.api_key:
        reply = "❌ 系統尚未設定 OpenAI 金鑰，請聯絡管理者或在 Render 設定環境變數。"
    elif request.method == "POST":
        user_input = request.form.get("user_input", "")
        if user_input:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_input}]
                )
                # 取出模型回覆（視 openai 套件回傳結構）
                reply = response.choices[0].message.content
            except Exception as e:
                logging.exception("OpenAI request failed")
                reply = f⚠️ 發生錯誤：{str(e)}"
    return render_template("index.html", reply=reply)

@app.route("/ping")
def ping():
    return "pong", 200

# 臨時測試用路由：回傳變數是否存在（請測試完畢後移除）
@app.route("/_env_check")
def env_check():
    return jsonify({"OPENAI_API_KEY_present": bool(os.getenv("OPENAI_API_KEY"))}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    # 在 Render 上建議使用 gunicorn 作為 Start Command，而非直接啟動開發伺服器
    app.run(host="0.0.0.0", port=port)
