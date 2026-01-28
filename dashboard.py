#!/usr/bin/env python3
"""
YouTube Dashboard - Streamlit 可视化看板
你的唯一操作入口
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import re
from datetime import datetime, timedelta
from pathlib import Path
from collections import Counter
import os

# 配置页面
st.set_page_config(
    page_title="YouTube 数据监控看板",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义 CSS
st.markdown("""
<style>
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 20px;
        border-radius: 10px;
        color: white;
        margin: 10px 0;
    }
    .success-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
    .alert-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)


# ==================== 数据库操作函数 ====================

def get_connection():
    """获取数据库连接"""
    db_path = Path('youtube_dashboard.db')
    
    # 如果数据库不存在，初始化
    if not db_path.exists():
        init_database()
    
    conn = sqlite3.connect('youtube_dashboard.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_database():
    """初始化数据库"""
    conn = sqlite3.connect('youtube_dashboard.db')
    cursor = conn.cursor()
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            title TEXT,
            channel_title TEXT,
            added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS video_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            date DATE,
            view_count INTEGER DEFAULT 0,
            like_count INTEGER DEFAULT 0,
            comment_count INTEGER DEFAULT 0,
            engagement_rate REAL DEFAULT 0,
            fetch_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos(video_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS video_comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            comment_text TEXT,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos(video_id)
        )
    ''')
    
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT,
            alert_type TEXT,
            current_value INTEGER,
            message TEXT,
            sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos(video_id)
        )
    ''')
    
    conn.commit()
    conn.close()


def extract_video_id(url_or_id):
    """从 URL 或 ID 中提取 video_id"""
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id

    patterns = [
        r'(?:v=|/)([0-9A-Za-z_-]{11}).*',
        r'(?:embed/)([0-9A-Za-z_-]{11})',
        r'(?:v/)([0-9A-Za-z_-]{11})',
        r'(?:youtu\.be/)([0-9A-Za-z_-]{11})'
    ]

    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)

    return None


