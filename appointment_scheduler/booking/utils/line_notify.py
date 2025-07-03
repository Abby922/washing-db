from linebot import LineBotApi
from linebot.models import TextSendMessage

LINE_ACCESS_TOKEN = '你的 Channel Access Token'

line_bot_api = LineBotApi(LINE_ACCESS_TOKEN)

def send_line_message(line_user_id, message):
    try:
        line_bot_api.push_message(line_user_id, TextSendMessage(text=message))
        return True
    except Exception as e:
        print(f"[Line 發送錯誤] {e}")
        return False