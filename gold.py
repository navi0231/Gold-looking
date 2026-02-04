import requests

def get_price():
    """获取国际现货黄金 (XAU)"""
    url = "https://hq.sinajs.cn/list=hf_XAU"
    headers = {"Referer": "http://finance.sina.com.cn/"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        # 解析新浪国际金接口
        data = r.text.split('"')[1].split(',')
        return float(data[0])
    except:
        return None

def get_sge_price():
    # 换成沪金主力接口，更稳定
    url = "https://hq.sinajs.cn/list=nf_AU0"
    headers = {"Referer": "http://finance.sina.com.cn/"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        # 沪金解析逻辑
        data = r.text.split('"')[1].split(',')
        return float(data[8]) # 第9个字段是最新价
    except:
        return None