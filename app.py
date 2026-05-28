# -*- coding: utf-8 -*-
import os
import random
from flask import Flask, jsonify, render_template_string
from flask_cors import CORS

# 1. 先创建 Flask 应用实例
app = Flask(__name__)
CORS(app)

# ---------- 模拟数据（为了让页面立刻显示内容，避免百度爬虫问题）----------
# 如果您后续申请了 GNews API，可以替换这部分逻辑
MOCK_ARTICLES = [
    {"title": "都江堰灌区春灌工作全面启动", "url": "https://example.com/news/1", "source": "四川日报", "topicTag": "水利灌区"},
    {"title": "成都龙泉驿樱桃采摘节开幕", "url": "https://example.com/news/2", "source": "成都农业", "topicTag": "农业丰收"},
    {"title": "绵阳志愿者开展灌区环保行动", "url": "https://example.com/news/3", "source": "绵阳日报", "topicTag": "好人好事"},
    {"title": "眉山柑橘获地理标志产品认证", "url": "https://example.com/news/4", "source": "眉山新闻", "topicTag": "物产美食"},
    {"title": "德阳汛期安全巡查全面展开", "url": "https://example.com/news/5", "source": "德阳水利", "topicTag": "天气预警"},
    {"title": "都江堰水利工程科普：鱼嘴分水原理", "url": "https://example.com/news/6", "source": "科普中国", "topicTag": "科普宣传"},
    {"title": "乐山举办首届灌区丰收节", "url": "https://example.com/news/7", "source": "乐山日报", "topicTag": "农业丰收"},
    {"title": "资阳整治灌区水环境", "url": "https://example.com/news/8", "source": "资阳观察", "topicTag": "水利灌区"},
    {"title": "雅安茶叶品牌入选国家级名录", "url": "https://example.com/news/9", "source": "四川茶业", "topicTag": "物产美食"},
    {"title": "遂宁农技专家深入田间指导", "url": "https://example.com/news/10", "source": "遂宁农业", "topicTag": "行业动态"},
]

def collect_news():
    """临时返回模拟数据，后续可替换为真实API"""
    # 随机打乱顺序，模拟每次刷新不同结果
    random.shuffle(MOCK_ARTICLES)
    return MOCK_ARTICLES[:20]   # 最多返回20条

@app.route("/api/collect")
def api_collect():
    try:
        articles = collect_news()
        return jsonify({
            "success": True,
            "total": len(articles),
            "results": articles,
            "message": "采集成功（演示数据）"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "total": 0,
            "results": [],
            "message": str(e)
        }), 500

@app.route("/")
def index():
    # 这里放之前的前端HTML（完整内容，为了简洁只给框架，请用之前您调好的完整前端代码替换）
    return render_template_string('''
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>都江堰灌区资讯采集</title>
    <style>
        /* 这里请粘贴您之前的前端样式（完整CSS） */
        body { font-family: sans-serif; background: #f0f7f0; padding: 20px; }
        .container { max-width: 1200px; margin: auto; }
        /* 省略详细样式，您可直接复制之前的完整前端代码块 */
    </style>
</head>
<body>
    <div class="container">
        <h1>🌾 都江堰灌区智能采集系统</h1>
        <div id="status">加载中...</div>
        <div id="results"></div>
    </div>
    <script>
        // 这里请粘贴您之前完整的前端JavaScript代码，并确保 API_URL = '/api/collect'
        // 下面仅作示意，您务必替换为实际的前端代码（含渲染函数）
        fetch('/api/collect')
            .then(r => r.json())
            .then(data => {
                if(data.success) {
                    document.getElementById('results').innerHTML = data.results.map(a => `<div><a href="${a.url}" target="_blank">${a.title}</a> [${a.topicTag}]</div>`).join('');
                    document.getElementById('status').innerText = `共 ${data.total} 条`;
                } else {
                    document.getElementById('status').innerText = '采集失败';
                }
            });
    </script>
</body>
</html>
    ''')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)