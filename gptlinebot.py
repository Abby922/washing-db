print("🔵 執行中：gptlinebot.py")

from flask import Flask, request, abort
from datetime import datetime
import django, os

from dotenv import load_dotenv
load_dotenv()

# DJANGO 初始化
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "appointment_scheduler.settings")
django.setup()

# 🔇 抑制 Django 的 SQL debug log
import logging
logging.getLogger('django.db.backends').setLevel(logging.WARNING)

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from booking.models import CustomUser, Appointment

# Flask 應用
app = Flask(__name__)

LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

import openai

from openai import OpenAI

openai_api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

def askchatgpt(q):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "你是一位風趣又友善的洗衣機預約系統助理。請用簡單、貼心的方式回應問題，並在要使用到中文的地方都使用繁體中文。"},
                {"role": "user", "content": q}
            ],
            temperature=1,
            max_tokens=256
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ ChatGPT 回覆失敗：{e}"

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    text = event.message.text.strip()
    user_id = event.source.user_id

    if text.startswith("我的學號是"):
        student_id = text.replace("我的學號是", "").strip()
        try:
            user = CustomUser.objects.get(student_id=student_id)
            user.line_id = user_id
            user.save()
            msg = "✅ 學號綁定成功！"
        except CustomUser.DoesNotExist:
            msg = "❌ 查無此學號"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
        return

    elif text == "我的預約":
        try:
            user = CustomUser.objects.get(line_id=user_id)
            appointments = Appointment.objects.filter(
                student_id=user.student_id,
                date__gte=datetime.today().date()
            ).order_by("date", "start_time")
            if appointments.exists():
                msg = "📅 你的未來預約如下：\n"
                for a in appointments:
                    msg += f"- {a.date} {a.start_time.strftime('%H:%M')} ~ {a.end_time.strftime('%H:%M')}（{a.machine}）\n"
            else:
                msg = "🙅‍♀️ 沒有任何未來的預約喔～"
        except CustomUser.DoesNotExist:
            msg = "⚠️ 尚未綁定學號"
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text=msg))
        return

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=askchatgpt(text)))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
