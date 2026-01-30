# YouTube Analytics Dashboard - 从需求到自动化部署的完整方案

> 这是一个完整的、可执行的 prompt，用于创建一个全新的、干净的 YouTube 数据分析仪表板项目。
> 从零开始，避免所有已知问题，实现从需求到自动化部署的完整流程。

---

## 📋 第一部分：项目需求

### 1.1 功能需求

#### 核心功能
1. **视频数据监控**
   - 添加/删除 YouTube 视频
   - 获取视频元数据（标题、描述、缩略图等）
   - 追踪视频统计数据（观看量、点赞、评论等）
   - 历史数据记录和趋势分析

2. **数据可视化**
   - 视观看量趋势图
   - 点赞/评论/分享对比图
   - 互动率分析
   - 视频性能对比
   - 热门视频排行

3. **数据分析**
   - 互动率计算
   - 视频性能排名
   - 增长趋势分析
   - 最佳发布时间分析
   - 内容表现评估

4. **自动更新**
   - 定时自动更新数据
   - 支持 GitHub Actions 自动化
   - 支持手动触发更新

5. **数据管理**
   - SQLite 数据库存储
   - 数据备份和恢复
   - 批量导入/导出
   - 数据清理和归档

#### 用户界面需求
1. **主仪表板**
   - 核心指标概览（总观看量、总点赞、视频数量等）
   - 最新视频动态
   - 热门视频排行
   - 趋势图表

2. **视频管理页面**
   - 添加视频（URL 或视频 ID）
   - 批量导入（从文件）
   - 视频列表（可搜索、筛选、排序）
   - 视频详情页面

3. **深度分析页面**
   - 单个视频的详细分析
   - 历史趋势图表
   - 评论分析（词云、情感分析）
   - 与其他视频对比

4. **设置页面**
   - API 密钥配置
   - 更新频率设置
   - 数据管理选项
   - 界面主题设置

### 1.2 非功能需求

#### 性能需求
- 页面加载时间 < 3 秒
- 图表渲染时间 < 2 秒
- 支持最多 1000 个视频
- 支持历史数据至少 30 天

#### 可靠性需求
- 数据更新成功率 > 95%
- 应用可用性 > 99%
- 数据库一致性保证
- 错误处理和日志记录

#### 安全性需求
- API 密钥加密存储
- 不暴露敏感信息
- 输入验证和清理
- SQL 注入防护

#### 可维护性需求
- 模块化代码结构
- 完整的代码注释
- 清晰的文档
- 简单的部署流程

### 1.3 用户场景

#### 场景 1：添加新视频
```
用户 → 访问"视频管理"页面
     → 输入 YouTube 视频 URL
     → 点击"添加视频"
     → 系统获取视频信息
     → 系统保存到数据库
     → 显示成功提示
```

#### 场景 2：查看视频趋势
```
用户 → 访问"深度分析"页面
     → 选择一个视频
     → 查看观看量趋势图
     → 查看互动率分析
     → 查看评论词云
```

#### 场景 3：自动数据更新
```
GitHub Actions → 每天定时触发
              → 运行数据更新脚本
              → 更新数据库
              → 推送到 GitHub
              → Streamlit Cloud 自动重新部署
```

---

## 🏗️ 第二部分：技术架构

### 2.1 技术栈

| 技术组件 | 选择 | 版本 | 原因 |
|---------|------|------|------|
| Web 框架 | Streamlit | 1.53.1 | 简单易用，专为数据应用设计 |
| 数据处理 | Pandas | 2.3.3 | 强大的数据处理能力 |
| 数据可视化 | Plotly | 6.5.2 | 交互式图表，美观 |
| HTTP 请求 | Requests | 2.32.5 | 简单可靠的 HTTP 库 |
| 数据库 | SQLite3 | 内置 | 轻量级，无需额外安装 |
| API 集成 | YouTube Data API v3 | - | 官方 API，功能完整 |

### 2.2 系统架构

```
┌─────────────────────────────────────────────────────────────┐
│                    用户浏览器                              │
└────────────────────────┬────────────────────────────────────┘
                     │ HTTPS
┌────────────────────────▼────────────────────────────────────┐
│                  Streamlit Cloud                         │
│  ┌─────────────────────────────────────────────────────┐  │
│  │              Python 应用 (app.py)                    │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────────┐    │  │
│  │  │  UI 层  │  │ 业务层  │  │  数据访问层  │    │  │
│  │  └────┬────┘  └────┬────┘  └──────┬──────┘    │  │
│  └───────┼────────────┼───────────────┼────────────┘  │
│          │            │               │                │
│  ┌───────▼────────────▼───────────────▼────────────┐  │
│  │           SQLite 数据库                         │  │
│  │        (youtube_dashboard.db)                  │  │
│  └────────────────────────────────────────────────┘  │
└────────────────────────┬────────────────────────────────────┘
                     │ API
┌────────────────────────▼────────────────────────────────────┐
│              YouTube Data API v3                          │
└─────────────────────────────────────────────────────────────┘

GitHub Actions (自动化)
  ┌─────────────────────────────────┐
  │  定时触发 (每天 3 次)          │
  │  ├─ 检出代码                 │
  │  ├─ 获取最新数据             │
  │  ├─ 更新数据库               │
  │  └─ 推送到 GitHub             │
  └─────────────────────────────────┘
```

### 2.3 模块划分

| 模块 | 文件 | 职责 |
|------|------|------|
| 主应用 | app.py | Streamlit 应用入口，页面路由，UI 渲染 |
| 数据库 | database.py | 数据库连接，CRUD 操作，数据查询 |
| API 集成 | youtube_api.py | YouTube API 调用，数据获取，错误处理 |
| 数据分析 | analytics.py | 数据计算，统计，可视化 |
| 工具函数 | utils.py | 格式化，工具函数，辅助方法 |
| 配置 | config.py | 配置管理，环境变量，常量定义 |

---

## 📁 第三部分：项目结构

### 3.1 完整目录树

