import yfinance as yf
import requests
import os
import configparser
from datetime import datetime, timedelta

config = configparser.ConfigParser()
config.read('/root/gold_monitor/config.ini')
DISCORD_URL = config['secret']['discord_url']

PRICE_FILE = "/root/gold_monitor/last_price.txt"
LAST_LEVEL_FILE = "/root/gold_monitor/last_alert_level.txt"

def get_live_data():
    try:
        # 獲取國際克價
        gold_oz = yf.Ticker("GC=F").fast_info['last_price']
        usd_cnh = yf.Ticker("CNH=X").fast_info['last_price']
        return round((gold_oz * usd_cnh) / 31.1035, 2)
    except:
        return None

if __name__ == "__main__":
    # 判斷交易時段 (09:30 - 22:30)
    now_bj = datetime.utcnow() + timedelta(hours=8)
    curr_time = now_bj.strftime("%H:%M")
    is_weekday = now_bj.weekday() < 5
    is_open = is_weekday and ("09:30" <= curr_time <= "22:30")

    # 休市時直接退出，不發提醒
    if not is_open:
        exit()

    current_intl = get_live_data()
    if not current_intl or not os.path.exists(PRICE_FILE):
        exit()

    with open(PRICE_FILE, "r") as f:
        base_price = float(f.read().strip())
    
    diff = round(current_intl - base_price, 2)
    current_level = int(diff // 5)

    last_level = 0
    if os.path.exists(LAST_LEVEL_FILE):
        with open(LAST_LEVEL_FILE, "r") as f:
            try: last_level = int(f.read().strip())
            except: last_level = 0

    # 階梯變化且波動達標則報警
    if current_level != last_level and abs(current_level) >= 1:
        with open(LAST_LEVEL_FILE, "w") as f:
            f.write(str(current_level))
        
        direction = "大漲" if diff > 0 else "大跌"
        content = f"‼️ 金價{direction}\n當前: {current_intl}\n較收盤漲跌: {diff}\n時間: {now_bj.strftime('%H:%M:%S')}"
        requests.post(DISCORD_URL, json={"content": content})
