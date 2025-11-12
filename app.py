import os
import openai
from flask import Flask, render_template, request

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
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"⚠️ 發生錯誤：{str(e)}"
    return render_template("index.html", reply=reply)

@app.route("/ping")
def ping():
    return "pong", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
