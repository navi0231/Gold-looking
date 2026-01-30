import yfinance as yf
import requests
import os
import configparser
from datetime import datetime, timedelta

# 读取脱敏配置
config = configparser.ConfigParser()
config.read('/root/gold_monitor/config.ini')
DISCORD_URL = config['secret']['discord_url']

PRICE_FILE = "/root/gold_monitor/last_price.txt"

def get_live_data():
    try:
        gold_oz = yf.Ticker("GC=F").fast_info['last_price']
        usd_cnh = yf.Ticker("CNH=X").fast_info['last_price']
        price_intl_gram = round((gold_oz * usd_cnh) / 31.1035, 2)
        return price_intl_gram, round(gold_oz, 2)
    except:
        return None, None

if __name__ == "__main__":
    now_bj = datetime.utcnow() + timedelta(hours=8)
    curr_time = now_bj.strftime("%H:%M")
    is_weekday = now_bj.weekday() < 5
    is_open = is_weekday and ("09:30" <= curr_time <= "22:30")
    status = "交易中" if is_open else "休市"
    
    price_intl_gram, price_intl_oz = get_live_data()
    old_price_cn = None
    if os.path.exists(PRICE_FILE):
        with open(PRICE_FILE, "r") as f:
            try: old_price_cn = float(f.read().strip())
            except: pass

    if is_open:
        price_cn = round(price_intl_gram + 0.8, 2) if price_intl_gram else old_price_cn
        if price_cn:
            with open(PRICE_FILE, "w") as f:
                f.write(str(price_cn))
    else:
        price_cn = old_price_cn

    diff_str = "N/A"
    if price_intl_gram and old_price_cn:
        change = round(price_intl_gram - old_price_cn, 2)
        diff_str = f"+{change}" if change > 0 else f"{change}"

    line_intl = f"最新价格（国际）: {price_intl_gram if price_intl_gram else '失败'}元/克 [{price_intl_oz if price_intl_oz else 'N/A'}美元/盎司]"
    content = f"{status}\n最新价格（国内）: {price_cn}元/克\n{line_intl}\n涨跌幅: {diff_str}"
    requests.post(DISCORD_URL, json={"content": content})
