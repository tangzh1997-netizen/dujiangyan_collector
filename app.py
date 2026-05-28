# -*- coding: utf-8 -*-
import re
import time
import random
from flask import Flask, jsonify, render_template_string
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# ----- 八市列表 -----
CITIES = ["成都", "绵阳", "德阳", "眉山", "乐山", "雅安", "资阳", "遂宁"]

# ----- 采集主题（农业/水利/物产/好人好事/美食/节庆等）-----
TOPICS = [
    "农业", "水利", "灌区管理", "都江堰灌区", "春灌", "汛期",
    "好人好事", "暖心", "助农",
    "樱桃", "桃子", "枇杷", "李子", "杏子", "梨", "苹果", "猕猴桃", "葡萄",
    "柑橘", "柚子", "橙子", "草莓", "蓝莓", "西瓜", "甜瓜",
    "蔬菜", "茶叶", "中药材", "特色农产品", "地理标志产品", "农产品品牌",
    "采摘节", "丰收节", "农事节庆",
    "灌区动态", "丰收讯息", "重大天气", "行业重要新闻", "行业科普",
    "媒体宣传", "都江堰灌区美食",
]

BAIDU_NEWS_URL = "https://www.baidu.com/s?tn=news&rtt=1&bsst=1&cl=2&wd={}"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
}

def fetch_baidu_news(keyword):
    try:
        url = BAIDU_NEWS_URL.format(keyword)
        resp = requests.get(url, headers=HEADERS, timeout=10)
        resp.encoding = "utf-8"
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        for item in soup.select(".result"):
            title_tag = item.select_one("h3 a")
            if not title_tag:
                continue
            title = title_tag.get_text(strip=True)
            link = title_tag.get("href")
            if not link or link.startswith("javascript"):
                continue
            source_tag = item.select_one(".c-color-gray, .news-source")
            source = source_tag.get_text(strip=True) if source_tag else "百度资讯"
            results.append({
                "title": title,
                "url": link,
                "source": source[:30],
                "topicTag": keyword
            })
        return results[:8]
    except Exception as e:
        print(f"关键词 {keyword} 失败: {e}")
        return []

def collect_all_news():
    all_articles = []
    seen_urls = set()
    search_queries = []
    for city in CITIES:
        for topic in TOPICS:
            search_queries.append(f"{city} {topic}")
    extra = ["都江堰灌区", "都江堰水利", "四川水利灌区", "灌区丰收"]
    search_queries.extend(extra)
    random.shuffle(search_queries)

    for idx, query in enumerate(search_queries):
        if idx >= 180:
            break
        print(f"采集: {query}")
        articles = fetch_baidu_news(query)
        for art in articles:
            if art["url"] not in seen_urls:
                seen_urls.add(art["url"])
                all_articles.append(art)
        time.sleep(random.uniform(1, 1.5))
        if len(all_articles) >= 350:
            break

    for fk in ["都江堰 美食", "灌区 特产", "樱桃 采摘节", "柑橘 品牌", "四川 地理标志"]:
        articles = fetch_baidu_news(fk)
        for art in articles:
            if art["url"] not in seen_urls:
                seen_urls.add(art["url"])
                all_articles.append(art)
        time.sleep(1)
    print(f"总共采集到 {len(all_articles)} 条")
    return all_articles

@app.route("/api/collect")
def api_collect():
    try:
        articles = collect_all_news()
        return jsonify({
            "success": True,
            "total": len(articles),
            "results": articles,
            "message": "采集成功"
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "total": 0,
            "results": [],
            "message": f"采集错误: {str(e)}"
        }), 500

