from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_job
from apscheduler.triggers.cron import CronTrigger
import logging
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from booking.models import Appointment, MachineStatus

# 建立 Chrome 設定（可選：不跳出視窗、無頭模式）
chrome_options = Options()
chrome_options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
chrome_options.add_argument("--headless")  # 如不想開視窗可取消註解這行

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()
scheduler.add_jobstore(DjangoJobStore(), "default")

@register_job(scheduler, "interval", seconds=60, id="test_func", replace_existing=True, misfire_grace_time=1)
def test_func():
    chrome_driver_path = r"C:\Users\abby\Desktop\洗衣機\chromedriver-win64\chromedriver.exe"
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920x1080")
    
    service = Service(chrome_driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.get("https://service.upyoung.com.tw/artemis/monitor/lqjRO")

    time.sleep(3)  # 等待網頁載入

    try:
        rows = driver.find_element(By.ID, 'dtcTable').text.split()
    except Exception as e:
        logger.error(f"讀取資料失敗：{e}")
        driver.quit()
        return

    for i in range(len(rows)):
        if rows[i] in ('待機中', '運轉結束'):
            if i + 1 >= len(rows) or rows[i + 1] not in ('有', '無'):
                rows.insert(i + 1, '無')

    formatted_data = []
    if len(rows) >= 4:
        for i in range(4, len(rows), 4):  # 不硬編碼到 24
            try:
                machine_id = rows[i - 4]
                machine_name = rows[i - 3]
                status = rows[i - 2]
                remaining_time = rows[i - 1]
                formatted_data.append(f"{machine_id} {machine_name} {status} {remaining_time}")
            except IndexError:
                logger.warning(f"資料不足無法解析第 {i//4 + 1} 台機器：{rows}")
                continue

    filepath = r"C:\Users\abby\Desktop\洗衣機\washing_scheduler\data_from_states.txt"
    with open(filepath, "w", encoding="utf-8") as file:
        for line in formatted_data:
            file.write(line + "\n")

    driver.quit()

    with open(filepath, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for index, line in enumerate(lines):
        parts = line.strip().split(' ', 3)
        if len(parts) < 4:
            continue
        _, name, status, time_remaining = parts
        MachineStatus.objects.update_or_create(name=name, defaults={
            'status': status,
            'time_remaining': time_remaining
        })

@register_job(scheduler, CronTrigger(minute='1,31', hour='*'), id="delete_expired_appointments", replace_existing=True, misfire_grace_time=1)

def delete_expired_appointments():
    now = datetime.now()
    expired_appointments = Appointment.objects.filter(
        date__lt=now.date()
    ) | Appointment.objects.filter(
        date=now.date(), end_time__lt=now.time()
    )
    count = expired_appointments.count()
    expired_appointments.delete()
    logger.info(f"Deleted {count} expired appointments.")
