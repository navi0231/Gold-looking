import requests

# 国际 (USD/oz)
def get_price():
    url = "https://hq.sinajs.cn/list=hf_XAU"
    headers = {"Referer": "http://finance.sina.com.cn/", "User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        return float(response.text.split('"')[1].split(',')[0])
    except:
        return None

# 国内 (CNY/g)
def get_sge_price():
    url = "https://hq.sinajs.cn/list=sge_au9999"
    headers = {"Referer": "http://finance.sina.com.cn/", "User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.encoding = 'gbk'
        return float(response.text.split('"')[1].split(',')[1])
    except:
        return None