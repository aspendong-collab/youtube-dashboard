#!/usr/bin/env python3
"""
YouTube Analytics Dashboard - 优化版本
融合 Adjust + Apple 设计风格
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import os

# 导入自定义模块
from ui import (
    render_sidebar,
    get_current_page,
    set_current_page,
    render_metric_card,
    render_info_box,
    render_warning_box,
    render_success_box,
    render_chart_container,
    render_section_title,
    render_empty_state,
    render_separator,
)
from database import (
    init_database,
    get_videos,
    get_video_info,
    get_latest_stats,
    get_video_stats_history,
    get_comments,
    get_all_tags,
    get_unread_alerts,
    mark_alert_as_read,
    add_video,
    save_video_stats,
    save_comment,
    save_tags,
)
from api import YouTubeAPI, extract_video_id
from analytics import (
    analyze_video_performance,
    create_performance_chart,
    create_comparison_chart,
    generate_optimization_suggestions,
    generate_word_cloud,
    analyze_comment_sentiment,
    get_top_commenters,
    get_most_liked_comments,
)
from utils import (
    format_number,
    format_percentage,
    calculate_engagement_rate,
    format_duration,
    parse_duration,
    get_video_age,
    truncate_text,
)
from config import Config, set_api_key

# 配置页面
st.set_page_config(
    page_title="YouTube Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 初始化数据库
init_database()

# 初始化 session state
if "api_key" not in st.session_state:
    st.session_state.api_key = Config.YOUTUBE_API_KEY
if "selected_videos" not in st.session_state:
    st.session_state.selected_videos = []


# ==================== 主应用 ====================

def main():
    """主函数"""
    
    # 渲染侧边栏
    current_page = render_sidebar()
    
    # 应用全局样式
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #16213e 100%);
        color: #ffffff;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 根据当前页面路由
    if current_page == "video_management":
        render_video_management()
    elif current_page == "overall_dashboard":
        render_overall_dashboard()
    elif current_page == "video_detail":
        render_video_detail()
    elif current_page == "alerts":
        render_alerts()
    elif current_page == "seo_analysis":
        render_seo_analysis()
    elif current_page == "duration_analysis":
        render_duration_analysis()
    elif current_page == "publish_time":
        render_publish_time_analysis()
    elif current_page == "tags_analysis":
        render_tags_analysis()
    elif current_page == "sentiment_analysis":
        render_sentiment_analysis()
    elif current_page == "user_profile":
        render_user_profile()
    elif current_page == "comment_analysis":
        render_comment_analysis()
    elif current_page == "api_settings":
        render_api_settings()
    elif current_page == "data_source":
        render_data_source()
    else:
        render_video_management()


# ==================== 视频管理页面 ====================

def render_video_management():
    """渲染视频管理页面"""
    
    st.title("📹 视频管理")
    render_section_title("添加新视频", "通过 YouTube URL 或视频 ID 添加视频到监控系统")
    
    # 输入框
    col1, col2 = st.columns([3, 1])
    
    with col1:
        video_input = st.text_input(
            "YouTube URL 或视频 ID",
            placeholder="例如: https://www.youtube.com/watch?v=dQw4w9WgXcQ 或 dQw4w9WgXcQ",
            help="支持 YouTube 视频 URL 或 11 位视频 ID"
        )
    
    with col2:
        st.write("")
        st.write("")
        add_button = st.button("添加视频", type="primary", width='stretch')
    
    # 批量添加
    st.markdown("---")
    render_section_title("批量添加视频", "支持通过文本文件批量添加多个视频")
    
    uploaded_file = st.file_uploader(
        "上传视频列表文件",
        type=["txt"],
        help="每行一个 YouTube URL 或视频 ID"
    )
    
    if uploaded_file:
        content = uploaded_file.read().decode("utf-8")
        video_lines = [line.strip() for line in content.split("\n") if line.strip()]
        
        st.write(f"检测到 {len(video_lines)} 个视频:")
        st.dataframe(pd.DataFrame({"视频列表": video_lines}))
        
        if st.button("批量添加", type="primary"):
            with st.spinner(f"正在添加 {len(video_lines)} 个视频..."):
                api = YouTubeAPI(st.session_state.api_key)
                success_count = 0
                
                for line in video_lines:
                    video_id = extract_video_id(line)
                    if video_id:
                        try:
                            # 获取视频信息
                            videos = api.get_video_info([video_id])
                            if videos:
                                video_data = videos[0]
                                
                                # 保存视频信息
                                add_video(video_data)
                                
                                # 保存统计数据
                                stats = {
                                    "view_count": video_data.get("view_count", 0),
                                    "like_count": video_data.get("like_count", 0),
                                    "comment_count": video_data.get("comment_count", 0),
                                    "favorite_count": video_data.get("favorite_count", 0)
                                }
                                save_video_stats(video_id, stats)
                                
                                # 保存标签
                                tags = video_data.get("tags", [])
                                if tags:
                                    save_tags(video_id, tags)
                                
                                success_count += 1
                        except Exception as e:
                            st.warning(f"添加视频 {video_id} 失败: {str(e)}")
                
                render_success_box("批量添加完成", f"成功添加 {success_count} 个视频，失败 {len(video_lines) - success_count} 个")
    
    # 处理单个添加
    if add_button and video_input:
        with st.spinner("正在获取视频信息..."):
            video_id = extract_video_id(video_input)
            
            if not video_id:
                render_error_box("无效的视频 URL", "请输入有效的 YouTube 视频 URL 或 11 位视频 ID")
            else:
                api = YouTubeAPI(st.session_state.api_key)
                videos = api.get_video_info([video_id])
                
                if videos:
                    video_data = videos[0]
                    
                    # 保存视频信息
                    add_video(video_data)
                    
                    # 保存统计数据
                    stats = {
                        "view_count": video_data.get("view_count", 0),
                        "like_count": video_data.get("like_count", 0),
                        "comment_count": video_data.get("comment_count", 0),
                        "favorite_count": video_data.get("favorite_count", 0)
                    }
                    save_video_stats(video_id, stats)
                    
                    # 保存标签
                    tags = video_data.get("tags", [])
                    if tags:
                        save_tags(video_id, tags)
                    
                    render_success_box("添加成功", f"已添加视频: {truncate_text(video_data['title'], 50)}")
                else:
                    render_error_box("获取失败", "无法获取视频信息，请检查 API 密钥和网络连接")
    
    # 显示已添加的视频
    render_separator("已监控视频")
    
    videos = get_videos()
    
    if not videos:
        render_empty_state("暂无监控视频，请先添加视频", icon="📹")
    else:
        # 准备数据
        video_list = []
        for video in videos:
            video_list.append({
                "视频标题": video[1],
                "频道": video[2],
                "观看量": format_number(video[4] or 0),
                "点赞量": format_number(video[5] or 0),
                "评论量": format_number(video[6] or 0),
                "发布时间": get_video_age(video[3]) if video[3] else "未知"
            })
        
        df = pd.DataFrame(video_list)
        st.dataframe(df, width='stretch', hide_index=True)


# ==================== 整体看板页面 ====================

def render_overall_dashboard():
    """渲染整体看板页面"""
    
    st.title("📊 整体数据看板")

    # 导航提示
    st.info("""
    💡 **导航提示**
    
    - 使用左侧导航栏切换页面
    - 返回主页点击"视频管理"或"整体看板"
    """, icon="🧭")
    
    st.markdown("---")
    
    videos = get_videos()
    
    if not videos:
        render_empty_state("暂无监控视频，请先添加视频", icon="📊")
        return
    
    # 计算总体数据
    total_views = sum([video[4] or 0 for video in videos])
    total_likes = sum([video[5] or 0 for video in videos])
    total_comments = sum([video[6] or 0 for video in videos])
    
    # 渲染指标卡片
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_metric_card("总观看量", format_number(total_views))
    
    with col2:
        render_metric_card("总点赞量", format_number(total_likes))
    
    with col3:
        render_metric_card("总评论量", format_number(total_comments))
    
    # 视频排行
    render_separator("热门视频排行")
    
    video_list = []
    for video in videos:
        engagement_rate = calculate_engagement_rate(
            video[5] or 0,
            video[6] or 0,
            video[4] or 0
        )
        video_list.append({
            "视频标题": video[1],
            "观看量": video[4] or 0,
            "点赞量": video[5] or 0,
            "评论量": video[6] or 0,
            "互动率": engagement_rate
        })
    
    df = pd.DataFrame(video_list)
    df_sorted = df.sort_values("观看量", ascending=False).head(10)
    
    # 创建对比图表
    col1, col2 = st.columns(2)
    
    with col1:
        fig = px.bar(
            df_sorted,
            x="观看量",
            y="视频标题",
            orientation="h",
            title="观看量 Top 10",
            color="观看量",
            color_continuous_scale="viridis"
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            height=500
        )
        render_chart_container("观看量排行", fig)
    
    with col2:
        fig = px.bar(
            df_sorted,
            x="互动率",
            y="视频标题",
            orientation="h",
            title="互动率 Top 10",
            color="互动率",
            color_continuous_scale="viridis"
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            height=500
        )
        render_chart_container("互动率排行", fig)


# ==================== 单个视频详情页面 ====================

def render_video_detail():
    """渲染单个视频详情页面"""
    
    st.title("📹 视频详情分析")

    # 导航提示
    st.info("""
    💡 **导航提示**
    
    - 使用左侧导航栏切换页面
    - 返回主页点击"视频管理"或"整体看板"
    """, icon="🧭")
    
    st.markdown("---")
    
    # 选择视频
    videos = get_videos()
    
    if not videos:
        render_empty_state("暂无监控视频，请先添加视频", icon="📹")
        return
    
    video_options = {f"{video[1]} ({video[0]})": video[0] for video in videos}
    selected_video = st.selectbox("选择视频", list(video_options.keys()))
    
    video_id = video_options[selected_video]
    
    # 获取视频信息
    video_info = get_video_info(video_id)
    if not video_info:
        render_error_box("视频信息不存在", "请先添加该视频")
        return
    
    # 获取最新统计
    latest_stats = get_latest_stats(video_id)
    
    # 渲染视频信息
    col1, col2 = st.columns([1, 2])
    
    with col1:
        # 显示视频缩略图
        thumbnail_url = video_info.get("thumbnail_url")
        if thumbnail_url:
            st.image(thumbnail_url, width="stretch")
        else:
            st.info("📹 无缩略图", icon="📹")
    
    with col2:
        st.subheader(video_info.get("title", ""))
        
        col_a, col_b, col_c, col_d = st.columns(4)
        
        with col_a:
            st.metric("观看量", format_number(latest_stats.get("view_count", 0) if latest_stats else 0))
        
        with col_b:
            st.metric("点赞量", format_number(latest_stats.get("like_count", 0) if latest_stats else 0))
        
        with col_c:
            st.metric("评论量", format_number(latest_stats.get("comment_count", 0) if latest_stats else 0))
        
        with col_d:
            # 计算互动率
            engagement_rate = calculate_engagement_rate(
                latest_stats.get("like_count", 0) if latest_stats else 0,
                latest_stats.get("comment_count", 0) if latest_stats else 0,
                latest_stats.get("view_count", 0) if latest_stats else 0
            )
            st.metric("互动率", format_percentage(engagement_rate))
    
    # 数据趋势图
    render_separator("数据趋势")
    
    fig = create_performance_chart(video_id, days=30)
    render_chart_container("过去 30 天数据趋势", fig)
    
    # 优化建议
    render_separator("优化建议")
    
    suggestions = generate_optimization_suggestions(video_id)
    
    if suggestions:
        for suggestion in suggestions:
            if suggestion["type"] == "warning":
                render_warning_box(suggestion["title"], suggestion["message"])
            elif suggestion["type"] == "info":
                render_info_box(suggestion["title"], suggestion["message"])
            elif suggestion["type"] == "success":
                render_success_box(suggestion["title"], suggestion["message"])
    else:
        render_info_box("无需优化", "当前视频表现良好，继续保持！")
    
    # 评论词云
    render_separator("评论分析")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("评论词云")
        wordcloud = generate_word_cloud(video_id)
        
        import matplotlib.pyplot as plt
        
        fig, ax = plt.subplots(figsize=(10, 5))
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis("off")
        st.pyplot(fig)
        plt.close()
    
    with col2:
        st.subheader("情感分析")
        sentiment = analyze_comment_sentiment(video_id)
        
        fig = go.Figure(data=[
            go.Bar(name="正面", x=["正面"], y=[sentiment.get("positive", 0)]),
            go.Bar(name="中性", x=["中性"], y=[sentiment.get("neutral", 0)]),
            go.Bar(name="负面", x=["负面"], y=[sentiment.get("negative", 0)])
        ])
        
        fig.update_layout(
            barmode="stack",
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff")
        )
        
        st.plotly_chart(fig, width='stretch')


# ==================== 爆款提醒页面 ====================

def render_alerts():
    """渲染爆款提醒页面"""
    
    st.title("🔥 爆款提醒")

    # 导航提示
    st.info("""
    💡 **导航提示**
    
    - 使用左侧导航栏切换页面
    - 返回主页点击"视频管理"或"整体看板"
    """, icon="🧭")
    
    st.markdown("---")
    
    alerts = get_unread_alerts()
    
    if not alerts:
        render_empty_state("暂无未读提醒", icon="🔔")
    else:
        for alert in alerts:
            with st.container():
                render_warning_box(
                    f"视频: {truncate_text(alert[8], 40)}",
                    f"{alert[3]}: 当前值 {alert[5]}, 阈值 {alert[4]}"
                )
                
                if st.button(f"标记为已读", key=f"read_{alert[0]}"):
                    mark_alert_as_read(alert[0])
                    st.rerun()
                
                st.markdown("---")


# ==================== SEO 分析页面 ====================

def render_seo_analysis():
    """渲染 SEO 分析页面"""
    
    st.title("🎯 SEO 优化分析")

    # 导航提示
    st.info("""
    💡 **导航提示**
    
    - 使用左侧导航栏切换页面
    - 返回主页点击"视频管理"或"整体看板"
    """, icon="🧭")
    
    st.markdown("---")
    
    videos = get_videos()
    
    if not videos:
        render_empty_state("暂无监控视频，请先添加视频", icon="📊")
        return
    
    # 选择视频
    video_options = {f"{video[1]} ({video[0]})": video[0] for video in videos}
    selected_video = st.selectbox("选择视频", list(video_options.keys()))
    
    video_id = video_options[selected_video]
    video_info = get_video_info(video_id)
    
    if not video_info:
        return
    
    # 标题分析
    render_section_title("标题分析")
    
    title = video_info.get("title", "")
    title_length = len(title)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("标题长度", f"{title_length} 字符")
    
    with col2:
        optimal_range = "30-60"
        status = "✅ 优秀" if 30 <= title_length <= 60 else "⚠️ 需优化" if title_length < 30 else "❌ 过长"
        st.metric("最佳范围", optimal_range)
    
    with col3:
        st.metric("状态", status)
    
    # 描述分析
    render_section_title("描述分析")
    
    description = video_info.get("description", "")
    desc_length = len(description)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("描述长度", f"{desc_length} 字符")
    
    with col2:
        optimal_range = "200-500"
        status = "✅ 优秀" if 200 <= desc_length <= 500 else "⚠️ 需优化" if desc_length < 200 else "❌ 过长"
        st.metric("最佳范围", optimal_range)
    
    with col3:
        st.metric("状态", status)
    
    # 标签分析
    render_separator("标签分析")
    
    tags_data = get_all_tags(limit=50)
    
    if tags_data:
        tag_df = pd.DataFrame(tags_data, columns=["标签", "出现次数"])
        st.dataframe(tag_df.head(20), width='stretch', hide_index=True)
    else:
        render_empty_state("暂无标签数据", icon="🏷️")


# ==================== 其他分析页面占位符 ====================

def render_duration_analysis():
    """渲染时长分析页面"""
    st.title("⏱️ 视频时长分析")

    # 导航提示
    st.info("""
    💡 **导航提示**
    
    - 使用左侧导航栏切换页面
    - 返回主页点击"视频管理"或"整体看板"
    """, icon="🧭")
    
    st.markdown("---")

    # 导航提示
    st.info("""
    💡 **导航提示**
    
    - 使用左侧导航栏切换页面
    - 返回主页点击"视频管理"或"整体看板"
    """, icon="🧭")
    
    st.markdown("---")
    render_info_box("功能开发中", "此功能正在开发中，敬请期待！")

def render_publish_time_analysis():
    """渲染发布时间分析页面"""
    st.title("🕐 发布时间分析")

    # 导航提示
    st.info("""
    💡 **导航提示**
    
    - 使用左侧导航栏切换页面
    - 返回主页点击"视频管理"或"整体看板"
    """, icon="🧭")
    
    st.markdown("---")
    render_info_box("功能开发中", "此功能正在开发中，敬请期待！")

def render_tags_analysis():
    """渲染标签分析页面"""
    st.title("🏷️ 标签分析")

    # 导航提示
    st.info("""
    💡 **导航提示**
    
    - 使用左侧导航栏切换页面
    - 返回主页点击"视频管理"或"整体看板"
    """, icon="🧭")
    
    st.markdown("---")
    render_info_box("功能开发中", "此功能正在开发中，敬请期待！")

def render_sentiment_analysis():
    """渲染情感分析页面"""
    st.title("😊 情感分析")

    # 导航提示
    st.info("""
    💡 **导航提示**
    
    - 使用左侧导航栏切换页面
    - 返回主页点击"视频管理"或"整体看板"
    """, icon="🧭")
    
    st.markdown("---")
    render_info_box("功能开发中", "此功能正在开发中，敬请期待！")

def render_user_profile():
    """渲染用户画像页面"""
    st.title("👥 用户画像")

    # 导航提示
    st.info("""
    💡 **导航提示**
    
    - 使用左侧导航栏切换页面
    - 返回主页点击"视频管理"或"整体看板"
    """, icon="🧭")
    
    st.markdown("---")
    render_info_box("功能开发中", "此功能正在开发中，敬请期待！")

def render_comment_analysis():
    """渲染评论分析页面"""
    st.title("💬 评论分析")
    
    videos = get_videos()
    
    if not videos:
        render_empty_state("暂无监控视频，请先添加视频", icon="📊")
        return
    
    # 选择视频
    video_options = {f"{video[1]} ({video[0]})": video[0] for video in videos}
    selected_video = st.selectbox("选择视频", list(video_options.keys()))
    
    video_id = video_options[selected_video]
    
    # 获取最活跃评论者
    top_commenters = get_top_commenters(video_id, limit=10)
    
    if top_commenters:
        commenter_df = pd.DataFrame(top_commenters)
        st.subheader("最活跃评论者")
        st.dataframe(commenter_df, width='stretch', hide_index=True)
    
    # 获取最多点赞的评论
    most_liked = get_most_liked_comments(video_id, limit=10)
    
    if most_liked:
        st.subheader("最多点赞的评论")
        for i, comment in enumerate(most_liked, 1):
            st.markdown(f"**{i}. {comment['author_name']}** ({comment['like_count']} 点赞)")
            st.markdown(f">{comment['text'][:200]}...")
            st.markdown("---")


def render_api_settings():
    """渲染 API 设置页面"""
    st.title("🔑 API 配置")
    
    render_section_title("YouTube Data API", "配置您的 YouTube Data API 密钥")
    
    current_api_key = st.session_state.get("api_key", "")
    
    api_key_input = st.text_input(
        "API 密钥",
        value=current_api_key,
        type="password",
        help="从 Google Cloud Console 获取您的 YouTube Data API v3 密钥"
    )
    
    if st.button("保存 API 密钥", type="primary"):
        st.session_state.api_key = api_key_input
        set_api_key(api_key_input)
        render_success_box("保存成功", "API 密钥已更新")


def render_data_source():
    """渲染数据源管理页面"""
    st.title("📊 数据源管理")
    
    render_info_box("数据源说明", "当前使用 SQLite 数据库存储数据，数据文件为 youtube_dashboard.db")
    
    st.markdown("---")
    
    render_section_title("数据库统计")
    
    videos = get_videos()
    
    if videos:
        st.metric("监控视频数", len(videos))
        
        total_views = sum([video[4] or 0 for video in videos])
        st.metric("总观看量", format_number(total_views))
    else:
        render_empty_state("暂无数据", icon="📊")


def render_error_box(title, content):
    """渲染错误框（临时函数，使用组件中的）"""
    st.error(f"{title}: {content}")


# 运行主函数
if __name__ == "__main__":
    main()