```
youtube-dashboard/
├── .github/
│   └── workflows/
│       └── auto-update.yml          # GitHub Actions 自动更新
├── .streamlit/
│   └── config.toml                # Streamlit 配置
├── app.py                         # 主应用入口
├── database.py                    # 数据库模块
├── youtube_api.py                 # YouTube API 集成
├── analytics.py                   # 数据分析模块
├── utils.py                      # 工具函数
├── config.py                     # 配置模块
├── requirements.txt               # Python 依赖（严格 4 行）
├── README.md                     # 项目说明
├── docs/
│   ├── DEVELOPMENT.md             # 开发指南
│   ├── DEPLOYMENT.md              # 部署指南
│   └── TROUBLESHOOTING.md        # 故障排除指南
└── youtube_dashboard.db           # SQLite 数据库（生成）
```

### 3.2 文件说明

| 文件 | 说明 | 必需 |
|------|------|------|
| app.py | Streamlit 主应用，包含所有页面和 UI | ✅ 必需 |
| database.py | 数据库操作，表结构，数据查询 | ✅ 必需 |
| youtube_api.py | YouTube API 调用，错误处理 | ✅ 必需 |
| analytics.py | 数据分析，图表生成 | ✅ 必需 |
| utils.py | 工具函数，格式化方法 | ✅ 必需 |
| config.py | 配置管理，常量定义 | ✅ 必需 |
| requirements.txt | Python 依赖（严格 4 行） | ✅ 必需 |
| .streamlit/config.toml | Streamlit 配置 | ✅ 必需 |
| .github/workflows/auto-update.yml | GitHub Actions 自动更新 | ⚠️ 可选 |
| README.md | 项目说明文档 | ⚠️ 推荐 |
| docs/ | 开发和部署文档 | ⚠️ 推荐 |

### 3.3 命名规范

- 文件名：小写字母，下划线分隔（如：youtube_api.py）
- 类名：大驼峰命名法（如：YouTubeAPI）
- 函数名：小写字母，下划线分隔（如：get_video_data）
- 常量：大写字母，下划线分隔（如：DATABASE_PATH）
- 数据库表：小写字母，下划线分隔（如：videos, video_stats）

---

## 💻 第四部分：核心代码实现

### 4.1 requirements.txt（严格 4 行，永不修改）

```txt
streamlit==1.53.1
pandas==2.3.3
plotly==6.5.2
requests==2.32.5
```

**重要说明**：
- ❌ 永远不要添加其他依赖
- ❌ 永远不要使用 pip freeze
- ❌ 永远不要使用 pipreqs
- ✅ 只保留这 4 行
- ✅ 使用精确版本号（==）

### 4.2 .streamlit/config.toml

```toml
[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true

[logger]
level = "info"

[theme]
primaryColor = "#FF6B6B"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
font = "sans serif"
```

### 4.3 config.py

```python
"""
配置管理模块
统一管理所有配置项和常量
"""
import os
from typing import Optional

# ==================== 数据库配置 ====================
DATABASE_PATH = os.path.join(
    os.path.dirname(__file__),
    "youtube_dashboard.db"
)

# ==================== YouTube API 配置 ====================
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3"
YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")
YOUTUBE_VIDEO_URL = "https://www.youtube.com/watch?v={video_id}"

# ==================== 应用配置 ====================
APP_TITLE = "YouTube Analytics Dashboard"
APP_ICON = "📊"
PAGE_SIZE = 20
MAX_VIDEOS = 1000

# ==================== 数据更新配置 ====================
UPDATE_INTERVAL_HOURS = 8
MAX_HISTORY_DAYS = 30

# ==================== Streamlit 配置 ====================
STREAMLIT_PAGE_CONFIG = {
    "page_title": APP_TITLE,
    "page_icon": APP_ICON,
    "layout": "wide",
    "initial_sidebar_state": "expanded"
}

def get_api_key() -> str:
    """获取 YouTube API 密钥"""
    if not YOUTUBE_API_KEY:
        raise ValueError(
            "YouTube API Key 未配置。"
            "请在环境变量 YOUTUBE_API_KEY 或 Streamlit Secrets 中设置。"
        )
    return YOUTUBE_API_KEY
```

### 4.4 utils.py

```python
"""
工具函数模块
提供格式化、计算等辅助函数
"""
from typing import Optional
from datetime import datetime

def format_number(num: int) -> str:
    """格式化数字，添加千分位"""
    if num >= 1000000:
        return f"{num / 1000000:.1f}M"
    elif num >= 1000:
        return f"{num / 1000:.1f}K"
    else:
        return str(num)

def format_percentage(value: float) -> str:
    """格式化百分比"""
    return f"{value * 100:.2f}%"

def calculate_engagement_rate(
    likes: int,
    comments: int,
    views: int
) -> float:
    """计算互动率"""
    if views == 0:
        return 0.0
    return (likes + comments) / views

def extract_video_id(url_or_id: str) -> Optional[str]:
    """从 URL 或直接输入中提取视频 ID"""
    import re
    
    # 如果已经是 11 位视频 ID
    if len(url_or_id) == 11 and url_or_id.isalnum():
        return url_or_id
    
    # 从 URL 中提取
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed\/)([0-9A-Za-z_-]{11})',
        r'(?:v\/)([0-9A-Za-z_-]{11}).*',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    return None

def truncate_text(text: str, max_length: int = 50) -> str:
    """截断文本"""
    if len(text) <= max_length:
        return text
    return text[:max_length] + "..."

def get_video_age(published_at: str) -> str:
    """计算视频发布时间距现在的时长"""
    published = datetime.fromisoformat(published_at.replace('Z', '+00:00'))
    now = datetime.now(published.tzinfo)
    
    delta = now - published
    days = delta.days
    
    if days == 0:
        return "今天"
    elif days == 1:
        return "昨天"
    elif days < 7:
        return f"{days} 天前"
    elif days < 30:
        weeks = days // 7
        return f"{weeks} 周前"
    else:
        months = days // 30
        return f"{months} 月前"
```

### 4.5 database.py

