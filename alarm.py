import os
import sys
import requests

# 环境配置
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())

import gold
import config

def main():
    sge = gold.get_sge_price()
    intl = gold.get_price()

    # 构造推送内容
    lines = ["**金价报告**"]
    if sge: lines.append(f"> 国内 (Au99.99): **{sge}** 元/克")
    if intl: lines.append(f"> 国际 (XAU/USD): **{intl}** 美元/盎司")

    # 推送判断
    if len(lines) > 1:
        content = "\n".join(lines)
        r = requests.post(config.WEBHOOK_URL, json={"content": content})
        print(f"Sent! Status: {r.status_code}")
    else:
        # 如果接口都挂了，发个通知提醒你
        print("No price data found.")
        requests.post(config.WEBHOOK_URL, json={"content": "监控运行中，但目前接口未返回价格。"})

if __name__ == "__main__":
    main()