@app.route("/")
def index():
    # 完整的前端HTML代码（已内嵌）
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes">
        <title>都江堰灌区智能采集系统 | 新闻·资讯·物产</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body { background: #f0f7f0; font-family: system-ui, 'Segoe UI', 'Roboto', sans-serif; padding: 20px; color: #1e3a2f; }
            .container { max-width: 1400px; margin: 0 auto; }
            .header-card { background: linear-gradient(135deg, #1e6b3b, #0f4c2a); border-radius: 32px; padding: 24px 28px; margin-bottom: 28px; box-shadow: 0 12px 24px rgba(0,0,0,0.1); color: white; }
            .header-card h1 { font-size: 1.8rem; font-weight: 700; display: flex; align-items: center; gap: 12px; flex-wrap: wrap; }
            .header-card h1 span { background: #ffd966; color: #1e3a2f; font-size: 0.9rem; padding: 4px 12px; border-radius: 40px; font-weight: 500; }
            .sub { margin-top: 12px; opacity: 0.9; font-size: 0.95rem; border-left: 3px solid #ffd966; padding-left: 14px; }
            .city-badge { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 18px; font-size: 0.85rem; }
            .city-badge div { background: rgba(255,255,240,0.2); backdrop-filter: blur(2px); border-radius: 40px; padding: 5px 14px; }
            .control-bar { background: white; border-radius: 60px; padding: 10px 20px; margin-bottom: 30px; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 15px; box-shadow: 0 4px 12px rgba(0,0,0,0.03); border: 1px solid #d9ead3; }
            .status { display: flex; align-items: center; gap: 12px; font-weight: 500; }
            .spinner { width: 22px; height: 22px; border: 3px solid #c8e6d9; border-top-color: #1e6b3b; border-radius: 50%; animation: spin 0.8s linear infinite; display: inline-block; }
            @keyframes spin { to { transform: rotate(360deg); } }
            .btn-refresh { background: #1e6b3b; border: none; color: white; padding: 8px 22px; border-radius: 40px; font-weight: 600; cursor: pointer; transition: 0.2s; box-shadow: 0 2px 6px rgba(0,0,0,0.1); }
            .btn-refresh:hover { background: #0f4c2a; transform: scale(0.97); }
            .stats { background: #eef4ea; border-radius: 28px; padding: 14px 24px; margin-bottom: 28px; display: flex; gap: 28px; flex-wrap: wrap; font-weight: 500; border: 1px solid #cfe3c2; }
            .stats span { color: #2d6a4f; font-weight: 700; font-size: 1.3rem; margin-left: 8px; }
            .results-grid { display: flex; flex-direction: column; gap: 24px; }
            .section-card { background: white; border-radius: 28px; box-shadow: 0 8px 20px rgba(0,0,0,0.05); overflow: hidden; border: 1px solid #e2f0da; }
            .section-header { background: #f9fff7; padding: 16px 24px; border-bottom: 2px solid #c8e6b5; display: flex; align-items: baseline; flex-wrap: wrap; gap: 10px; }
            .section-header h2 { font-size: 1.35rem; font-weight: 700; color: #1e562e; }
            .section-header .count { background: #d4edc9; border-radius: 30px; padding: 2px 12px; font-size: 0.75rem; font-weight: 600; }
            .news-list { list-style: none; }
            .news-item { border-bottom: 1px solid #edf5e7; transition: background 0.1s; }
            .news-item:hover { background: #fefce8; }
            .news-link { display: flex; align-items: flex-start; gap: 14px; padding: 16px 24px; text-decoration: none; color: #1e3a2f; }
            .news-icon { font-size: 1.4rem; min-width: 32px; text-align: center; }
            .news-content { flex: 1; }
            .news-title { font-weight: 600; font-size: 1rem; line-height: 1.4; margin-bottom: 6px; color: #0b2b1f; }
            .news-meta { display: flex; flex-wrap: wrap; gap: 14px; font-size: 0.7rem; color: #6c8b6e; }
            .badge-topic { background: #eaf4e4; padding: 2px 8px; border-radius: 20px; font-size: 0.7rem; }
            .empty-msg { padding: 40px; text-align: center; color: #8ba888; font-style: italic; }
            footer { margin-top: 40px; text-align: center; font-size: 0.75rem; color: #5a7c5a; border-top: 1px solid #d4e2ca; padding-top: 24px; }
            @media (max-width: 640px) { body { padding: 12px; } .news-link { padding: 12px 16px; } .section-header h2 { font-size: 1.2rem; } }
        </style>
    </head>
    <body>
    <div class="container">
        <div class="header-card">
            <h1>🌾 都江堰灌区·智采千里眼 <span>八市41县市区</span></h1>
            <div class="sub">📍 覆盖成都·绵阳·德阳·眉山·乐山·雅安·资阳·遂宁 | 农业水利·物产节庆·好人好事·灌区动态·天气科普·美食资讯</div>
            <div class="city-badge"><div>🏙️ 成都</div><div>🏙️ 绵阳</div><div>🏙️ 德阳</div><div>🏙️ 眉山</div><div>🏙️ 乐山</div><div>🏙️ 雅安</div><div>🏙️ 资阳</div><div>🏙️ 遂宁</div><div>🍒 樱桃/枇杷/猕猴桃/柑橘</div><div>🌿 茶叶/中药材</div><div>🎉 丰收节/采摘节</div></div>
        </div>
        <div class="control-bar">
            <div class="status" id="statusArea"><span>🟢 就绪</span></div>
            <button class="btn-refresh" id="refreshBtn">🔄 立即采集最新资讯</button>
        </div>
        <div class="stats" id="statsPanel">📊 共采集 <span id="totalCount">0</span> 条 · 涵盖主题 <span id="topicCount">0</span>+</div>
        <div id="resultsContainer" class="results-grid"><div class="empty-msg">✨ 打开页面自动采集 · 正在为您搜罗都江堰灌区最新消息，请稍等...</div></div>
        <footer>⚡ 智能采集引擎 · 实时聚合百度新闻/主流资讯 (基于关键词精准覆盖) | 数据仅为个人学习参考，链接均来自公开网络</footer>
    </div>
    <script>
        const API_URL = '/api/collect';
        async function startCollection() {
            const statusDiv = document.getElementById('statusArea');
            const refreshBtn = document.getElementById('refreshBtn');
            const resultsContainer = document.getElementById('resultsContainer');
            const totalSpan = document.getElementById('totalCount');
            const topicSpan = document.getElementById('topicCount');
            statusDiv.innerHTML = '<div class="spinner"></div> 🔍 正在智能爬取八市41县农业·水利·物产·动态... 耐心等待(约15~30秒)';
            refreshBtn.disabled = true;
            refreshBtn.style.opacity = '0.6';
            resultsContainer.innerHTML = '<div class="empty-msg">⏳ 正在连接后端采集引擎，关键词覆盖300+组合，去重聚合中…<br>（首次加载可能稍慢）</div>';
            try {
                const response = await fetch(API_URL, { method: 'GET', headers: { 'Accept': 'application/json' } });
                if (!response.ok) throw new Error(`HTTP ${response.status}`);
                const data = await response.json();
                if (data.success && data.results) {
                    renderGroupedResults(data.results);
                    totalSpan.innerText = data.total || 0;
                    const allTopics = new Set();
                    data.results.forEach(item => { if (item.topicTag) allTopics.add(item.topicTag); });
                    topicSpan.innerText = allTopics.size || '多';
                    statusDiv.innerHTML = `✅ 采集完成 · 最新 ${data.total} 条新闻/资讯`;
                } else {
                    resultsContainer.innerHTML = `<div class="empty-msg">⚠️ 暂无数据，请检查网络或稍后重试。<br>${data.message || '后端采集未返回有效数据'}</div>`;
                    statusDiv.innerHTML = '⚠️ 采集异常，可点击刷新重试';
                }
            } catch (err) {
                resultsContainer.innerHTML = `<div class="empty-msg">❌ 采集服务请求失败: ${err.message}<br>请稍后刷新重试</div>`;
                statusDiv.innerHTML = '❌ 连接后端失败';
            } finally {
                refreshBtn.disabled = false;
                refreshBtn.style.opacity = '1';
            }
        }
        function renderGroupedResults(articles) {
            const container = document.getElementById('resultsContainer');
            if (!articles || articles.length === 0) { container.innerHTML = '<div class="empty-msg">📭 暂未采集到相关资讯，试试刷新或稍后再来~</div>'; return; }
            const categoryMap = { '农业丰收': ['丰收','春灌','农业','采摘节','丰收节','物产','水果','蔬菜','猕猴桃','柑橘','樱桃','枇杷','蓝莓','西瓜','农产品','地理标志'], '水利灌区': ['水利','灌区管理','都江堰','汛期','春灌','灌区动态','水资源'], '好人好事': ['好人','好事','暖心','助农','志愿'], '物产美食': ['美食','茶叶','中药材','特色农产品','品牌','采摘','水果节','甜瓜','草莓'], '天气预警': ['天气','气象','汛情','重大天气'], '科普宣传': ['科普','行业科普','媒体宣传','宣传'], '行业动态': ['行业重要新闻','动态','政策','管理','会议'] };
            const enhanced = articles.map(art => { let primaryCat = '灌区综合'; const text = (art.title + ' ' + (art.topicTag || '')).toLowerCase(); for (const [cat, keywords] of Object.entries(categoryMap)) { if (keywords.some(kw => text.includes(kw.toLowerCase()))) { primaryCat = cat; break; } } return { ...art, displayCat: primaryCat }; });
            const groups = {};
            enhanced.forEach(art => { if (!groups[art.displayCat]) groups[art.displayCat] = []; groups[art.displayCat].push(art); });
            const order = ['农业丰收','水利灌区','物产美食','好人好事','天气预警','科普宣传','行业动态','灌区综合'];
            let html = '';
            for (let cat of order) if (groups[cat] && groups[cat].length) html += buildSectionCard(cat, groups[cat]);
            for (let otherCat in groups) if (!order.includes(otherCat)) html += buildSectionCard(otherCat, groups[otherCat]);
            container.innerHTML = html;
        }
        function buildSectionCard(categoryName, articles) {
            const iconMap = { '农业丰收':'🌾','水利灌区':'💧','物产美食':'🍊','好人好事':'❤️','天气预警':'⛈️','科普宣传':'📚','行业动态':'📰','灌区综合':'🗞️' };
            const icon = iconMap[categoryName] || '📌';
            return `<div class="section-card"><div class="section-header"><h2>${icon} ${categoryName}</h2><div class="count">${articles.length}条</div></div><ul class="news-list">${articles.map(item => `<li class="news-item"><a href="${escapeHtml(item.url)}" target="_blank" rel="noopener noreferrer" class="news-link"><div class="news-icon">🔗</div><div class="news-content"><div class="news-title">${escapeHtml(item.title)}</div><div class="news-meta"><span>🏷️ ${escapeHtml(item.topicTag || '灌区资讯')}</span>${item.source ? `<span>📰 ${escapeHtml(item.source)}</span>` : ''}<span>🔗 点击阅读原文</span></div></div></a></li>`).join('')}</ul></div>`;
        }
        function escapeHtml(str) { if (!str) return ''; return str.replace(/[&<>]/g, function(m) { if (m === '&') return '&amp;'; if (m === '<') return '&lt;'; if (m === '>') return '&gt;'; return m; }); }
        window.addEventListener('DOMContentLoaded', () => { startCollection(); document.getElementById('refreshBtn').addEventListener('click', () => { startCollection(); }); });
    </script>
    </body>
    </html>
    ''')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)  # Render 默认使用 10000 端口