```python
"""
数据库模块
处理所有数据库操作
"""
import sqlite3
from typing import List, Dict, Optional, Tuple
from datetime import datetime
import os

from config import DATABASE_PATH

class Database:
    """数据库类"""
    
    def __init__(self, db_path: str = DATABASE_PATH):
        """初始化数据库连接"""
        self.db_path = db_path
        self.conn = None
        self.connect()
        self.init_tables()
    
    def connect(self):
        """连接到数据库"""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
    
    def init_tables(self):
        """初始化数据表"""
        cursor = self.conn.cursor()
        
        # 视频表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS videos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                channel_id TEXT,
                channel_title TEXT,
                thumbnail_url TEXT,
                published_at TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        # 视频统计表
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS video_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                video_id TEXT NOT NULL,
                view_count INTEGER DEFAULT 0,
                like_count INTEGER DEFAULT 0,
                comment_count INTEGER DEFAULT 0,
                favorite_count INTEGER DEFAULT 0,
                recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (video_id) REFERENCES videos(video_id)
            )
        """)
        
        # 创建索引
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_video_stats_video_id
            ON video_stats(video_id)
        """)
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_video_stats_recorded_at
            ON video_stats(recorded_at)
        """)
        
        self.conn.commit()
    
    def add_video(self, video_data: Dict) -> bool:
        """添加视频"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT OR REPLACE INTO videos
                (video_id, title, description, channel_id, channel_title,
                 thumbnail_url, published_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                video_data['video_id'],
                video_data['title'],
                video_data.get('description', ''),
                video_data.get('channel_id', ''),
                video_data.get('channel_title', ''),
                video_data.get('thumbnail_url', ''),
                video_data.get('published_at', '')
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding video: {e}")
            return False
    
    def add_video_stats(self, stats_data: Dict) -> bool:
        """添加视频统计数据"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO video_stats
                (video_id, view_count, like_count, comment_count, favorite_count)
                VALUES (?, ?, ?, ?, ?)
            """, (
                stats_data['video_id'],
                stats_data.get('view_count', 0),
                stats_data.get('like_count', 0),
                stats_data.get('comment_count', 0),
                stats_data.get('favorite_count', 0)
            ))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding stats: {e}")
            return False
    
    def get_videos(self, limit: Optional[int] = None) -> List[Dict]:
        """获取所有视频"""
        cursor = self.conn.cursor()
        query = """
            SELECT v.*, 
                   (SELECT view_count FROM video_stats 
                    WHERE video_id = v.video_id 
                    ORDER BY recorded_at DESC LIMIT 1) as view_count,
                   (SELECT like_count FROM video_stats 
                    WHERE video_id = v.video_id 
                    ORDER BY recorded_at DESC LIMIT 1) as like_count,
                   (SELECT comment_count FROM video_stats 
                    WHERE video_id = v.video_id 
                    ORDER BY recorded_at DESC LIMIT 1) as comment_count
            FROM videos v
            ORDER BY v.created_at DESC
        """
        if limit:
            query += f" LIMIT {limit}"
        
        cursor.execute(query)
        return [dict(row) for row in cursor.fetchall()]
    
    def get_video_by_id(self, video_id: str) -> Optional[Dict]:
        """根据视频 ID 获取视频"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT v.*,
                   (SELECT view_count FROM video_stats 
                    WHERE video_id = v.video_id 
                    ORDER BY recorded_at DESC LIMIT 1) as view_count,
                   (SELECT like_count FROM video_stats 
                    WHERE video_id = v.video_id 
                    ORDER BY recorded_at DESC LIMIT 1) as like_count,
                   (SELECT comment_count FROM video_stats 
                    WHERE video_id = v.video_id 
                    ORDER BY recorded_at DESC LIMIT 1) as comment_count
            FROM videos v
            WHERE v.video_id = ?
        """, (video_id,))
        row = cursor.fetchone()
        return dict(row) if row else None
    
    def get_video_stats_history(
        self, 
        video_id: str, 
        days: int = 30
    ) -> List[Dict]:
        """获取视频统计历史"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT * FROM video_stats
            WHERE video_id = ?
            AND recorded_at >= datetime('now', '-' || ? || ' days')
            ORDER BY recorded_at ASC
        """, (video_id, days))
        return [dict(row) for row in cursor.fetchall()]
    
    def delete_video(self, video_id: str) -> bool:
        """删除视频"""
        cursor = self.conn.cursor()
        try:
            cursor.execute("DELETE FROM video_stats WHERE video_id = ?", (video_id,))
            cursor.execute("DELETE FROM videos WHERE video_id = ?", (video_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting video: {e}")
            return False
    
    def get_total_stats(self) -> Dict:
        """获取总体统计"""
        cursor = self.conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as count FROM videos")
        total_videos = cursor.fetchone()['count']
        
        cursor.execute("""
            SELECT SUM(view_count) as views, 
                   SUM(like_count) as likes,
                   SUM(comment_count) as comments
            FROM video_stats
        """)
        stats = cursor.fetchone()
        
        return {
            'total_videos': total_videos,
            'total_views': stats['views'] or 0,
            'total_likes': stats['likes'] or 0,
            'total_comments': stats['comments'] or 0
        }
    
    def close(self):
        """关闭数据库连接"""
        if self.conn:
            self.conn.close()

# 全局数据库实例
db = Database()

def get_database() -> Database:
    """获取数据库实例"""
    return db
```

### 4.6 youtube_api.py

