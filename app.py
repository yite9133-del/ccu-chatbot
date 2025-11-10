import os
import openai
from flask import Flask, render_template, request

app = Flask(__name__)

# 讀取 Render 的環境變數
openai.api_key = os.environ.get("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY 未設定！")

@app.route("/", methods=["GET", "POST"])
def index():
    reply = ""
    if request.method == "POST":
        user_input = request.form.get("user_input", "")
        if user_input:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": user_input}]
                )
                reply = response.choices[0].message.content
            except Exception as e:
                reply = f"發生錯誤：{str(e)}"
    return render_template("index.html", reply=reply)

@app.route("/ping")
def ping():
    return "pong", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
