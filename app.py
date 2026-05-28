@app.route("/")
def index():
    return render_template_string('''
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>都江堰灌区资讯采集</title>
    <style>
        * { margin:0; padding:0; box-sizing:border-box; }
        body { background:#f0f7f0; font-family: system-ui, sans-serif; padding:20px; color:#1e3a2f; }
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
        <h1>🌾 都江堰灌区·智采千里眼 <span>八市41县市区</span></h1>
        <div class="sub">📍 成都·绵阳·德阳·眉山·乐山·雅安·资阳·遂宁 | 农业水利·物产·好人好事·灌区动态·美食</div>
        <div class="city-badge"><div>🏙️ 成都</div><div>绵阳</div><div>德阳</div><div>眉山</div><div>乐山</div><div>雅安</div><div>资阳</div><div>遂宁</div><div>🍒 水果/蔬菜/茶叶</div><div>🎉 丰收节/采摘节</div></div>
    </div>
    <div class="control-bar">
        <div class="status" id="statusArea"><span>🟢 就绪</span></div>
        <button class="btn-refresh" id="refreshBtn">🔄 立即采集</button>
    </div>
    <div class="stats">📊 共采集 <span id="totalCount">0</span> 条 · 涵盖主题 <span id="topicCount">0</span></div>
    <div id="resultsContainer" class="results-grid"><div class="empty-msg">✨ 打开页面自动采集，请稍后...</div></div>
    <footer>数据来源于公开网络，仅用于学习</footer>
</div>
<script>
    const API_URL = '/api/collect';
    async function startCollection() {
        const statusDiv = document.getElementById('statusArea');
        const refreshBtn = document.getElementById('refreshBtn');
        const resultsDiv = document.getElementById('resultsContainer');
        const totalSpan = document.getElementById('totalCount');
        const topicSpan = document.getElementById('topicCount');
        statusDiv.innerHTML = '<div class="spinner"></div> 🔍 正在采集资讯（约15-30秒）...';
        refreshBtn.disabled = true;
        refreshBtn.style.opacity = '0.6';
        resultsDiv.innerHTML = '<div class="empty-msg">⏳ 请求后端中，请耐心等待...</div>';
        try {
            const response = await fetch(API_URL);
            if (!response.ok) throw new Error(`HTTP ${response.status}`);
            const data = await response.json();
            console.log('后端返回数据:', data);
            if (data.success && Array.isArray(data.results)) {
                if (data.results.length === 0) {
                    resultsDiv.innerHTML = '<div class="empty-msg">📭 暂无相关资讯，可尝试刷新或稍后再来。</div>';
                } else {
                    renderGroupedResults(data.results);
                }
                totalSpan.innerText = data.total || 0;
                const topics = new Set(data.results.map(item => item.topicTag).filter(Boolean));
                topicSpan.innerText = topics.size;
                statusDiv.innerHTML = `✅ 采集完成 · ${data.results.length} 条最新资讯`;
            } else {
                throw new Error(data.message || '返回数据格式错误');
            }
        } catch (err) {
            console.error('采集错误:', err);
            resultsDiv.innerHTML = `<div class="empty-msg">❌ 采集失败：${err.message}<br>请检查后端服务是否正常，稍后重试。</div>`;
            statusDiv.innerHTML = '⚠️ 采集异常';
        } finally {
            refreshBtn.disabled = false;
            refreshBtn.style.opacity = '1';
        }
    }
    function renderGroupedResults(articles) {
        const categoryMap = {
            '农业丰收': ['丰收','春灌','农业','采摘节','丰收节','物产','水果','蔬菜','猕猴桃','柑橘','樱桃','枇杷','蓝莓','西瓜','农产品','地理标志'],
            '水利灌区': ['水利','灌区管理','都江堰','汛期','灌区动态','水资源'],
            '好人好事': ['好人','好事','暖心','助农','志愿'],
            '物产美食': ['美食','茶叶','中药材','特色农产品','品牌','采摘','水果节','甜瓜','草莓'],
            '天气预警': ['天气','气象','汛情','重大天气'],
            '科普宣传': ['科普','行业科普','媒体宣传','宣传'],
            '行业动态': ['行业重要新闻','动态','政策','管理','会议']
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