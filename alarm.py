import requests
import os
import time
import config

# 配置
WEBHOOK_URL =config.WEBHOOK_URL
FILE_PATH = "/root/gold_monitor/last_price.txt"
# 存放上次報警信息的數據：時間,價格
ALERT_LOG = "/root/gold_monitor/alert_log.txt" 
TARGET_PRICE = 1100
USER_ID =config.USER_ID

def send_discord(price, msg_type="目標達成"):
    content = f"🔔 **金價預警 ({msg_type})**\n當前價格：`{price}`\n提醒：<@{USER_ID}>"
    requests.post(WEBHOOK_URL, json={"content": content})

def check():
    if not os.path.exists(FILE_PATH): return
    
    with open(FILE_PATH, "r") as f:
        current_price = float(f.read().strip())

    # 如果價格高於目標，直接結束並清理日誌
    if current_price > TARGET_PRICE:
        if os.path.exists(ALERT_LOG): os.remove(ALERT_LOG)
        return

    # 觸發報警條件
    now = time.time()
    should_alert = False
    reason = "目標達成"

    if not os.path.exists(ALERT_LOG):
        # 第一次跌破目標
        should_alert = True
    else:
        with open(ALERT_LOG, "r") as f:
            last_time, last_price = map(float, f.read().split(','))
        
        # 檢查是否超過 30 分鐘 且 價格比上次報警時更低
        if (now - last_time > 1800) and (current_price < last_price):
            should_alert = True
            reason = "持續下跌提醒"

    if should_alert:
        send_discord(current_price, reason)
        # 記錄本次報警的時間和價格
        with open(ALERT_LOG, "w") as f:
            f.write(f"{now},{current_price}")

if __name__ == "__main__":
    check()

