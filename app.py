# -*- coding: utf-8 -*-
import os
import random
import requests
from flask import Flask, jsonify, render_template_string
from flask_cors import CORS

# ---------- 1. 创建 Flask 应用实例 ----------
app = Flask(__name__)
CORS(app)

# ---------- 2. 获取真实新闻（使用 NewsAPI 免费版）----------
# 如果你不想注册 NewsAPI，可以直接使用下面的模拟数据函数（已备用）
# 但建议去 https://newsapi.org/register 免费注册，获得 API Key 后替换下面的 YOUR_API_KEY

NEWSAPI_KEY = "YOUR_API_KEY"  # 请替换为你的真实 Key，或者保持原样（此时会自动使用模拟数据）

def get_real_news():
    """从 NewsAPI 获取与都江堰灌区相关的新闻"""
    if NEWSAPI_KEY == "YOUR_API_KEY":
        return get_mock_news()  # 未配置 Key 时使用模拟数据
    
    url = "https://newsapi.org/v2/everything"
    params = {
        "q": "都江堰 OR 灌区 OR 成都水利 OR 绵阳农业 OR 眉山丰收",
        "apiKey": NEWSAPI_KEY,
        "language": "zh",
        "pageSize": 30,
        "sortBy": "publishedAt"
    }
    try:
        resp = requests.get(url, params=params, timeout=10)
        data = resp.json()
        if data.get("status") == "ok":
            articles = []
            for art in data.get("articles", []):
                articles.append({
                    "title": art["title"],
                    "url": art["url"],
                    "source": art["source"]["name"],
                    "topicTag": classify_topic(art["title"]),
                    "published": art["publishedAt"]
                })
            return articles
        else:
            return get_mock_news()
    except Exception as e:
        print("NewsAPI 调用失败:", e)
        return get_mock_news()

def get_mock_news():
    """模拟数据（备用）"""
    return [
        {"title": "都江堰灌区春灌工作全面启动", "url": "https://sichuan.scol.com.cn/ggxw/202503/82456789.html", "source": "四川日报", "topicTag": "水利灌区"},
        {"title": "成都龙泉驿樱桃采摘节开幕", "url": "https://www.chengdu.gov.cn/news/202503/123456.html", "source": "成都农业", "topicTag": "农业丰收"},
        {"title": "绵阳志愿者开展灌区环保行动", "url": "https://myrb.my.gov.cn/news/123", "source": "绵阳日报", "topicTag": "好人好事"},
        {"title": "眉山柑橘获地理标志产品认证", "url": "https://www.ms.gov.cn/news/456", "source": "眉山新闻", "topicTag": "物产美食"},
        {"title": "德阳汛期安全巡查全面展开", "url": "https://www.deyang.gov.cn/news/789", "source": "德阳水利", "topicTag": "天气预警"},
        {"title": "都江堰水利工程科普：鱼嘴分水原理", "url": "https://www.kepu.gov.cn/article/101", "source": "科普中国", "topicTag": "科普宣传"},
        {"title": "乐山举办首届灌区丰收节", "url": "https://lsrb.leshan.cn/news/111", "source": "乐山日报", "topicTag": "农业丰收"},
        {"title": "资阳整治灌区水环境", "url": "https://www.zy.gov.cn/news/222", "source": "资阳观察", "topicTag": "水利灌区"},
    ]

def classify_topic(title):
    kw_map = {
        '农业丰收': ['丰收','春灌','农业','采摘','水果','猕猴桃','柑橘','樱桃','枇杷','蔬菜','地理标志'],
        '水利灌区': ['水利','灌区','都江堰','汛期','水资源','东风渠'],
        '好人好事': ['好人','暖心','志愿','助农','救','帮扶'],
        '物产美食': ['美食','茶叶','中药材','特产','品牌'],
        '天气预警': ['天气','气象','预警','暴雨','高温'],
        '科普宣传': ['科普','知识','宣传','讲堂'],
        '行业动态': ['会议','调研','部署','管理','政策']
    }
    for cat, keywords in kw_map.items():
        if any(kw in title for kw in keywords):
            return cat
    return '灌区综合'

@app.route("/api/collect")
def api_collect():
    articles = get_real_news()
    random.shuffle(articles)  # 每次刷新顺序不同
    return jsonify({
        "success": True,
        "total": len(articles),
        "results": articles,
        "message": "采集成功"
    })