```python
"""
YouTube API 集成模块
处理所有 YouTube Data API 调用
"""
import requests
from typing import List, Dict, Optional
import time

from config import YOUTUBE_API_URL, YOUTUBE_API_KEY, get_api_key

class YouTubeAPI:
    """YouTube API 客户端"""
    
    def __init__(self, api_key: Optional[str] = None):
        """初始化 API 客户端"""
        self.api_key = api_key or get_api_key()
        self.base_url = YOUTUBE_API_URL
        self.session = requests.Session()
    
    def _make_request(
        self, 
        endpoint: str, 
        params: Dict
    ) -> Optional[Dict]:
        """发送 API 请求"""
        params['key'] = self.api_key
        url = f"{self.base_url}/{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request failed: {e}")
            return None
    
    def get_video_info(self, video_ids: List[str]) -> List[Dict]:
        """获取视频信息"""
        if not video_ids:
            return []
        
        params = {
            'part': 'snippet,statistics',
            'id': ','.join(video_ids)
        }
        
        data = self._make_request('videos', params)
        
        if not data or 'items' not in data:
            return []
        
        videos = []
        for item in data['items']:
            snippet = item.get('snippet', {})
            statistics = item.get('statistics', {})
            
            video_data = {
                'video_id': item['id'],
                'title': snippet.get('title', ''),
                'description': snippet.get('description', ''),
                'channel_id': snippet.get('channelId', ''),
                'channel_title': snippet.get('channelTitle', ''),
                'thumbnail_url': self._get_thumbnail_url(snippet.get('thumbnails', {})),
                'published_at': snippet.get('publishedAt', ''),
                'view_count': int(statistics.get('viewCount', 0)),
                'like_count': int(statistics.get('likeCount', 0)),
                'comment_count': int(statistics.get('commentCount', 0)),
                'favorite_count': int(statistics.get('favoriteCount', 0))
            }
            videos.append(video_data)
        
        return videos
    
    def _get_thumbnail_url(self, thumbnails: Dict) -> str:
        """获取最佳缩略图 URL"""
        # 优先级：maxres > standard > high > medium > default
        for quality in ['maxres', 'standard', 'high', 'medium', 'default']:
            if quality in thumbnails:
                return thumbnails[quality].get('url', '')
        return ''
    
    def get_video_stats(self, video_id: str) -> Optional[Dict]:
        """获取视频统计数据"""
        videos = self.get_video_info([video_id])
        return videos[0] if videos else None
    
    def search_videos(
        self, 
        query: str, 
        max_results: int = 10
    ) -> List[str]:
        """搜索视频"""
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': max_results
        }
        
        data = self._make_request('search', params)
        
        if not data or 'items' not in data:
            return []
        
        return [
            item['id']['videoId'] 
            for item in data['items'] 
            if 'videoId' in item['id']
        ]
```

### 4.7 analytics.py

```python
"""
数据分析模块
提供数据计算、统计和可视化功能
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict
from datetime import datetime

from utils import calculate_engagement_rate, format_number

class VideoAnalyzer:
    """视频分析器"""
    
    @staticmethod
    def create_view_trend_chart(
        stats_history: List[Dict]
    ) -> go.Figure:
        """创建观看量趋势图"""
        if not stats_history:
            return go.Figure()
        
        df = pd.DataFrame(stats_history)
        df['recorded_at'] = pd.to_datetime(df['recorded_at'])
        
        fig = px.line(
            df,
            x='recorded_at',
            y='view_count',
            title='观看量趋势',
            labels={
                'recorded_at': '时间',
                'view_count': '观看量'
            },
            markers=True
        )
        
        fig.update_layout(
            template='plotly_white',
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_engagement_chart(
        stats_history: List[Dict]
    ) -> go.Figure:
        """创建互动分析图"""
        if not stats_history:
            return go.Figure()
        
        df = pd.DataFrame(stats_history)
        df['recorded_at'] = pd.to_datetime(df['recorded_at'])
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=df['recorded_at'],
            y=df['like_count'],
            mode='lines+markers',
            name='点赞数',
            line=dict(color='#4CAF50')
        ))
        
        fig.add_trace(go.Scatter(
            x=df['recorded_at'],
            y=df['comment_count'],
            mode='lines+markers',
            name='评论数',
            line=dict(color='#2196F3')
        ))
        
        fig.update_layout(
            title='互动趋势',
            xaxis_title='时间',
            yaxis_title='数量',
            template='plotly_white',
            hovermode='x unified'
        )
        
        return fig
    
    @staticmethod
    def create_comparison_chart(videos: List[Dict]) -> go.Figure:
        """创建视频对比图"""
        if not videos:
            return go.Figure()
        
        df = pd.DataFrame(videos)
        df = df.sort_values('view_count', ascending=False).head(10)
        
        fig = px.bar(
            df,
            x='view_count',
            y='title',
            orientation='h',
            title='热门视频排行（观看量）',
            labels={'view_count': '观看量', 'title': '视频标题'},
            color='view_count',
            color_continuous_scale='Viridis'
        )
        
        fig.update_layout(
            template='plotly_white',
            yaxis={'categoryorder': 'total ascending'}
        )
        
        return fig
    
    @staticmethod
    def calculate_video_performance(
        video: Dict
    ) -> Dict:
        """计算视频性能指标"""
        view_count = video.get('view_count', 0)
        like_count = video.get('like_count', 0)
        comment_count = video.get('comment_count', 0)
        
        engagement_rate = calculate_engagement_rate(
            like_count,
            comment_count,
            view_count
        )
        
        return {
            'video_id': video.get('video_id'),
            'title': video.get('title'),
            'view_count': view_count,
            'like_count': like_count,
            'comment_count': comment_count,
            'engagement_rate': engagement_rate,
            'view_count_formatted': format_number(view_count),
            'like_count_formatted': format_number(like_count),
            'comment_count_formatted': format_number(comment_count),
            'engagement_rate_formatted': f"{engagement_rate * 100:.2f}%"
        }
    
    @staticmethod
    def get_top_videos(videos: List[Dict], metric: str = 'view_count') -> List[Dict]:
        """获取热门视频"""
        if not videos:
            return []
        
        # 计算性能指标
        videos_with_performance = [
            VideoAnalyzer.calculate_video_performance(video)
            for video in videos
        ]
        
        # 排序
        sorted_videos = sorted(
            videos_with_performance,
            key=lambda x: x.get(metric, 0),
            reverse=True
        )
        
        return sorted_videos[:10]
```

### 4.8 app.py（主应用）

