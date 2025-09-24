@echo off
chcp 65001
echo ✅ 啟動預約系統中...

:: 啟動 Django Server（視窗1）
start "Django Server" cmd /k "conda activate washing && python manage.py runserver"

:: 啟動 GPT Line Bot + ngrok（視窗2）
start "LineBot + Ngrok" cmd /k "conda activate washing && python gptlinebot.py"

:: 背景執行 Scheduler（不跳視窗）
powershell -WindowStyle Hidden -Command "Start-Process powershell -WindowStyle Hidden -ArgumentList 'conda activate washing;python manage.py run_scheduler'"


echo ✅ 所有服務已啟動，請勿關閉 Django 與 LineBot 的視窗！
pause