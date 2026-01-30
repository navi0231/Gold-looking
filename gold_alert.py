import os
import sys
import requests

# 切换到脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())

import gold
import config

# 紀錄上次推送價格的文件
DB_FILE = "last_alert_price.txt"

def main():
    curr_sge = gold.get_sge_price()
    if not curr_sge: return

    # 讀取上次觸發報警的價格
    last_price = None
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r") as f:
            last_price = float(f.read())

    # 如果是第一次運行，紀錄價格後退出
    if last_price is None:
        with open(DB_FILE, "w") as f:
            f.write(str(curr_sge))
        return

    diff = curr_sge - last_price

    # 判斷漲跌幅是否達到 5 元
    if abs(diff) >= 5.0:
        trend = "📈 发现上涨" if diff > 0 else "📉 发现下跌"
        content = (
            f"<@{config.USER_ID}>\n"
            f"**【波动警告】**\n"
            f"国内金价变动大 {trend}！\n"
            f"幅度：**{abs(diff):.2f}** 元\n"
            f"当前价格：**{curr_sge}** 元/克"
        )
        
        # 推送到 Discord
        res = requests.post(config.WEBHOOK_URL, json={"content": content})
        
        # 只有發送成功才更新基準價，防止網絡波動導致漏報
        if res.status_code == 204:
            with open(DB_FILE, "w") as f:
                f.write(str(curr_sge))

if __name__ == "__main__":
    main()