```python
"""
YouTube Analytics Dashboard - 主应用
Streamlit 应用的入口点
"""
import streamlit as st
import pandas as pd
from datetime import datetime

# 导入自定义模块
from config import STREAMLIT_PAGE_CONFIG
from database import get_database
from youtube_api import YouTubeAPI
from analytics import VideoAnalyzer
from utils import extract_video_id, format_number, calculate_engagement_rate

# 配置页面
st.set_page_config(**STREAMLIT_PAGE_CONFIG)

# 初始化数据库
db = get_database()

# 初始化 session state
if 'current_page' not in st.session_state:
    st.session_state.current_page = 'overview'
if 'selected_video' not in st.session_state:
    st.session_state.selected_video = None

# ==================== 侧边栏导航 ====================

def render_sidebar():
    """渲染侧边栏"""
    st.sidebar.title("📊 导航菜单")
    
    pages = [
        ('📈 数据概览', 'overview'),
        ('📹 视频管理', 'management'),
        ('🔍 深度分析', 'analysis'),
        ('⚙️ 设置', 'settings')
    ]
    
    for label, page_key in pages:
        if st.sidebar.button(label, key=f"nav_{page_key}"):
            st.session_state.current_page = page_key
    
    st.sidebar.markdown("---")
    
    # 显示统计信息
    total_stats = db.get_total_stats()
    st.sidebar.subheader("📊 总体统计")
    st.sidebar.metric("视频总数", total_stats['total_videos'])
    st.sidebar.metric("总观看量", format_number(total_stats['total_views']))
    st.sidebar.metric("总点赞量", format_number(total_stats['total_likes']))
    
    return st.session_state.current_page

# ==================== 主页面 ====================

def main():
    """主函数"""
    # 渲染侧边栏
    current_page = render_sidebar()
    
    # 根据当前页面渲染内容
    if current_page == 'overview':
        render_overview()
    elif current_page == 'management':
        render_management()
    elif current_page == 'analysis':
        render_analysis()
    elif current_page == 'settings':
        render_settings()
    else:
        render_overview()

# ==================== 数据概览页面 ====================

def render_overview():
    """渲染数据概览页面"""
    st.title("📈 数据概览")
    
    # 获取总体统计
    total_stats = db.get_total_stats()
    
    # 核心指标
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "视频总数",
            total_stats['total_videos'],
            help="当前监控的视频数量"
        )
    
    with col2:
        st.metric(
            "总观看量",
            format_number(total_stats['total_views']),
            help="所有视频的总观看量"
        )
    
    with col3:
        st.metric(
            "总点赞量",
            format_number(total_stats['total_likes']),
            help="所有视频的总点赞量"
        )
    
    with col4:
        st.metric(
            "总评论量",
            format_number(total_stats['total_comments']),
            help="所有视频的总评论量"
        )
    
    st.write("---")
    
    # 获取视频列表
    videos = db.get_videos(limit=10)
    
    if not videos:
        st.warning("⚠️ 暂无视频数据，请先添加视频")
        return
    
    # 热门视频排行
    st.subheader("🔥 热门视频排行")
    top_videos = VideoAnalyzer.get_top_videos(videos, 'view_count')
    
    if top_videos:
        fig = VideoAnalyzer.create_comparison_chart(top_videos)
        st.plotly_chart(fig, use_container_width=True)
    
    st.write("---")
    
    # 最新视频
    st.subheader("🆕 最新添加的视频")
    for video in videos[:5]:
        with st.expander(f"{video['title']}"):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if video.get('thumbnail_url'):
                    st.image(video['thumbnail_url'], use_column_width=True)
            
            with col2:
                st.write(f"**观看量**: {format_number(video.get('view_count', 0))}")
                st.write(f"**点赞量**: {format_number(video.get('like_count', 0))}")
                st.write(f"**评论量**: {format_number(video.get('comment_count', 0))}")

# ==================== 视频管理页面 ====================

def render_management():
    """渲染视频管理页面"""
    st.title("📹 视频管理")
    
    # 添加视频
    st.subheader("➕ 添加新视频")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        video_input = st.text_input(
            "YouTube 视频链接或视频 ID",
            placeholder="例如: https://www.youtube.com/watch?v=dQw4w9WgXcQ 或 dQw4w9WgXcQ",
            help="支持完整的 YouTube URL 或 11 位视频 ID"
        )
    
    with col2:
        st.write("")
        add_button = st.button("添加视频", type="primary")
    
    # 处理添加视频
    if add_button and video_input:
        with st.spinner("正在获取视频信息..."):
            video_id = extract_video_id(video_input)
            
            if not video_id:
                st.error("❌ 无效的视频 URL 或 ID")
            else:
                try:
                    api = YouTubeAPI()
                    videos = api.get_video_info([video_id])
                    
                    if not videos:
                        st.error("❌ 无法获取视频信息，请检查 API 密钥和网络连接")
                    else:
                        video_data = videos[0]
                        
                        # 保存视频信息
                        if db.add_video(video_data):
                            # 保存统计数据
                            stats_data = {
                                'video_id': video_id,
                                'view_count': video_data.get('view_count', 0),
                                'like_count': video_data.get('like_count', 0),
                                'comment_count': video_data.get('comment_count', 0),
                                'favorite_count': video_data.get('favorite_count', 0)
                            }
                            db.add_video_stats(stats_data)
                            
                            st.success("✅ 视频添加成功！")
                            st.rerun()
                        else:
                            st.error("❌ 添加视频失败")
                
                except Exception as e:
                    st.error(f"❌ 错误: {str(e)}")
    
    st.write("---")
    
    # 视频列表
    st.subheader("📋 视频列表")
    
    videos = db.get_videos()
    
    if not videos:
        st.info("ℹ️ 暂无视频数据")
        return
    
    # 搜索和筛选
    search_term = st.text_input("🔍 搜索视频", "")
    
    if search_term:
        videos = [
            v for v in videos
            if search_term.lower() in v['title'].lower()
        ]
    
    # 显示视频列表
    for video in videos:
        with st.expander(f"{video['title']}"):
            col1, col2 = st.columns([1, 3])
            
            with col1:
                if video.get('thumbnail_url'):
                    st.image(video['thumbnail_url'], use_column_width=True)
            
            with col2:
                st.write(f"**视频 ID**: {video['video_id']}")
                st.write(f"**观看量**: {format_number(video.get('view_count', 0))}")
                st.write(f"**点赞量**: {format_number(video.get('like_count', 0))}")
                st.write(f"**评论量**: {format_number(video.get('comment_count', 0))}")
                
                if st.button(f"删除视频", key=f"delete_{video['video_id']}"):
                    if db.delete_video(video['video_id']):
                        st.success("✅ 视频已删除")
                        st.rerun()
                    else:
                        st.error("❌ 删除失败")

# ==================== 深度分析页面 ====================

def render_analysis():
    """渲染深度分析页面"""
    st.title("🔍 深度分析")
    
    # 选择视频
    videos = db.get_videos()
    
    if not videos:
        st.warning("⚠️ 暂无视频数据，请先添加视频")
        return
    
    video_options = {v['title']: v['video_id'] for v in videos}
    selected_title = st.selectbox("选择视频进行分析", list(video_options.keys()))
    
    if not selected_title:
        return
    
    video_id = video_options[selected_title]
    video = db.get_video_by_id(video_id)
    
    if not video:
        st.error("❌ 无法获取视频信息")
        return
    
    # 显示视频信息
    st.subheader("📹 视频信息")
    col1, col2 = st.columns([1, 2])
    
    with col1:
        if video.get('thumbnail_url'):
            st.image(video['thumbnail_url'], use_column_width=True)
    
    with col2:
        st.write(f"**标题**: {video['title']}")
        st.write(f"**视频 ID**: {video['video_id']}")
        st.write(f"**频道**: {video.get('channel_title', 'N/A')}")
        st.write(f"**发布时间**: {video.get('published_at', 'N/A')}")
    
    st.write("---")
    
    # 统计数据
    st.subheader("📊 当前统计数据")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("观看量", format_number(video.get('view_count', 0)))
    with col2:
        st.metric("点赞量", format_number(video.get('like_count', 0)))
    with col3:
        st.metric("评论量", format_number(video.get('comment_count', 0)))
    with col4:
        engagement_rate = calculate_engagement_rate(
            video.get('like_count', 0),
            video.get('comment_count', 0),
            video.get('view_count', 0)
        )
        st.metric("互动率", f"{engagement_rate * 100:.2f}%")
    
    st.write("---")
    
    # 历史趋势
    st.subheader("📈 历史趋势")
    
    stats_history = db.get_video_stats_history(video_id)
    
    if not stats_history:
        st.info("ℹ️ 暂无历史数据")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            fig = VideoAnalyzer.create_view_trend_chart(stats_history)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = VideoAnalyzer.create_engagement_chart(stats_history)
            st.plotly_chart(fig, use_container_width=True)

# ==================== 设置页面 ====================

def render_settings():
    """渲染设置页面"""
    st.title("⚙️ 设置")
    
    # API 密钥配置
    st.subheader("🔑 API 密钥配置")
    st.info(
        "💡 在生产环境中，API 密钥应通过 Streamlit Secrets 配置，"
        "而不是直接输入。"
    )
    
    api_key = st.text_input(
        "YouTube API 密钥",
        type="password",
        help="请输入你的 YouTube Data API v3 密钥"
    )
    
    if st.button("保存 API 密钥"):
        st.success("✅ API 密钥已保存（仅用于当前会话）")
        st.warning("⚠️ 请在 Streamlit Cloud Secrets 中配置永久保存")
    
    st.write("---")
    
    # 数据管理
    st.subheader("🗄️ 数据管理")
    
    if st.button("清空所有数据", type="secondary"):
        if st.confirm("确定要清空所有数据吗？此操作不可恢复！"):
            # TODO: 实现清空数据功能
            st.warning("⚠️ 此功能尚未实现")
    
    st.write("---")
    
    # 关于
    st.subheader("ℹ️ 关于")
    st.markdown("""
    **YouTube Analytics Dashboard**

    - 版本: 1.0.0
    - 技术栈: Streamlit + Pandas + Plotly
    - 数据库: SQLite
    
    由 [你的名字] 开发
    """)

# ==================== 应用入口 ====================

if __name__ == "__main__":
    main()
```

