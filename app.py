<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>都江堰灌区全媒体信息采集系统</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.8/dist/chart.umd.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <script>
        tailwind.config = {
            theme: {
                extend: {
                    colors: {
                        primary: '#1e40af',
                        secondary: '#0369a1',
                        accent: '#0891b2',
                        success: '#16a34a',
                        warning: '#ca8a04',
                        danger: '#dc2626',
                        dark: '#1e293b',
                        light: '#f8fafc'
                    },
                    fontFamily: {
                        sans: ['Inter', 'system-ui', 'sans-serif'],
                    },
                }
            }
        }
    </script>
    <style type="text/tailwindcss">
        @layer utilities {
            .content-auto {
                content-visibility: auto;
            }
            .scrollbar-hide {
                -ms-overflow-style: none;
                scrollbar-width: none;
            }
            .scrollbar-hide::-webkit-scrollbar {
                display: none;
            }
            .animate-pulse-slow {
                animation: pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite;
            }
            .text-shadow {
                text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
        }
    </style>
</head>
<body class="bg-gray-50 font-sans text-gray-800 min-h-screen flex flex-col">
    <!-- 顶部导航栏 -->
    <header class="bg-gradient-to-r from-primary to-secondary text-white shadow-lg sticky top-0 z-50">
        <div class="container mx-auto px-4 py-3">
            <div class="flex items-center justify-between">
                <div class="flex items-center space-x-3">
                    <i class="fa fa-tint text-2xl text-blue-200"></i>
                    <div>
                        <h1 class="text-xl font-bold text-shadow">都江堰灌区全媒体信息采集系统</h1>
                        <p class="text-xs text-blue-200">覆盖8市41县市区 · 实时采集 · 智能分类</p>
                    </div>
                </div>
                <div class="flex items-center space-x-4">
                    <div id="systemStatus" class="flex items-center space-x-2">
                        <span class="inline-block w-3 h-3 rounded-full bg-success animate-pulse"></span>
                        <span class="text-sm">系统运行中</span>
                    </div>
                    <div class="text-sm text-blue-200">
                        <span id="currentTime"></span>
                    </div>
                </div>
            </div>
        </div>
    </header>

    <!-- 主内容区 -->
    <main class="flex-grow container mx-auto px-4 py-6">
        <!-- 统计卡片 -->
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 mb-6">
            <div class="bg-white rounded-lg shadow-md p-5 border-l-4 border-primary">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-gray-500 text-sm">今日采集总数</p>
                        <h3 id="todayTotal" class="text-3xl font-bold text-primary mt-1">0</h3>
                        <p class="text-xs text-gray-400 mt-1">较昨日 <span id="todayCompare" class="text-success">+0%</span></p>
                    </div>
                    <div class="bg-primary/10 p-3 rounded-full">
                        <i class="fa fa-newspaper-o text-primary text-xl"></i>
                    </div>
                </div>
            </div>
            <div class="bg-white rounded-lg shadow-md p-5 border-l-4 border-success">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-gray-500 text-sm">水利相关</p>
                        <h3 id="waterCount" class="text-3xl font-bold text-success mt-1">0</h3>
                        <p class="text-xs text-gray-400 mt-1">春灌、汛期、工程动态</p>
                    </div>
                    <div class="bg-success/10 p-3 rounded-full">
                        <i class="fa fa-tint text-success text-xl"></i>
                    </div>
                </div>
            </div>
            <div class="bg-white rounded-lg shadow-md p-5 border-l-4 border-warning">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-gray-500 text-sm">农业物产</p>
                        <h3 id="agricultureCount" class="text-3xl font-bold text-warning mt-1">0</h3>
                        <p class="text-xs text-gray-400 mt-1">丰收、采摘、地理标志</p>
                    </div>
                    <div class="bg-warning/10 p-3 rounded-full">
                        <i class="fa fa-leaf text-warning text-xl"></i>
                    </div>
                </div>
            </div>
            <div class="bg-white rounded-lg shadow-md p-5 border-l-4 border-accent">
                <div class="flex justify-between items-start">
                    <div>
                        <p class="text-gray-500 text-sm">待审核内容</p>
                        <h3 id="pendingCount" class="text-3xl font-bold text-accent mt-1">0</h3>
                        <p class="text-xs text-gray-400 mt-1">需要人工确认</p>
                    </div>
                    <div class="bg-accent/10 p-3 rounded-full">
                        <i class="fa fa-clock-o text-accent text-xl"></i>
                    </div>
                </div>
            </div>
        </div>

        <!-- 选项卡导航 -->
        <div class="bg-white rounded-lg shadow-md mb-6">
            <div class="border-b border-gray-200">
                <nav class="flex -mb-px">
                    <button id="tabDashboard" class="tab-btn active" onclick="switchTab('dashboard')">
                        <i class="fa fa-dashboard mr-2"></i>采集监控
                    </button>
                    <button id="tabData" class="tab-btn" onclick="switchTab('data')">
                        <i class="fa fa-database mr-2"></i>数据浏览
                    </button>
                    <button id="tabConfig" class="tab-btn" onclick="switchTab('config')">
                        <i class="fa fa-cog mr-2"></i>采集配置
                    </button>
                    <button id="tabRegions" class="tab-btn" onclick="switchTab('regions')">
                        <i class="fa fa-map-marker mr-2"></i>地区管理
                    </button>
                </nav>
            </div>

            <!-- 采集监控面板 -->
            <div id="panelDashboard" class="tab-panel p-6">
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <!-- 采集进度 -->
                    <div class="lg:col-span-2">
                        <div class="bg-gray-50 rounded-lg p-4 mb-4">
                            <h3 class="text-lg font-semibold mb-4 flex items-center">
                                <i class="fa fa-refresh mr-2 text-primary"></i>实时采集进度
                                <button id="startAllBtn" class="ml-auto bg-primary hover:bg-primary/90 text-white px-4 py-1 rounded text-sm transition" onclick="startAllCrawlers()">
                                    <i class="fa fa-play mr-1"></i>开始全部采集
                                </button>
                            </h3>
                            <div id="crawlerProgress" class="space-y-3 max-h-80 overflow-y-auto scrollbar-hide">
                                <!-- 采集进度项将在这里动态生成 -->
                            </div>
                        </div>
                        
                        <!-- 最近采集记录 -->
                        <div class="bg-gray-50 rounded-lg p-4">
                            <h3 class="text-lg font-semibold mb-4 flex items-center">
                                <i class="fa fa-history mr-2 text-primary"></i>最近采集记录
                            </h3>
                            <div id="recentRecords" class="space-y-2 max-h-64 overflow-y-auto scrollbar-hide">
                                <p class="text-gray-500 text-center py-8">暂无采集记录，点击"开始全部采集"开始</p>
                            </div>
                        </div>
                    </div>

                    <!-- 统计图表 -->
                    <div>
                        <div class="bg-gray-50 rounded-lg p-4 mb-4">
                            <h3 class="text-lg font-semibold mb-4">分类统计</h3>
                            <canvas id="categoryChart" height="250"></canvas>
                        </div>
                        <div class="bg-gray-50 rounded-lg p-4">
                            <h3 class="text-lg font-semibold mb-4">地区分布</h3>
                            <canvas id="regionChart" height="250"></canvas>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 数据浏览面板 -->
            <div id="panelData" class="tab-panel p-6 hidden">
                <!-- 搜索和筛选 -->
                <div class="bg-gray-50 rounded-lg p-4 mb-4">
                    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">关键词</label>
                            <input type="text" id="searchKeyword" placeholder="输入关键词搜索" 
                                class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">地区</label>
                            <select id="filterRegion" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50">
                                <option value="">全部地区</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">分类</label>
                            <select id="filterCategory" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50">
                                <option value="">全部分类</option>
                                <option value="水利">水利相关</option>
                                <option value="农业">农业生产</option>
                                <option value="物产">灌区物产</option>
                                <option value="天气">重大天气</option>
                                <option value="管理">灌区管理</option>
                                <option value="动态">灌区动态</option>
                                <option value="丰收">丰收讯息</option>
                                <option value="春灌">春灌信息</option>
                                <option value="汛期">汛期信息</option>
                                <option value="科普">行业科普</option>
                                <option value="宣传">媒体宣传</option>
                                <option value="美食">地方美食</option>
                                <option value="好人好事">好人好事</option>
                                <option value="其他">其他</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">时间范围</label>
                            <select id="filterTime" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50">
                                <option value="today">今天</option>
                                <option value="yesterday">昨天</option>
                                <option value="7days">近7天</option>
                                <option value="30days">近30天</option>
                                <option value="all">全部</option>
                            </select>
                        </div>
                    </div>
                    <div class="flex justify-between items-center mt-4">
                        <button id="searchBtn" class="bg-primary hover:bg-primary/90 text-white px-4 py-2 rounded transition" onclick="searchData()">
                            <i class="fa fa-search mr-1"></i>搜索
                        </button>
                        <div class="space-x-2">
                            <button class="bg-success hover:bg-success/90 text-white px-4 py-2 rounded transition" onclick="exportToExcel()">
                                <i class="fa fa-file-excel-o mr-1"></i>导出Excel
                            </button>
                            <button class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded transition" onclick="exportToJSON()">
                                <i class="fa fa-file-code-o mr-1"></i>导出JSON
                            </button>
                        </div>
                    </div>
                </div>

                <!-- 数据列表 -->
                <div class="bg-white rounded-lg shadow overflow-hidden">
                    <div class="overflow-x-auto">
                        <table class="min-w-full divide-y divide-gray-200">
                            <thead class="bg-gray-50">
                                <tr>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">标题</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">来源</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">地区</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">分类</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">发布时间</th>
                                    <th class="px-4 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">操作</th>
                                </tr>
                            </thead>
                            <tbody id="dataTableBody" class="bg-white divide-y divide-gray-200">
                                <tr>
                                    <td colspan="6" class="px-4 py-8 text-center text-gray-500">暂无数据</td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                    <!-- 分页 -->
                    <div class="bg-gray-50 px-4 py-3 flex items-center justify-between border-t border-gray-200">
                        <div class="text-sm text-gray-700">
                            显示 <span id="pageStart">0</span> 到 <span id="pageEnd">0</span> 条，共 <span id="totalRecords">0</span> 条
                        </div>
                        <div class="flex space-x-2">
                            <button id="prevPageBtn" class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50" onclick="prevPage()" disabled>
                                上一页
                            </button>
                            <button id="nextPageBtn" class="px-3 py-1 border border-gray-300 rounded text-sm disabled:opacity-50" onclick="nextPage()" disabled>
                                下一页
                            </button>
                        </div>
                    </div>
                </div>
            </div>

            <!-- 采集配置面板 -->
            <div id="panelConfig" class="tab-panel p-6 hidden">
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <!-- 采集源配置 -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h3 class="text-lg font-semibold mb-4 flex items-center">
                            <i class="fa fa-link mr-2 text-primary"></i>采集源管理
                        </h3>
                        <div id="sourceList" class="space-y-2 max-h-96 overflow-y-auto scrollbar-hide mb-4">
                            <!-- 采集源列表将在这里动态生成 -->
                        </div>
                        <button class="w-full bg-primary hover:bg-primary/90 text-white px-4 py-2 rounded transition" onclick="addSource()">
                            <i class="fa fa-plus mr-1"></i>添加采集源
                        </button>
                    </div>

                    <!-- 系统设置 -->
                    <div class="bg-gray-50 rounded-lg p-4">
                        <h3 class="text-lg font-semibold mb-4 flex items-center">
                            <i class="fa fa-cogs mr-2 text-primary"></i>系统设置
                        </h3>
                        <div class="space-y-4">
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">自动采集间隔（分钟）</label>
                                <input type="number" id="autoInterval" value="60" min="10" max="1440"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50">
                                <p class="text-xs text-gray-500 mt-1">设置为0则关闭自动采集</p>
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">每次采集最大条数</label>
                                <input type="number" id="maxPerCrawl" value="50" min="10" max="200"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50">
                            </div>
                            <div>
                                <label class="block text-sm font-medium text-gray-700 mb-1">数据保留天数</label>
                                <input type="number" id="dataRetention" value="90" min="7" max="365"
                                    class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50">
                            </div>
                            <div class="flex items-center">
                                <input type="checkbox" id="autoClassify" checked class="mr-2">
                                <label for="autoClassify" class="text-sm font-medium text-gray-700">启用自动分类</label>
                            </div>
                            <div class="flex items-center">
                                <input type="checkbox" id="autoDeduplicate" checked class="mr-2">
                                <label for="autoDeduplicate" class="text-sm font-medium text-gray-700">启用自动去重</label>
                            </div>
                            <div class="flex items-center">
                                <input type="checkbox" id="autoStart" class="mr-2">
                                <label for="autoStart" class="text-sm font-medium text-gray-700">打开页面自动开始采集</label>
                            </div>
                        </div>
                        <button class="w-full bg-success hover:bg-success/90 text-white px-4 py-2 rounded transition mt-4" onclick="saveSettings()">
                            <i class="fa fa-save mr-1"></i>保存设置
                        </button>
                    </div>
                </div>

                <!-- 关键词配置 -->
                <div class="bg-gray-50 rounded-lg p-4 mt-6">
                    <h3 class="text-lg font-semibold mb-4 flex items-center">
                        <i class="fa fa-tags mr-2 text-primary"></i>分类关键词配置
                    </h3>
                    <p class="text-sm text-gray-600 mb-4">系统将根据以下关键词自动对采集到的内容进行分类，多个关键词用逗号分隔</p>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">水利相关</label>
                            <textarea id="kwWater" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm">都江堰,水利,灌区,渠系,水库,大坝,闸门,输水,供水,节水,灌溉,引水,防洪,防汛,抗旱,水资源,水利工程</textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">农业生产</label>
                            <textarea id="kwAgriculture" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm">农业,农村,农民,三农,种植,养殖,粮食,水稻,小麦,玉米,大豆,油菜,蔬菜,茶叶,中药材,农机,农技,农资</textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">灌区物产</label>
                            <textarea id="kwProduce" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm">樱桃,桃子,枇杷,李子,杏子,梨,苹果,猕猴桃,葡萄,柑橘,柚子,橙子,草莓,蓝莓,西瓜,甜瓜,地理标志,农产品,特产,采摘节,丰收节</textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">重大天气</label>
                            <textarea id="kwWeather" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm">暴雨,洪水,干旱,高温,寒潮,大风,冰雹,雷电,台风,预警,气象,天气预报</textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">灌区管理</label>
                            <textarea id="kwManagement" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm">灌区管理,水利厅,都江堰水利发展中心,管理处,用水管理,水费,水权,调度,巡查,维护,检修</textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">春灌信息</label>
                            <textarea id="kwSpringIrrigation" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm">春灌,春耕,泡田,栽秧,插秧,关秧门,大春,备耕,育秧</textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">汛期信息</label>
                            <textarea id="kwFlood" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm">汛期,主汛期,防洪,度汛,泄洪,洪峰,水位,流量,防汛抗旱,应急响应</textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">地方美食</label>
                            <textarea id="kwFood" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm">美食,小吃,特产,餐饮,老字号,特色菜,川菜,火锅,串串,烧烤</textarea>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-gray-700 mb-1">好人好事</label>
                            <textarea id="kwGoodPeople" rows="2" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm">好人好事,见义勇为,助人为乐,道德模范,最美人物,志愿者,公益,爱心</textarea>
                        </div>
                    </div>
                    <button class="bg-success hover:bg-success/90 text-white px-4 py-2 rounded transition mt-4" onclick="saveKeywords()">
                        <i class="fa fa-save mr-1"></i>保存关键词
                    </button>
                </div>
            </div>

            <!-- 地区管理面板 -->
            <div id="panelRegions" class="tab-panel p-6 hidden">
                <div class="bg-gray-50 rounded-lg p-4 mb-6">
                    <h3 class="text-lg font-semibold mb-4 flex items-center">
                        <i class="fa fa-map mr-2 text-primary"></i>都江堰灌区覆盖范围
                        <span class="ml-2 text-sm font-normal text-gray-500">8市41县(市、区)</span>
                    </h3>
                    <div id="regionTree" class="space-y-4">
                        <!-- 地区树将在这里动态生成 -->
                    </div>
                </div>
                <div class="bg-gray-50 rounded-lg p-4">
                    <h3 class="text-lg font-semibold mb-4">地区采集统计</h3>
                    <canvas id="regionDetailChart" height="300"></canvas>
                </div>
            </div>
        </div>
    </main>

    <!-- 页脚 -->
    <footer class="bg-dark text-white py-4 mt-8">
        <div class="container mx-auto px-4 text-center text-sm text-gray-400">
            <p>都江堰灌区全媒体信息采集系统 © 2026 | 数据仅供参考，请以官方发布为准</p>
        </div>
    </footer>

    <!-- 文章详情模态框 -->
    <div id="articleModal" class="fixed inset-0 bg-black/50 z-50 hidden flex items-center justify-center p-4">
        <div class="bg-white rounded-lg shadow-xl max-w-4xl w-full max-h-[90vh] overflow-hidden flex flex-col">
            <div class="bg-primary text-white px-6 py-4 flex justify-between items-center">
                <h3 id="modalTitle" class="text-lg font-semibold truncate">文章详情</h3>
                <button onclick="closeModal()" class="text-white hover:text-gray-200">
                    <i class="fa fa-times text-xl"></i>
                </button>
            </div>
            <div class="p-6 overflow-y-auto flex-grow">
                <div class="mb-4 flex flex-wrap gap-2 text-sm text-gray-600">
                    <span><i class="fa fa-source mr-1"></i><span id="modalSource"></span></span>
                    <span><i class="fa fa-map-marker mr-1"></i><span id="modalRegion"></span></span>
                    <span><i class="fa fa-tag mr-1"></i><span id="modalCategory"></span></span>
                    <span><i class="fa fa-clock-o mr-1"></i><span id="modalTime"></span></span>
                </div>
                <div id="modalContent" class="prose max-w-none">
                    <!-- 文章内容将在这里显示 -->
                </div>
            </div>
            <div class="bg-gray-50 px-6 py-3 flex justify-end space-x-2 border-t">
                <a id="modalOriginalLink" href="#" target="_blank" class="bg-primary hover:bg-primary/90 text-white px-4 py-2 rounded transition">
                    <i class="fa fa-external-link mr-1"></i>查看原文
                </a>
                <button onclick="closeModal()" class="bg-gray-600 hover:bg-gray-700 text-white px-4 py-2 rounded transition">
                    关闭
                </button>
            </div>
        </div>
    </div>

    <script>
        // ==================== 全局变量 ====================
        const REGIONS = {
            "成都市": ["都江堰市", "彭州市", "郫都区", "温江区", "崇州市", "大邑县", "邛崃市", "双流区", "新津区", "新都区", "武侯区", "锦江区", "成华区", "青羊区", "金牛区", "成都高新区", "龙泉驿区", "青白江区", "金堂县", "简阳市"],
            "德阳市": ["什邡市", "广汉市", "绵竹市", "旌阳区", "中江县", "罗江区"],
            "绵阳市": ["安州区", "涪城区", "三台县"],
            "遂宁市": ["射洪市", "大英县", "安居区"],
            "乐山市": ["井研县"],
            "眉山市": ["仁寿县", "彭山区", "东坡区", "青神县"],
            "资阳市": ["雁江区", "安岳县", "乐至县"],
            "内江市": ["资中县"]
        };

        const CATEGORIES = [
            "水利", "农业", "物产", "天气", "管理", "动态", 
            "丰收", "春灌", "汛期", "科普", "宣传", "美食", "好人好事", "其他"
        ];

        let collectedData = JSON.parse(localStorage.getItem('collectedData') || '[]');
        let settings = JSON.parse(localStorage.getItem('settings') || JSON.stringify({
            autoInterval: 60,
            maxPerCrawl: 50,
            dataRetention: 90,
            autoClassify: true,
            autoDeduplicate: true,
            autoStart: false
        }));
        let keywords = JSON.parse(localStorage.getItem('keywords') || '{}');
        let sources = JSON.parse(localStorage.getItem('sources') || JSON.stringify([
            { id: 1, name: "四川省水利厅", url: "http://slt.sc.gov.cn", enabled: true },
            { id: 2, name: "四川省都江堰水利发展中心", url: "shturl.cc/zAyX8b3fmB", enabled: true },
            { id: 3, name: "四川在线", url: "https://sichuan.scol.com.cn", enabled: true },
            { id: 4, name: "四川新闻网", url: "https://www.newssc.org", enabled: true },
            { id: 5, name: "今日头条-四川", url: "https://www.toutiao.com/c/sichuan/", enabled: true },
            { id: 6, name: "成都日报", url: "https://www.cdrb.com.cn", enabled: true },
            { id: 7, name: "眉山日报", url: "https://www.mshw.net", enabled: true },
            { id: 8, name: "德阳日报", url: "https://www.dyrbw.com", enabled: true }
        ]));

        let currentPage = 1;
        let pageSize = 20;
        let filteredData = [];
        let autoCrawlTimer = null;
        let categoryChart = null;
        let regionChart = null;
        let regionDetailChart = null;

        // ==================== 初始化 ====================
        document.addEventListener('DOMContentLoaded', function() {
            updateCurrentTime();
            setInterval(updateCurrentTime, 1000);
            
            loadSettings();
            loadKeywords();
            initRegionTree();
            initRegionFilter();
            initCrawlerProgress();
            initCharts();
            updateStatistics();
            renderDataTable();
            
            if (settings.autoStart) {
                setTimeout(() => {
                    startAllCrawlers();
                }, 2000);
            }
            
            if (settings.autoInterval > 0) {
                startAutoCrawl();
            }
        });

        // ==================== 时间更新 ====================
        function updateCurrentTime() {
            const now = new Date();
            document.getElementById('currentTime').textContent = now.toLocaleString('zh-CN');
        }

        // ==================== 选项卡切换 ====================
        function switchTab(tabName) {
            // 隐藏所有面板
            document.querySelectorAll('.tab-panel').forEach(panel => {
                panel.classList.add('hidden');
            });
            
            // 移除所有选项卡的活动状态
            document.querySelectorAll('.tab-btn').forEach(btn => {
                btn.classList.remove('active');
            });
            
            // 显示选中的面板
            document.getElementById('panel' + tabName.charAt(0).toUpperCase() + tabName.slice(1)).classList.remove('hidden');
            
            // 设置选中选项卡的活动状态
            document.getElementById('tab' + tabName.charAt(0).toUpperCase() + tabName.slice(1)).classList.add('active');
            
            // 如果切换到地区面板，更新图表
            if (tabName === 'regions') {
                updateRegionDetailChart();
            }
        }

        // ==================== 地区树初始化 ====================
        function initRegionTree() {
            const container = document.getElementById('regionTree');
            container.innerHTML = '';
            
            Object.keys(REGIONS).forEach(city => {
                const cityDiv = document.createElement('div');
                cityDiv.className = 'bg-white rounded-lg p-3 shadow-sm';
                
                const cityHeader = document.createElement('div');
                cityHeader.className = 'flex justify-between items-center cursor-pointer';
                cityHeader.innerHTML = `
                    <div class="flex items-center">
                        <i class="fa fa-chevron-right text-gray-400 mr-2 transition-transform" id="chevron-${city.replace(/\s/g, '')}"></i>
                        <span class="font-medium">${city}</span>
                        <span class="ml-2 text-xs text-gray-500">(${REGIONS[city].length}个县市区)</span>
                    </div>
                    <label class="flex items-center">
                        <input type="checkbox" checked class="city-checkbox" data-city="${city}" onchange="toggleCity('${city}')">
                        <span class="ml-1 text-sm text-gray-600">全部采集</span>
                    </label>
                `;
                cityHeader.onclick = (e) => {
                    if (e.target.type !== 'checkbox') {
                        toggleCityExpand(city);
                    }
                };
                
                const countiesDiv = document.createElement('div');
                countiesDiv.className = 'mt-2 pl-6 hidden';
                countiesDiv.id = `counties-${city.replace(/\s/g, '')}`;
                
                REGIONS[city].forEach(county => {
                    const countyDiv = document.createElement('div');
                    countyDiv.className = 'flex justify-between items-center py-1';
                    countyDiv.innerHTML = `
                        <span class="text-sm">${county}</span>
                        <label class="flex items-center">
                            <input type="checkbox" checked class="county-checkbox" data-city="${city}" data-county="${county}">
                        </label>
                    `;
                    countiesDiv.appendChild(countyDiv);
                });
                
                cityDiv.appendChild(cityHeader);
                cityDiv.appendChild(countiesDiv);
                container.appendChild(cityDiv);
            });
        }

        function toggleCityExpand(city) {
            const chevron = document.getElementById(`chevron-${city.replace(/\s/g, '')}`);
            const counties = document.getElementById(`counties-${city.replace(/\s/g, '')}`);
            
            chevron.classList.toggle('rotate-90');
            counties.classList.toggle('hidden');
        }

        function toggleCity(city) {
            const cityCheckbox = document.querySelector(`.city-checkbox[data-city="${city}"]`);
            const countyCheckboxes = document.querySelectorAll(`.county-checkbox[data-city="${city}"]`);
            
            countyCheckboxes.forEach(checkbox => {
                checkbox.checked = cityCheckbox.checked;
            });
        }

        // ==================== 地区筛选初始化 ====================
        function initRegionFilter() {
            const select = document.getElementById('filterRegion');
            
            Object.keys(REGIONS).forEach(city => {
                const optgroup = document.createElement('optgroup');
                optgroup.label = city;
                
                REGIONS[city].forEach(county => {
                    const option = document.createElement('option');
                    option.value = `${city}-${county}`;
                    option.textContent = county;
                    optgroup.appendChild(option);
                });
                
                select.appendChild(optgroup);
            });
        }

        // ==================== 采集进度初始化 ====================
        function initCrawlerProgress() {
            const container = document.getElementById('crawlerProgress');
            container.innerHTML = '';
            
            sources.forEach(source => {
                const item = document.createElement('div');
                item.className = 'bg-white rounded p-3 flex justify-between items-center';
                item.id = `crawler-${source.id}`;
                item.innerHTML = `
                    <div class="flex items-center">
                        <span class="inline-block w-2 h-2 rounded-full bg-gray-400 mr-3" id="status-${source.id}"></span>
                        <span>${source.name}</span>
                    </div>
                    <div class="flex items-center space-x-3">
                        <span class="text-sm text-gray-500" id="progress-${source.id}">待采集</span>
                        <button class="text-primary hover:text-primary/80 text-sm" onclick="startCrawler(${source.id})" ${!source.enabled ? 'disabled' : ''}>
                            <i class="fa fa-play"></i>
                        </button>
                    </div>
                `;
                container.appendChild(item);
            });
        }

        // ==================== 图表初始化 ====================
        function initCharts() {
            // 分类统计图表
            const categoryCtx = document.getElementById('categoryChart').getContext('2d');
            categoryChart = new Chart(categoryCtx, {
                type: 'doughnut',
                data: {
                    labels: CATEGORIES,
                    datasets: [{
                        data: CATEGORIES.map(cat => collectedData.filter(item => item.category === cat).length),
                        backgroundColor: [
                            '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6',
                            '#ec4899', '#06b6d4', '#84cc16', '#f97316', '#6366f1',
                            '#a855f7', '#14b8a6', '#22c55e', '#6b7280'
                        ],
                        borderWidth: 0
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            position: 'right',
                            labels: {
                                boxWidth: 12,
                                font: {
                                    size: 11
                                }
                            }
                        }
                    }
                }
            });

            // 地区分布图表
            const regionCtx = document.getElementById('regionChart').getContext('2d');
            regionChart = new Chart(regionCtx, {
                type: 'bar',
                data: {
                    labels: Object.keys(REGIONS),
                    datasets: [{
                        label: '采集数量',
                        data: Object.keys(REGIONS).map(city => {
                            return collectedData.filter(item => item.region.startsWith(city)).length;
                        }),
                        backgroundColor: '#3b82f6',
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        }
                    }
                }
            });
        }

        function updateCharts() {
            // 更新分类统计
            categoryChart.data.datasets[0].data = CATEGORIES.map(cat => 
                collectedData.filter(item => item.category === cat).length
            );
            categoryChart.update();

            // 更新地区分布
            regionChart.data.datasets[0].data = Object.keys(REGIONS).map(city => 
                collectedData.filter(item => item.region.startsWith(city)).length
            );
            regionChart.update();
        }

        function updateRegionDetailChart() {
            const ctx = document.getElementById('regionDetailChart').getContext('2d');
            
            if (regionDetailChart) {
                regionDetailChart.destroy();
            }
            
            const allCounties = [];
            const counts = [];
            
            Object.keys(REGIONS).forEach(city => {
                REGIONS[city].forEach(county => {
                    allCounties.push(county);
                    counts.push(collectedData.filter(item => item.region === `${city}-${county}`).length);
                });
            });
            
            regionDetailChart = new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: allCounties,
                    datasets: [{
                        label: '采集数量',
                        data: counts,
                        backgroundColor: '#3b82f6',
                        borderRadius: 4
                    }]
                },
                options: {
                    responsive: true,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                precision: 0
                            }
                        },
                        x: {
                            ticks: {
                                autoSkip: false,
                                maxRotation: 90,
                                minRotation: 90,
                                font: {
                                    size: 10
                                }
                            }
                        }
                    }
                }
            });
        }

        // ==================== 统计更新 ====================
        function updateStatistics() {
            const today = new Date().toDateString();
            const todayData = collectedData.filter(item => 
                new Date(item.crawlTime).toDateString() === today
            );
            
            const yesterday = new Date();
            yesterday.setDate(yesterday.getDate() - 1);
            const yesterdayData = collectedData.filter(item => 
                new Date(item.crawlTime).toDateString() === yesterday.toDateString()
            );
            
            document.getElementById('todayTotal').textContent = todayData.length;
            
            if (yesterdayData.length > 0) {
                const change = ((todayData.length - yesterdayData.length) / yesterdayData.length * 100).toFixed(1);
                const compareEl = document.getElementById('todayCompare');
                compareEl.textContent = `${change > 0 ? '+' : ''}${change}%`;
                compareEl.className = change >= 0 ? 'text-success' : 'text-danger';
            } else {
                document.getElementById('todayCompare').textContent = '+100%';
            }
            
            document.getElementById('waterCount').textContent = 
                todayData.filter(item => ['水利', '春灌', '汛期', '管理'].includes(item.category)).length;
            
            document.getElementById('agricultureCount').textContent = 
                todayData.filter(item => ['农业', '物产', '丰收'].includes(item.category)).length;
            
            document.getElementById('pendingCount').textContent = 
                collectedData.filter(item => !item.reviewed).length;
            
            updateCharts();
        }

        // ==================== 采集功能 ====================
        function startAllCrawlers() {
            sources.forEach(source => {
                if (source.enabled) {
                    startCrawler(source.id);
                }
            });
        }

        function startCrawler(sourceId) {
            const source = sources.find(s => s.id === sourceId);
            if (!source || !source.enabled) return;
            
            const statusEl = document.getElementById(`status-${sourceId}`);
            const progressEl = document.getElementById(`progress-${sourceId}`);
            
            statusEl.className = 'inline-block w-2 h-2 rounded-full bg-warning animate-pulse mr-3';
            progressEl.textContent = '采集中...';
            
            // 模拟采集过程
            setTimeout(() => {
                const newItems = simulateCrawl(source);
                
                // 去重
                if (settings.autoDeduplicate) {
                    const existingUrls = collectedData.map(item => item.url);
                    const uniqueItems = newItems.filter(item => !existingUrls.includes(item.url));
                    
                    // 自动分类
                    if (settings.autoClassify) {
                        uniqueItems.forEach(item => {
                            item.category = classifyContent(item.title + ' ' + (item.summary || ''));
                        });
                    }
                    
                    // 添加到数据
                    collectedData = [...uniqueItems, ...collectedData];
                    
                    // 清理过期数据
                    cleanupOldData();
                    
                    // 保存到本地存储
                    saveData();
                    
                    // 更新UI
                    statusEl.className = 'inline-block w-2 h-2 rounded-full bg-success mr-3';
                    progressEl.textContent = `完成，新增${uniqueItems.length}条`;
                    
                    addRecentRecord(source.name, uniqueItems.length);
                    updateStatistics();
                    renderDataTable();
                }
            }, 1000 + Math.random() * 2000);
        }

        function simulateCrawl(source) {
            const items = [];
            const count = Math.floor(Math.random() * (settings.maxPerCrawl / 2)) + 5;
            
            // 获取所有启用的地区
            const enabledRegions = [];
            document.querySelectorAll('.county-checkbox:checked').forEach(checkbox => {
                enabledRegions.push(`${checkbox.dataset.city}-${checkbox.dataset.county}`);
            });
            
            if (enabledRegions.length === 0) return [];
            
            const titles = [
                "都江堰灌区春灌工作有序推进",
                "XX县迎来樱桃丰收季",
                "XX市开展水利工程安全检查",
                "XX区举办首届枇杷采摘节",
                "XX县发布暴雨蓝色预警",
                "XX市加强灌区用水管理",
                "XX区水稻种植面积稳步增长",
                "XX县获评地理标志产品",
                "XX市开展防汛应急演练",
                "XX区好人好事暖人心",
                "XX县特色农产品走出国门",
                "XX市水利工程建设进展顺利",
                "XX区茶叶喜获丰收",
                "XX县开展农业技术培训",
                "XX市灌区现代化改造加速推进"
            ];
            
            for (let i = 0; i < count; i++) {
                const region = enabledRegions[Math.floor(Math.random() * enabledRegions.length)];
                const title = titles[Math.floor(Math.random() * titles.length)].replace(/XX/g, region.split('-')[1]);
                
                items.push({
                    id: Date.now() + i,
                    title: title,
                    source: source.name,
                    region: region,
                    url: `${source.url}/article/${Date.now() + i}`,
                    summary: `这是关于${region.split('-')[1]}的一条新闻，内容涉及${title}。本文详细介绍了相关情况，为读者提供了全面的信息。`,
                    content: `<p>这是关于${region.split('-')[1]}的一条新闻，内容涉及${title}。</p><p>本文详细介绍了相关情况，为读者提供了全面的信息。都江堰灌区作为全国最大的灌区，覆盖8市41县市区，灌溉面积达1164.7万亩。</p><p>近年来，灌区不断推进现代化改造，提高水资源利用效率，为保障粮食安全和促进地方经济发展做出了重要贡献。</p>`,
                    category: "其他",
                    publishTime: new Date().toISOString(),
                    crawlTime: new Date().toISOString(),
                    reviewed: false
                });
            }
            
            return items;
        }

        function classifyContent(content) {
            const contentLower = content.toLowerCase();
            
            // 检查关键词
            if (matchKeywords(contentLower, keywords.water || [])) return "水利";
            if (matchKeywords(contentLower, keywords.springIrrigation || [])) return "春灌";
            if (matchKeywords(contentLower, keywords.flood || [])) return "汛期";
            if (matchKeywords(contentLower, keywords.management || [])) return "管理";
            if (matchKeywords(contentLower, keywords.agriculture || [])) return "农业";
            if (matchKeywords(contentLower, keywords.produce || [])) return "物产";
            if (contentLower.includes('丰收')) return "丰收";
            if (matchKeywords(contentLower, keywords.weather || [])) return "天气";
            if (matchKeywords(contentLower, keywords.food || [])) return "美食";
            if (matchKeywords(contentLower, keywords.goodPeople || [])) return "好人好事";
            if (contentLower.includes('科普') || contentLower.includes('知识')) return "科普";
            if (contentLower.includes('宣传') || contentLower.includes('媒体')) return "宣传";
            if (contentLower.includes('动态') || contentLower.includes('新闻')) return "动态";
            
            return "其他";
        }

        function matchKeywords(content, keywordList) {
            return keywordList.some(keyword => content.includes(keyword.toLowerCase()));
        }

        function addRecentRecord(sourceName, count) {
            const container = document.getElementById('recentRecords');
            
            // 移除"暂无采集记录"提示
            const emptyTip = container.querySelector('.text-center');
            if (emptyTip) {
                emptyTip.remove();
            }
            
            const record = document.createElement('div');
            record.className = 'bg-white rounded p-2 text-sm flex justify-between items-center';
            record.innerHTML = `
                <div>
                    <span class="font
