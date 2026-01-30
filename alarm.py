import os
import sys
import requests

# 切换到脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.getcwd())

import gold
import config

def main():
    sge = gold.get_sge_price()
    intl = gold.get_price()
    
    # discord推送
    lines = ["**金价报告**"]
    if sge: lines.append(f"> 国内 (Au99.99): **{sge}** 元/克")
    if intl: lines.append(f"> 国际 (XAU/USD): **{intl}** 美元/盎司")
    
    if len(lines) > 1:
        content = f"<@{config.USER_ID}>\n" + "\n".join(lines)
        requests.post(config.WEBHOOK_URL, json={"content": content})

if __name__ == "__main__":
    main()