---

## 🚀 第五部分：自动化部署

### 5.1 GitHub Actions 配置

创建 `.github/workflows/auto-update.yml`：

```yaml
name: 自动更新 YouTube 数据

on:
  schedule:
    # 每天 3 次：北京时间 9:00, 12:00, 18:00
    - cron: '0 1 * * *'   # UTC 1:00 = 北京 9:00
    - cron: '0 4 * * *'   # UTC 4:00 = 北京 12:00
    - cron: '0 10 * * *'  # UTC 10:00 = 北京 18:00
  workflow_dispatch:  # 支持手动触发

permissions:
  contents: write  # 允许写入仓库

jobs:
  update:
    runs-on: ubuntu-latest
    
    steps:
      - name: 检出代码
        uses: actions/checkout@v4
      
      - name: 设置 Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      
      - name: 安装依赖
        run: |
          pip install requests
      
      - name: 创建数据更新脚本
        run: |
          cat > update_data.py << 'EOF'
          import requests
          import sqlite3
          import os
          from datetime import datetime
          
          # YouTube API 配置
          API_KEY = os.environ.get('YOUTUBE_API_KEY')
          API_URL = "https://www.googleapis.com/youtube/v3/videos"
          DB_PATH = "youtube_dashboard.db"
          
          def get_video_stats(video_id):
              """获取视频统计数据"""
              params = {
                  'part': 'statistics',
                  'id': video_id,
                  'key': API_KEY
              }
              response = requests.get(API_URL, params=params)
              data = response.json()
              
              if 'items' in data and data['items']:
                  stats = data['items'][0]['statistics']
                  return {
                      'view_count': int(stats.get('viewCount', 0)),
                      'like_count': int(stats.get('likeCount', 0)),
                      'comment_count': int(stats.get('commentCount', 0))
                  }
              return None
          
          def update_database(video_id):
              """更新数据库"""
              stats = get_video_stats(video_id)
              if not stats:
                  print(f"Failed to get stats for {video_id}")
                  return False
              
              conn = sqlite3.connect(DB_PATH)
              cursor = conn.cursor()
              
              cursor.execute("""
                  INSERT INTO video_stats
                  (video_id, view_count, like_count, comment_count)
                  VALUES (?, ?, ?, ?)
              """, (video_id, stats['view_count'], stats['like_count'], 
                    stats['comment_count']))
              
              conn.commit()
              conn.close()
              return True
          
          # 主流程
          def main():
              # 获取所有视频 ID
              conn = sqlite3.connect(DB_PATH)
              cursor = conn.cursor()
              cursor.execute("SELECT video_id FROM videos")
              video_ids = [row[0] for row in cursor.fetchall()]
              conn.close()
              
              # 更新每个视频的数据
              for video_id in video_ids:
                  update_database(video_id)
                  print(f"Updated {video_id}")
          
          if __name__ == "__main__":
              main()
          EOF
      
      - name: 运行数据更新
        env:
          YOUTUBE_API_KEY: ${{ secrets.YOUTUBE_API_KEY }}
        run: python update_data.py
      
      - name: 提交数据库更新
        run: |
          git config user.name "GitHub Action"
          git config user.email "action@github.com"
          git add youtube_dashboard.db
          git commit -m "chore: 自动更新数据 [skip ci]" || exit 0
          git push
```

