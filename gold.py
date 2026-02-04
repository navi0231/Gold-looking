import subprocess
import json
import re

def get_domestic():
    # 既然这个能出 1134，就死守这个
    cmd = "curl -sk --referer 'https://finance.sina.com.cn' 'https://hq.sinajs.cn/list=gds_AU9999'"
    try:
        output = subprocess.check_output(cmd, shell=True).decode('gbk')
        match = re.search(r'"([^,"]+)', output)
        return match.group(1) if match else None
    except:
        return None

def get_intl():
    # 使用 my-json-server 的公开数据镜像或替代 API
    # 尝试一个更简单的公开接口：gold-api (如果不通，直接返回固定测试值判断是否是网络问题)
    cmd = "curl -sk 'https://api.gold-api.com/price/XAU'"
    try:
        output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        data = json.loads(output)
        return data.get('price')
    except:
        return None

if __name__ == "__main__":
    print(f"Domestic: {get_domestic()}")
    print(f"International: {get_intl()}")
