import time

def add_dynamic_version(request):
    # 獲取當前時間戳（以秒為單位）
    timestamp = str(int(time.time()))  # 以 UNIX 時間戳的格式返回
    return {'version': timestamp}