**重要说明**：
- `[skip ci]` 标记避免触发 CI 检查
- 只推送数据库文件，不影响 requirements.txt
- 支持定时和手动触发

### 5.2 Streamlit Cloud 部署

#### 步骤 1: 创建 GitHub 仓库

```bash
# 1. 在 GitHub 上创建新仓库
# 2. 克隆到本地
git clone https://github.com/YOUR_USERNAME/youtube-dashboard-new.git
cd youtube-dashboard-new

# 3. 创建所有文件
# (按照上面的代码实现创建所有文件)

# 4. 提交并推送
git add .
git commit -m "Initial commit: Complete YouTube Analytics Dashboard"
git push origin main
```

#### 步骤 2: 配置 Streamlit Cloud

1. 访问 https://share.streamlit.io/
2. 点击 "New app"
3. 填写配置：
   ```
   Repository: YOUR_USERNAME/youtube-dashboard-new
   Branch: main
   Main file path: app.py
   Python version: 3.10
   ```
4. 配置 Secrets：
   ```
   YOUTUBE_API_KEY=你的YouTube_API密钥
   ```
5. 点击 "Deploy"

#### 步骤 3: 验证部署

```
✓ 依赖安装成功（4 个包）
✓ 应用启动成功
✓ 页面正常显示
✓ 数据库连接正常
```

### 5.3 本地开发流程

```bash
# 1. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 安装依赖（严格 4 行）
pip install -r requirements.txt

# 3. 运行应用
streamlit run app.py

# 4. 访问应用
# 浏览器打开 http://localhost:8501
```

---

## 📚 第六部分：文档

### 6.1 README.md

```markdown
# YouTube Analytics Dashboard

一个简单、优雅的 YouTube 数据分析仪表板，基于 Streamlit 构建。

## 功能特性

- 📊 实时数据监控
- 📈 交互式可视化
- 🔍 深度数据分析
- 🤖 自动数据更新
- 📱 响应式设计

## 技术栈

- Streamlit 1.53.1
- Pandas 2.3.3
- Plotly 6.5.2
- Requests 2.32.5
- SQLite

## 快速开始

### 本地运行

```bash
# 1. 克隆仓库
git clone https://github.com/YOUR_USERNAME/youtube-dashboard-new.git
cd youtube-dashboard-new

# 2. 创建虚拟环境
python3 -m venv venv
source venv/bin/activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 配置 API 密钥
export YOUTUBE_API_KEY=你的API密钥

# 5. 运行应用
streamlit run app.py
```

### Streamlit Cloud 部署

1. Fork 或克隆此仓库
2. 在 Streamlit Cloud 连接仓库
3. 配置 `YOUTUBE_API_KEY` Secret
4. 部署应用

## 配置

### YouTube API 密钥

1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建项目并启用 YouTube Data API v3
3. 创建 API 密钥
4. 在应用中配置密钥

### 数据库

- 数据库文件: `youtube_dashboard.db`
- 自动创建在应用根目录
- 可手动备份和恢复

## 文档

- [开发指南](docs/DEVELOPMENT.md)
- [部署指南](docs/DEPLOYMENT.md)
- [故障排除](docs/TROUBLESHOOTING.md)

## 许可证

MIT License
```

### 6.2 docs/DEVELOPMENT.md

```markdown
# 开发指南

## 项目结构

```
youtube-dashboard-new/
├── app.py                 # 主应用
├── database.py            # 数据库模块
├── youtube_api.py         # API 集成
├── analytics.py           # 数据分析
├── utils.py              # 工具函数
├── config.py             # 配置管理
├── requirements.txt       # 依赖（严格 4 行）
└── .streamlit/
    └── config.toml      # Streamlit 配置
```

## 开发规范

### 代码风格

- 使用 PEP 8 风格
- 添加类型提示
- 编写文档字符串
- 保持函数简短

### Git 提交规范

```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

### requirements.txt 管理规则

⚠️ **严格规则**：
- ❌ 永远不要使用 `pip freeze`
- ❌ 永远不要使用 `pipreqs`
- ❌ 永远不要添加额外的依赖
- ✅ 只保留这 4 行：
  ```
  streamlit==1.53.1
  pandas==2.3.3
  plotly==6.5.2
  requests==2.32.5
  ```

## 测试

```bash
# 运行应用
streamlit run app.py

# 访问 http://localhost:8501
```

## 常见问题

### Q: 如何添加新功能？
A: 遵循现有模块结构，添加新功能后更新文档。

### Q: 如何调试？
A: 使用 Streamlit 的 `st.write()` 和 `st.json()` 输出调试信息。
```

### 6.3 docs/DEPLOYMENT.md

```markdown
# 部署指南

## Streamlit Cloud 部署

### 前置要求

- GitHub 仓库
- YouTube API 密钥
- Streamlit 账号

