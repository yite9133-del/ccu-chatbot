import os
from openai import OpenAI
from flask import Flask, render_template, request

app = Flask(__name__)

# 讀取 Render 的環境變數
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY 未設定！")  # 如果沒設定，會直接報錯

client = OpenAI(api_key=api_key)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        user_input = request.form["user_input"]
        # 這裡可以加上呼叫 OpenAI 的程式碼，例如 ChatGPT 回應
        return f"你輸入了: {user_input}"
    return render_template("index.html")

# Flask 必須使用 0.0.0.0 + PORT 環境變數
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