@app.route("/")
def index():
    return render_template_string('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>都江堰灌区智能采集系统</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background:#f0f7f0; font-family: system-ui, 'Segoe UI', sans-serif; padding:20px; color:#1e3a2f; }
        .container { max-width:1400px; margin:0 auto; }
        .header-card { background:linear-gradient(135deg,#1e6b3b,#0f4c2a); border-radius:32px; padding:24px 28px; margin-bottom:28px; color:white; }
        .header-card h1 { font-size:1.8rem; display:flex; align-items:center; gap:12px; flex-wrap:wrap; }
        .header-card h1 span { background:#ffd966; color:#1e3a2f; font-size:0.9rem; padding:4px 12px; border-radius:40px; }
        .sub { margin-top:12px; border-left:3px solid #ffd966; padding-left:14px; }
        .city-badge { display:flex; flex-wrap:wrap; gap:12px; margin-top:18px; font-size:0.85rem; }
        .city-badge div { background:rgba(255,255,240,0.2); border-radius:40px; padding:5px 14px; }
        .control-bar { background:white; border-radius:60px; padding:10px 20px; margin-bottom:30px; display:flex; justify-content:space-between; flex-wrap:wrap; gap:15px; border:1px solid #d9ead3; }
        .status { display:flex; align-items:center; gap:12px; font-weight:500; }
        .spinner { width:22px; height:22px; border:3px solid #c8e6d9; border-top-color:#1e6b3b; border-radius:50%; animation:spin 0.8s linear infinite; display:inline-block; }
        @keyframes spin { to { transform:rotate(360deg); } }
        .btn-refresh { background:#1e6b3b; border:none; color:white; padding:8px 22px; border-radius:40px; font-weight:600; cursor:pointer; }
        .btn-refresh:hover { background:#0f4c2a; }
        .stats { background:#eef4ea; border-radius:28px; padding:14px 24px; margin-bottom:28px; display:flex; gap:28px; flex-wrap:wrap; }
        .stats span { color:#2d6a4f; font-weight:700; font-size:1.3rem; margin-left:8px; }
        .results-grid { display:flex; flex-direction:column; gap:24px; }
        .section-card { background:white; border-radius:28px; box-shadow:0 8px 20px rgba(0,0,0,0.05); border:1px solid #e2f0da; }
        .section-header { background:#f9fff7; padding:16px 24px; border-bottom:2px solid #c8e6b5; display:flex; align-items:baseline; gap:10px; }
        .section-header h2 { font-size:1.35rem; color:#1e562e; }
        .section-header .count { background:#d4edc9; border-radius:30px; padding:2px 12px; font-size:0.75rem; }
        .news-list { list-style:none; }
        .news-item { border-bottom:1px solid #edf5e7; }
        .news-item:hover { background:#fefce8; }
        .news-link { display:flex; gap:14px; padding:16px 24px; text-decoration:none; color:#1e3a2f; }
        .news-icon { font-size:1.4rem; min-width:32px; }
        .news-title { font-weight:600; margin-bottom:6px; }
        .news-meta { display:flex; flex-wrap:wrap; gap:14px; font-size:0.7rem; color:#6c8b6e; }
        .empty-msg { padding:40px; text-align:center; color:#8ba888; font-style:italic; }
        footer { margin-top:40px; text-align:center; font-size:0.75rem; border-top:1px solid #d4e2ca; padding-top:24px; }
    </style>
</head>
<body>
<div class="container">
    <div class="header-card">
        <h1>🌾 都江堰灌区·智采 <span>八市41县市区</span></h1>
        <div class="sub">📍 成都·绵阳·德阳·眉山·乐山·雅安·资阳·遂宁 | 农业水利·物产·好人好事·灌区动态·美食</div>
        <div class="city-badge"><div>🏙️ 成都</div><div>绵阳</div><div>德阳</div><div>眉山</div><div>乐山</div><div>雅安</div><div>资阳</div><div>遂宁</div><div>🍒 水果/蔬菜/茶叶</div><div>🎉 丰收节/采摘节</div></div>
    </div>
    <div class="control-bar">
        <div class="status" id="statusArea"><span>🟢 就绪</span></div>
        <button class="btn-refresh" id="refreshBtn">🔄 立即采集</button>
    </div>
    <div class="stats">📊 共采集 <span id="totalCount">0</span> 条 · 涵盖主题 <span id="topicCount">0</span></div>
    <div id="resultsContainer" class="results-grid"><div class="empty-msg">✨ 打开页面自动采集，请稍后...</div></div>
    <footer>数据来自公开信源，部分为模拟样例，真实数据需配置 NewsAPI Key</footer>
</div>
<script>
    const API_URL = '/api/collect';
    async function startCollection() {
        const statusDiv = document.getElementById('statusArea');
        const refreshBtn = document.getElementById('refreshBtn');
        const resultsDiv = document.getElementById('resultsContainer');
        const totalSpan = document.getElementById('totalCount');
        const topicSpan = document.getElementById('topicCount');
        statusDiv.innerHTML = '<div class="spinner"></div> 🔍 正在采集资讯...';
        refreshBtn.disabled = true;
        refreshBtn.style.opacity = '0.6';
        resultsDiv.innerHTML = '<div class="empty-msg">⏳ 请求后端中...</div>';
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            console.log('后端返回:', data);
            if (data.success && Array.isArray(data.results)) {
                if (data.results.length === 0) {
                    resultsDiv.innerHTML = '<div class="empty-msg">📭 暂无相关资讯，请稍后刷新。</div>';
                } else {
                    renderGroupedResults(data.results);
                }
                totalSpan.innerText = data.total || 0;
                const topics = new Set(data.results.map(item => item.topicTag).filter(Boolean));
                topicSpan.innerText = topics.size;
                statusDiv.innerHTML = `✅ 采集完成 · ${data.results.length} 条资讯`;
            } else {
                throw new Error(data.message || '返回数据格式错误');
            }
        } catch (err) {
            console.error('采集错误:', err);
            resultsDiv.innerHTML = `<div class="empty-msg">❌ 采集失败：${err.message}<br>请检查后端服务。</div>`;
            statusDiv.innerHTML = '⚠️ 采集异常';
        } finally {
            refreshBtn.disabled = false;
            refreshBtn.style.opacity = '1';
        }
    }
    function renderGroupedResults(articles) {
        const categoryMap = {
            '农业丰收': ['丰收','春灌','农业','采摘','水果','猕猴桃','柑橘','樱桃','枇杷','蔬菜','地理标志'],
            '水利灌区': ['水利','灌区','都江堰','汛期','水资源'],
            '好人好事': ['好人','暖心','志愿','助农'],
            '物产美食': ['美食','茶叶','中药材','特产','品牌'],
            '天气预警': ['天气','气象','预警'],
            '科普宣传': ['科普','知识','宣传'],
            '行业动态': ['会议','调研','部署','管理','政策']
        };
        const enhanced = articles.map(art => {
            let cat = '灌区综合';
            const text = (art.title + ' ' + (art.topicTag || '')).toLowerCase();
            for (const [c, keywords] of Object.entries(categoryMap)) {
                if (keywords.some(kw => text.includes(kw.toLowerCase()))) {
                    cat = c;
                    break;
                }
            }
            return {...art, displayCat: cat};
        });
        const groups = {};
        enhanced.forEach(art => {
            if (!groups[art.displayCat]) groups[art.displayCat] = [];
            groups[art.displayCat].push(art);
        });
        const order = ['农业丰收','水利灌区','物产美食','好人好事','天气预警','科普宣传','行业动态','灌区综合'];
        let html = '';
        for (let cat of order) {
            if (groups[cat] && groups[cat].length) html += buildSection(cat, groups[cat]);
        }
        for (let cat in groups) {
            if (!order.includes(cat)) html += buildSection(cat, groups[cat]);
        }
        document.getElementById('resultsContainer').innerHTML = html;
    }
    function buildSection(catName, articles) {
        const icons = {'农业丰收':'🌾','水利灌区':'💧','物产美食':'🍊','好人好事':'❤️','天气预警':'⛈️','科普宣传':'📚','行业动态':'📰','灌区综合':'🗞️'};
        const icon = icons[catName] || '📌';
        return `
            <div class="section-card">
                <div class="section-header">
                    <h2>${icon} ${catName}</h2>
                    <div class="count">${articles.length}条</div>
                </div>
                <ul class="news-list">
                    ${articles.map(item => `
                        <li class="news-item">
                            <a href="${escapeHtml(item.url)}" target="_blank" rel="noopener" class="news-link">
                                <div class="news-icon">🔗</div>
                                <div class="news-content">
                                    <div class="news-title">${escapeHtml(item.title)}</div>
                                    <div class="news-meta">
                                        <span>🏷️ ${escapeHtml(item.topicTag || '灌区资讯')}</span>
                                        ${item.source ? `<span>📰 ${escapeHtml(item.source)}</span>` : ''}
                                        <span>🔗 点击阅读原文</span>
                                    </div>
                                </div>
                            </a>
                        </li>
                    `).join('')}
                </ul>
            </div>
        `;
    }
    function escapeHtml(str) {
        if (!str) return '';
        return str.replace(/[&<>]/g, function(m) {
            if (m === '&') return '&amp;';
            if (m === '<') return '&lt;';
            if (m === '>') return '&gt;';
            return m;
        });
    }
    window.addEventListener('DOMContentLoaded', startCollection);
    document.getElementById('refreshBtn').addEventListener('click', startCollection);
</script>
</body>
</html>
    ''')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