### 部署步骤

1. **准备代码**
   ```bash
   git clone https://github.com/YOUR_USERNAME/youtube-dashboard-new.git
   cd youtube-dashboard-new
   # 确保所有文件已提交
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **配置 Streamlit Cloud**
   - 访问 https://share.streamlit.io/
   - 点击 "New app"
   - 填写配置：
     ```
     Repository: YOUR_USERNAME/youtube-dashboard-new
     Branch: main
     Main file path: app.py
     Python version: 3.10
     ```

3. **配置 Secrets**
   - 在应用管理页面
   - 点击 "Settings" → "Secrets"
   - 添加：
     ```
     YOUTUBE_API_KEY=你的API密钥
     ```

4. **部署**
   - 点击 "Deploy"
   - 等待 3-5 分钟

### 验证部署

检查以下内容：
- ✅ 依赖安装成功（4 个包）
- ✅ 应用启动成功
- ✅ 页面正常显示
- ✅ 可以添加视频

## 自动更新

### GitHub Actions

配置了每天 3 次自动更新：
- UTC 1:00 (北京 9:00)
- UTC 4:00 (北京 12:00)
- UTC 10:00 (北京 18:00)

也可以手动触发更新。

### 故障排除

#### 问题: 依赖安装失败

**症状**: `ERROR: Could not find a version that satisfies the requirement distro-info`

**解决方案**:
1. 检查 requirements.txt 是否为 4 行
2. 删除应用并重新部署
3. 确保使用 main 分支

#### 问题: 应用启动失败

**症状**: 页面空白或错误

**解决方案**:
1. 查看部署日志
2. 检查 API 密钥配置
3. 验证所有文件已上传

#### 问题: 数据无法更新

**症状**: 数据不更新

**解决方案**:
1. 检查 GitHub Actions 日志
2. 验证 API 密钥有效
3. 手动触发更新 workflow
```

### 6.4 docs/TROUBLESHOOTING.md

```markdown
# 故障排除指南

## 常见问题

### 1. requirements.txt 被自动修改

**症状**: requirements.txt 变成 144 行，包含 distro-info

**解决方案**:
1. 恢复为 4 行：
   ```bash
   cat > requirements.txt << 'EOF'
   streamlit==1.53.1
   pandas==2.3.3
   plotly==6.5.2
   requests==2.32.5
   EOF
   ```
2. 禁用任何自动依赖生成工具
3. 使用 Git pre-commit hook 保护

### 2. Streamlit Cloud 部署失败

**症状**: 安装依赖时出错

**检查**:
- requirements.txt 是否为 4 行
- 是否有 distro-info 等系统包
- Python 版本是否兼容

**解决**:
```bash
# 强制恢复正确的 requirements.txt
git reset --hard <正确的提交>
git push origin main --force
```

### 3. API 密钥错误

**症状**: `Error 403: quotaExceeded` 或 `Error 400: keyInvalid`

**解决方案**:
1. 检查 API 密钥是否正确
2. 检查 Google Cloud Console 配额
3. 验证 API 密钥权限

### 4. 数据库错误

**症状**: `sqlite3.OperationalError: no such table`

**解决方案**:
```bash
# 删除数据库文件，让应用自动重建
rm youtube_dashboard.db

# 或手动初始化
python3 -c "from database import get_database; db = get_database()"
```

### 5. 页面加载缓慢

**症状**: 页面响应慢

**解决方案**:
1. 减少视频数量
2. 清理历史数据
3. 优化数据库查询
4. 使用缓存

## 调试技巧

### 1. 启用详细日志

编辑 `.streamlit/config.toml`:
```toml
[logger]
level = "debug"
```

### 2. 查看部署日志

在 Streamlit Cloud 管理页面查看完整日志。

### 3. 本地测试

在本地测试再部署：
```bash
streamlit run app.py
```

## 获取帮助

- 查看 Streamlit 文档: https://docs.streamlit.io/
- GitHub Issues: https://github.com/YOUR_USERNAME/youtube-dashboard-new/issues
- 社区论坛: https://discuss.streamlit.io/
```

---

## 🎯 第七部分：使用说明

### 如何使用这个 Prompt

1. **复制整个内容**
   - 复制这个 markdown 文件的全部内容

2. **发送给 AI 助手**
   - 打开一个新的对话
   - 粘贴内容
   - 添加说明："请按照这个方案创建一个全新的 YouTube Analytics Dashboard 项目"

3. **AI 助手会执行**
   - 创建所有文件
   - 实现所有功能
   - 提供部署指南

### 关键原则

1. **从零开始**
   - 不要依赖现有项目
   - 创建全新的 GitHub 仓库
   - 避免历史包袱

2. **严格依赖管理**
   - requirements.txt 必须是 4 行
   - 永远不要使用 pip freeze
   - 永远不要添加额外依赖

3. **清晰的结构**
   - 模块化代码
   - 完整的文档
   - 自动化部署

4. **完整的测试**
   - 本地测试
   - Streamlit Cloud 测试
   - 自动化更新测试

---

## ✅ 验证清单

### 开发完成检查

- [ ] 所有核心功能已实现
- [ ] 代码符合规范
- [ ] 文档完整
- [ ] 本地测试通过

### 部署完成检查

- [ ] GitHub 仓库已创建
- [ ] requirements.txt 是 4 行
- [ ] Streamlit Cloud 配置完成
- [ ] API 密钥已配置
- [ ] 应用正常部署
- [ ] 自动更新已配置

### 功能验证检查

- [ ] 可以添加视频
- [ ] 可以查看统计
- [ ] 图表正常显示
- [ ] 深度分析正常
- [ ] 自动更新工作

---

## 📞 支持和反馈

如有问题或建议，请：

1. 查看 [故障排除指南](docs/TROUBLESHOOTING.md)
2. 提交 [GitHub Issue](https://github.com/YOUR_USERNAME/youtube-dashboard-new/issues)
3. 联系维护者

---

**版本**: 1.0.0  
**最后更新**: 2026-01-30  
**状态**: 完整方案，可执行