def get_all_videos(conn):
    """获取所有监控的视频"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT video_id, title, channel_title, added_at, is_active
        FROM videos
        ORDER BY added_at DESC
    ''')
    return cursor.fetchall()


def add_videos(conn, video_urls):
    """批量添加视频"""
    cursor = conn.cursor()
    added_count = 0

    for url in video_urls:
        url = url.strip()
        if not url:
            continue

        video_id = extract_video_id(url)
        if not video_id:
            continue

        try:
            cursor.execute('''
                INSERT OR IGNORE INTO videos (video_id, title, channel_title)
                VALUES (?, ?, ?)
            ''', (video_id, '待更新', ''))
            if cursor.rowcount > 0:
                added_count += 1
        except Exception as e:
            st.error(f"添加失败 {url}: {e}")

    conn.commit()
    return added_count


def get_overall_stats(conn):
    """获取整体统计数据"""
    cursor = conn.cursor()

    # 获取所有视频的最新数据
    cursor.execute('''
        WITH latest_stats AS (
            SELECT video_id,
                   MAX(date) as latest_date
            FROM video_stats
            GROUP BY video_id
        )
        SELECT
            COUNT(DISTINCT vs.video_id) as total_videos,
            SUM(vs.view_count) as total_views,
            AVG(vs.engagement_rate) as avg_engagement_rate,
            SUM(vs.like_count) as total_likes,
            SUM(vs.comment_count) as total_comments
        FROM video_stats vs
        JOIN latest_stats ls ON vs.video_id = ls.video_id AND vs.date = ls.latest_date
        JOIN videos v ON v.video_id = vs.video_id AND v.is_active = 1
    ''')

    return cursor.fetchone()


def get_daily_overall_trend(conn, days=30):
    """获取每日整体趋势"""
    cursor = conn.cursor()

    query = f'''
        SELECT
            date,
            SUM(view_count) as total_views,
            AVG(engagement_rate) as avg_engagement_rate,
            COUNT(DISTINCT video_id) as video_count
        FROM video_stats
        WHERE date >= date('now', '-{days} days')
        GROUP BY date
        ORDER BY date
    '''

    df = pd.read_sql_query(query, conn)
    return df


def get_video_stats(conn, video_id):
    """获取单个视频的数据"""
    cursor = conn.cursor()

    cursor.execute('''
        SELECT * FROM videos WHERE video_id = ?
    ''', (video_id,))
    video_info = cursor.fetchone()

    cursor.execute('''
        SELECT * FROM video_stats
        WHERE video_id = ?
        ORDER BY date DESC
        LIMIT 30
    ''', (video_id,))
    stats = cursor.fetchall()

    return video_info, stats


def get_video_comments(conn, video_id, limit=100):
    """从数据库获取视频评论"""
    cursor = conn.cursor()
    cursor.execute('''
        SELECT comment_text FROM video_comments
        WHERE video_id = ?
        ORDER BY fetched_at DESC
        LIMIT ?
    ''', (video_id, limit))

    comments = [row['comment_text'] for row in cursor.fetchall()]
    return comments


def get_alerts(conn, days=7):
    """获取预警记录"""
    cursor = conn.cursor()

    query = f'''
        SELECT * FROM alerts
        WHERE sent_at >= datetime('now', '-{days} days')
        ORDER BY sent_at DESC
        LIMIT 50
    '''

    df = pd.read_sql_query(query, conn)
    return df


def generate_word_cloud(comments):
    """生成词云数据"""
    if not comments:
        return None

    # 简单的中文分词（按空格和标点符号分割）
    import re

    all_words = []
    for comment in comments:
        # 提取中文和英文单词
        words = re.findall(r'[\u4e00-\u9fa5]+|[a-zA-Z]+', comment)
        all_words.extend(words)

    if not all_words:
        return None

    # 统计词频
    word_counts = Counter(all_words)

    # 过滤掉常见词
    stop_words = {'的', '了', '是', '在', '我', '有', '和', '就', '不', '人', '都', '一', '一个', '上', '也', '很', '到', '说', '要', '去', '你', '会', '着', '没有', '看', '好', '自己', '这'}
    word_counts = {k: v for k, v in word_counts.items() if len(k) > 1 and k not in stop_words}

    # 取前 50 个高频词
    top_words = word_counts.most_common(50)

    return top_words


# ==================== 页面渲染函数 ====================

def render_video_management(conn):
    """渲染视频管理页面"""
    st.header("📹 视频管理")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("添加新视频")
        st.markdown("""
        <div class="success-box">
            💡 <b>提示：</b>每行输入一个 YouTube 视频地址，支持完整 URL 或直接输入 video_id
        </div>
        """, unsafe_allow_html=True)

        video_urls = st.text_area(
            "视频地址列表",
            height=200,
            placeholder="https://www.youtube.com/watch?v=xxx\nhttps://www.youtube.com/watch?v=yyy"
        )

        col_btn1 = st.columns(1)[0]

        with col_btn1:
            if st.button("➕ 添加视频", type="primary"):
                if video_urls:
                    urls = [u.strip() for u in video_urls.split('\n') if u.strip()]
                    count = add_videos(conn, urls)
                    if count > 0:
                        st.success(f"✅ 成功添加 {count} 个视频！")
                        st.rerun()
                    else:
                        st.warning("⚠️ 没有添加新视频（可能已存在或格式错误）")
                else:
                    st.warning("⚠️ 请输入视频地址")

    with col2:
        st.subheader("操作指南")
        st.markdown("""
        **添加视频步骤：**
        1. ✅ 在左侧输入框粘贴视频地址（每行一个）
        2. ✅ 点击"添加视频"按钮
        3. ✅ 查看下方的视频列表
        4. ✅ 定时脚本会自动获取数据

        **更新数据步骤：**
        1. ✅ 访问 GitHub Actions 页面手动触发
        2. ✅ 等待 1-3 分钟数据获取完成
        3. ✅ 刷新本页面查看更新后的数据
        4. ✅ 或者等待每日自动更新（9:00, 12:00, 18:00）

        **支持格式：**
        - `https://www.youtube.com/watch?v=xxx`
        - `https://youtu.be/xxx`
        - 直接输入 `xxx`（11位ID）
        """)

    st.divider()

    st.subheader("📋 监控视频列表")

    videos = get_all_videos(conn)

    if not videos:
        st.info("📭 暂无监控视频，请添加视频地址")
        return

    # 视频列表
    video_data = []
    for v in videos:
        video_data.append({
            'Video ID': v['video_id'],
            '标题': v['title'] or '待更新',
            '频道': v['channel_title'] or '-',
            '添加时间': v['added_at'],
            '状态': '✅ 活跃' if v['is_active'] else '❌ 停用'
        })

    df_videos = pd.DataFrame(video_data)

    # 显示表格
    st.dataframe(
        df_videos,
        use_container_width=True,
        column_config={
            'Video ID': st.column_config.TextColumn('Video ID', width='small'),
            '标题': st.column_config.TextColumn('标题'),
            '频道': st.column_config.TextColumn('频道', width='medium'),
            '添加时间': st.column_config.DatetimeColumn('添加时间', format='YYYY-MM-DD HH:mm'),
            '状态': st.column_config.TextColumn('状态', width='small')
        }
    )

    st.markdown(f"📊 共有 **{len(videos)}** 个视频正在监控")


def render_overall_dashboard(conn):
    """渲染整体数据看板"""
    st.header("📊 整体数据看板")

    # 获取统计数据
    stats = get_overall_stats(conn)

    if not stats or stats['total_videos'] == 0:
        st.warning("⚠️ 暂无数据，请先添加视频并等待定时脚本更新数据")
        return

    # KPI 卡片
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="📹 监控视频数",
            value=f"{stats['total_videos']:,}"
        )

    with col2:
        st.metric(
            label="👀 总播放量",
            value=f"{stats['total_views']:,}",
            delta="累计"
        )

    with col3:
        st.metric(
            label="💖 总点赞数",
            value=f"{stats['total_likes']:,}"
        )

    with col4:
        st.metric(
            label="💬 总评论数",
            value=f"{stats['total_comments']:,}"
        )

    st.divider()

    # 趋势图
    trend_df = get_daily_overall_trend(conn, days=30)

    if trend_df.empty:
        st.warning("⚠️ 暂无历史数据")
        return

    # 播放量趋势
    fig_views = px.line(
        trend_df,
        x='date',
        y='total_views',
        title='📈 总播放量趋势（近30天）',
        markers=True,
        template='plotly_white'
    )
    fig_views.update_layout(
        xaxis_title='日期',
        yaxis_title='播放量',
        hovermode='x unified'
    )
    st.plotly_chart(fig_views, use_container_width=True)

    # 互动率趋势
    col1, col2 = st.columns(2)

    with col1:
        fig_engagement = px.line(
            trend_df,
            x='date',
            y='avg_engagement_rate',
            title='📊 平均互动率变化（近30天）',
            markers=True,
            template='plotly_white'
        )
        fig_engagement.update_layout(
            xaxis_title='日期',
            yaxis_title='互动率 (%)',
            hovermode='x unified'
        )
        st.plotly_chart(fig_engagement, use_container_width=True)

    with col2:
        fig_count = px.bar(
            trend_df,
            x='date',
            y='video_count',
            title='📹 监控视频数量变化',
            template='plotly_white'
        )
        fig_count.update_layout(
            xaxis_title='日期',
            yaxis_title='视频数量'
        )
        st.plotly_chart(fig_count, use_container_width=True)


def render_video_detail_dashboard(conn):
    """渲染单个视频看板"""
    st.header("📹 单个视频看板")

    # 获取所有视频
    videos = get_all_videos(conn)

    if not videos:
        st.warning("⚠️ 暂无监控视频")
        return

    # 视频选择
    video_options = {f"{v['title'] or '待更新'} ({v['video_id']})": v['video_id'] for v in videos}
    selected_option = st.selectbox("选择视频", list(video_options.keys()))
    video_id = video_options[selected_option]

    # 获取视频数据
    video_info, stats = get_video_stats(conn, video_id)

    if not stats:
        st.warning(f"⚠️ 视频 {video_id} 暂无数据")
        return

    # 视频信息
    st.subheader(f"📺 {video_info['title']}")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"**频道**: {video_info['channel_title'] or '待更新'}")

    with col2:
        st.info(f"**添加时间**: {video_info['added_at']}")

    with col3:
        st.info(f"**数据记录**: {len(stats)} 条")

    # 最新数据 KPI
    latest = stats[0]
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="👀 播放量",
            value=f"{latest['view_count']:,}"
        )

    with col2:
        st.metric(
            label="💖 点赞数",
            value=f"{latest['like_count']:,}"
        )

    with col3:
        st.metric(
            label="💬 评论数",
            value=f"{latest['comment_count']:,}"
        )

    with col4:
        st.metric(
            label="📊 互动率",
            value=f"{latest['engagement_rate']:.2f}%"
        )

    st.divider()

    # 转换为 DataFrame
    df_stats = pd.DataFrame(stats)

    # 播放量趋势
    fig_views = px.line(
        df_stats.sort_values('date'),
        x='date',
        y='view_count',
        title='📈 播放量趋势',
        markers=True,
        template='plotly_white'
    )
    fig_views.update_layout(
        xaxis_title='日期',
        yaxis_title='播放量',
        hovermode='x unified'
    )
    st.plotly_chart(fig_views, use_container_width=True)

    # 互动数据
    col1, col2 = st.columns(2)

    with col1:
        fig_interactions = go.Figure()
        fig_interactions.add_trace(go.Scatter(
            x=df_stats['date'],
            y=df_stats['like_count'],
            mode='lines+markers',
            name='点赞数',
            line=dict(color='#FF6B6B')
        ))
        fig_interactions.add_trace(go.Scatter(
            x=df_stats['date'],
            y=df_stats['comment_count'],
            mode='lines+markers',
            name='评论数',
            line=dict(color='#4ECDC4')
        ))
        fig_interactions.update_layout(
            title='💖 互动数据趋势',
            xaxis_title='日期',
            yaxis_title='数量',
            template='plotly_white',
            hovermode='x unified'
        )
        st.plotly_chart(fig_interactions, use_container_width=True)

    with col2:
        fig_rates = go.Figure()
        fig_rates.add_trace(go.Bar(
            x=df_stats['date'],
            y=df_stats['engagement_rate'],
            name='互动率',
            marker_color='#95E1D3'
        ))
        fig_rates.update_layout(
            title='📊 互动率变化',
            xaxis_title='日期',
            yaxis_title='互动率 (%)',
            template='plotly_white'
        )
        st.plotly_chart(fig_rates, use_container_width=True)

    # 评论词云
    st.divider()
    st.subheader("💬 评论词云")

    # 获取评论
    comments = get_video_comments(conn, video_id)

    if comments:
        # 生成词云数据
        word_cloud_data = generate_word_cloud(comments)

        if word_cloud_data:
            # 转换为 DataFrame
            df_words = pd.DataFrame(word_cloud_data, columns=['词语', '频次'])

            # 显示词频表格
            col1, col2 = st.columns([1, 2])

            with col1:
                st.markdown("#### 高频词语")
                st.dataframe(
                    df_words.head(20),
                    use_container_width=True,
                    hide_index=True
                )

            with col2:
                # 使用柱状图显示词频
                fig_words = px.bar(
                    df_words.head(20),
                    x='频次',
                    y='词语',
                    orientation='h',
                    title='📊 高频词语 Top 20',
                    template='plotly_white',
                    color='频次',
                    color_continuous_scale='Blues'
                )
                fig_words.update_layout(
                    yaxis={'categoryorder': 'total ascending'},
                    height=500
                )
                st.plotly_chart(fig_words, use_container_width=True)
        else:
            st.info("📭 暂无足够的评论生成词云")
    else:
        st.info("📭 暂无评论数据，请等待数据更新")

    # 数据表格
    st.divider()
    st.subheader("📋 历史数据明细")

    df_display = df_stats[[
        'date', 'view_count', 'like_count', 'comment_count',
        'engagement_rate', 'fetch_time'
    ]].copy()

    df_display.columns = ['日期', '播放量', '点赞数', '评论数', '互动率', '更新时间']
    df_display = df_display.sort_values('日期', ascending=False)

    st.dataframe(
        df_display,
        use_container_width=True,
        column_config={
            '日期': st.column_config.DateColumn('日期'),
            '播放量': st.column_config.NumberColumn('播放量', format='%d'),
            '点赞数': st.column_config.NumberColumn('点赞数', format='%d'),
            '评论数': st.column_config.NumberColumn('评论数', format='%d'),
            '互动率': st.column_config.NumberColumn('互动率', format='%.2f'),
            '更新时间': st.column_config.DatetimeColumn('更新时间', format='YYYY-MM-DD HH:mm')
        }
    )


def render_alerts_dashboard(conn):
    """渲染预警看板"""
    st.header("🔥 爆款提醒记录")

    # 预警统计
    cursor = conn.cursor()
    cursor.execute('''
        SELECT
            alert_type,
            COUNT(*) as count,
            MAX(sent_at) as last_sent
        FROM alerts
        WHERE sent_at >= datetime('now', '-7 days')
        GROUP BY alert_type
        ORDER BY alert_type
    ''')

    alert_stats = cursor.fetchall()

    if alert_stats:
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            for stat in alert_stats:
                if '10000' in stat['alert_type']:
                    st.metric(
                        label="🔥 增长1万（7天）",
                        value=f"{stat['count']} 次"
                    )

        with col2:
            for stat in alert_stats:
                if '30000' in stat['alert_type']:
                    st.metric(
                        label="🔥 增长3万（7天）",
                        value=f"{stat['count']} 次"
                    )

        with col3:
            for stat in alert_stats:
                if '50000' in stat['alert_type']:
                    st.metric(
                        label="🔥 增长5万（7天）",
                        value=f"{stat['count']} 次"
                    )

        with col4:
            for stat in alert_stats:
                if '100k' in stat['alert_type']:
                    st.metric(
                        label="🔥 爆款10万（7天）",
                        value=f"{stat['count']} 次"
                    )

        col1, col2 = st.columns(2)

        with col1:
            for stat in alert_stats:
                if 'data_anomaly' in stat['alert_type']:
                    st.metric(
                        label="⚠️ 数据异常（7天）",
                        value=f"{stat['count']} 次"
                    )

    st.divider()

    # 预警记录
    alerts_df = get_alerts(conn, days=30)

    if alerts_df.empty:
        st.info("📭 暂无预警记录")
        return

    st.subheader(f"📋 近30天预警记录 ({len(alerts_df)} 条）")

    df_display = alerts_df[[
        'sent_at', 'title', 'alert_type', 'current_value', 'message'
    ]].copy()

    df_display.columns = ['时间', '视频标题', '预警类型', '当前播放量', '消息']
    df_display['预警类型'] = df_display['预警类型'].map({
        'growth_10000': '🔥 增长1万',
        'growth_30000': '🔥 增长3万',
        'growth_50000': '🔥 增长5万',
        '100k': '🔥 爆款10万',
        'data_anomaly': '⚠️ 数据异常'
    })

    st.dataframe(
        df_display,
        use_container_width=True,
        column_config={
            '时间': st.column_config.DatetimeColumn('时间', format='YYYY-MM-DD HH:mm'),
            '视频标题': st.column_config.TextColumn('视频标题'),
            '预警类型': st.column_config.TextColumn('预警类型'),
            '当前播放量': st.column_config.NumberColumn('当前播放量', format='%d'),
            '消息': st.column_config.TextColumn('消息')
        }
    )


# ==================== 主程序 ====================

def main():
    """主函数"""
    # 连接数据库
    conn = get_connection()

    # 侧边栏
    with st.sidebar:
        st.title("📊 YouTube Dashboard")
        st.markdown("---")

        page = st.radio(
            "选择页面",
            ["📹 视频管理", "📊 整体看板", "📹 单个视频", "🔥 爆款提醒"],
            label_visibility="collapsed"
        )

        st.markdown("---")
        st.markdown("""
        **使用说明：**
        1. 在"视频管理"添加视频地址
        2. 添加后访问 GitHub Actions 手动触发更新
        3. 查看"整体看板"和"单个视频"
        4. 关注"爆款提醒"通知
        """)

    # 根据选择渲染页面
    if page == "📹 视频管理":
        render_video_management(conn)
    elif page == "📊 整体看板":
        render_overall_dashboard(conn)
    elif page == "📹 单个视频":
        render_video_detail_dashboard(conn)
    elif page == "🔥 爆款提醒":
        render_alerts_dashboard(conn)

    # 关闭连接
    conn.close()


if __name__ == '__main__':
    main()
