import requests
import json
from line_config import LINE_CHANNEL_ACCESS_TOKEN

ACCESS_TOKEN = LINE_CHANNEL_ACCESS_TOKEN

# ✅ 正確 Content-Type 為 application/json（只用於建立 rich menu）
json_headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}",
    "Content-Type": "application/json"
}

# ✅ 無 Content-Type（讓 requests 自動幫你處理 multipart）
image_headers = {
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}

# ✅ Step 1：建立 Rich Menu 結構
create_rich_menu_url = 'https://api.line.me/v2/bot/richmenu'
body = {
    "size": {"width": 2500, "height": 843},
    "selected": True,
    "name": "main_menu",
    "chatBarText": "功能選單",
    "areas": [
        {
            "bounds": {"x": 250, "y": 200, "width": 1000, "height": 400},
            "action": {"type": "message", "label": "我的預約", "text": "我的預約"}
        },
        {
            "bounds": {"x": 1300, "y": 200, "width": 1000, "height": 400},
            "action": {"type": "uri", "label": "預約網站", "uri": "https://example.com"}
        }
    ]
}

res = requests.post(create_rich_menu_url, headers=json_headers, data=json.dumps(body))
print("建立結果:", res.status_code, res.text)

# ✅ 取得 richMenuId
try:
    rich_menu_id = res.json().get("richMenuId")
    if not rich_menu_id:
        raise ValueError("❌ 無法取得 Rich Menu ID，可能建立失敗")
    print("✅ Rich Menu ID:", rich_menu_id)
except Exception as e:
    print("❌ 建立 Rich Menu 發生錯誤：", e)
    exit(1)

import time
# 建立 Rich Menu 成功後
time.sleep(1.0)  # 等 1 秒再上傳圖片

# ✅ Step 2：上傳圖片（更完整錯誤輸出）
upload_url = f'https://api.line.me/v2/bot/richmenu/{rich_menu_id}/content'

print("🛰 上傳圖片網址:", upload_url)
print("📎 傳送 headers:", image_headers)

try:
    with open("richmenu.png", "rb") as image_file:
        files = {'file': ('richmenu.png', image_file, 'image/png')}
        res = requests.post(upload_url, headers=image_headers, files=files)

        if res.status_code != 200:
            print(f"❌ 上傳圖片失敗，狀態碼：{res.status_code}")
            try:
                print("❗ LINE 回應錯誤訊息：", res.json())
            except Exception:
                print("❗ 無法解析 LINE 錯誤回應文字：", res.text)
            exit(1)
        else:
            print("✅ 圖片上傳成功！")
except FileNotFoundError:
    print("❌ 找不到圖片檔案 'richmenu.png'")
    exit(1)

# ✅ Step 3：設為預設 Rich Menu
set_default_url = f'https://api.line.me/v2/bot/user/all/richmenu/{rich_menu_id}'
res = requests.post(set_default_url, headers=image_headers)
print("設為預設:", res.status_code, res.text)
if res.status_code == 200:
    print("🎉 成功設為預設 Rich Menu！")
else:
    print("⚠️ 設定失敗，請確認圖片是否已正確上傳")