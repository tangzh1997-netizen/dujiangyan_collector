import requests
from bs4 import BeautifulSoup
import time
import random
# 如果没有安装，需要先在项目中安装 fake_useragent 库
from fake_useragent import UserAgent

# 初始化一个UserAgent对象
ua = UserAgent()

def smart_fetch_baidu_news(keyword, proxy=None, retries=3):
    """带反反爬策略的百度新闻抓取函数"""
    for attempt in range(retries):
        try:
            # 1. 随机生成一个User-Agent
            headers = {
                'User-Agent': ua.random,
                'Accept-Language': 'zh-CN,zh;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Connection': 'keep-alive',
            }

            # 2. 构建搜索URL
            search_url = f"https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd={keyword}"
            print(f"尝试抓取: {keyword}")

            # 3. 发送请求，支持代理
            proxies = {"http": proxy, "https": proxy} if proxy else None
            response = requests.get(search_url, headers=headers, proxies=proxies, timeout=15)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                # ... (此处放之前解析新闻的代码，保持不变) ...
                # 解析代码参考原来的 fetch_baidu_news 函数
                # ...

                # 4. 关键：随机暂停，模拟人类行为
                # 每次成功请求后，随机暂停5-15秒，这是有效的反反爬手段
                sleep_time = random.uniform(5, 15)
                print(f"抓取完成，暂停 {sleep_time:.2f} 秒...")
                time.sleep(sleep_time)
                return results # 返回解析到的新闻列表
            else:
                print(f"请求失败，状态码: {response.status_code}")

        except Exception as e:
            print(f"抓取 '{keyword}' 时出错 (尝试 {attempt+1}/{retries}): {e}")

        # 在重试前也等待一段时间
        if attempt < retries - 1:
            time.sleep(30)

    return [] # 所有重试都失败，返回空列表

# 在你的主循环中，可以这样调用
# all_news = smart_fetch_baidu_news("成都 水利", proxy="http://你的代理IP:端口")