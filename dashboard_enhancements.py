#!/usr/bin/env python3
"""
Dashboard 增强 - 导航修复和完整数据看板

问题 1: 导航后无法返回
问题 2: 整体数据看板维度不完整

解决方案:
1. 在每个页面添加导航提示
2. 重新设计整体数据看板，包含完整的数据分析维度
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from collections import Counter
import re

# 导入自定义模块
from database import (
    init_database,
    get_videos,
    get_video_info,
    get_latest_stats,
    get_video_stats_history,
)
from utils import (
    format_number,
    format_percentage,
    calculate_engagement_rate,
    get_video_age,
    truncate_text,
)

# YouTube 数据分析维度
"""
作为 YouTube 数据分析专家，整体数据看板应该包含以下维度：

1. 核心指标 (Core Metrics)
   - 总观看量、总点赞量、总评论量
   - 平均互动率
   - 视频数量、频道数量

2. 观看趋势 (View Trends)
   - 每日观看量趋势
   - 增长率
   - 峰值分析

3. 内容表现 (Content Performance)
   - 热门视频排行榜
   - 互动率排行榜
   - 时长分布
   - 发布时间分析

4. 用户参与度 (Engagement)
   - 点赞率、评论率
   - 互动率分布
   - 高互动视频特征

5. 视频质量 (Video Quality)
   - 观看完成率（如果有数据）
   - 重复观看（如果有数据）
   - 点击率（如果有数据）

6. 时间维度 (Time Analysis)
   - 按周/月/季度的表现
   - 发布时间效果
   - 周期性分析

7. 竞争分析 (Competitive Analysis)
   - 视频间对比
   - 表现差异分析
   - 最佳实践总结

8. 优化建议 (Optimization)
   - 基于数据的优化建议
   - 下一步行动计划
   - 目标设定
"""


def render_navigation_help():
    """渲染导航帮助"""
    st.info("""
    💡 **导航提示**
    
    - 使用左侧导航栏切换页面
    - 每个页面都包含数据分析或功能
    - 返回主页点击"视频管理"或"整体看板"
    """, icon="🧭")


def render_enhanced_overall_dashboard():
    """渲染增强的整体数据看板"""
    
    st.title("📊 整体数据看板")
    
    # 导航提示
    render_navigation_help()
    
    # 获取数据
    videos = get_videos()
    
    if not videos:
        st.warning("暂无监控视频，请先添加视频到视频管理页面", icon="⚠️")
        return
    
    # ==================== 1. 核心指标 ====================
    st.subheader("📈 核心指标")
    
    # 计算总体数据
    total_views = sum([video[4] or 0 for video in videos])
    total_likes = sum([video[5] or 0 for video in videos])
    total_comments = sum([video[6] or 0 for video in videos])
    
    # 计算平均互动率
    engagement_rates = []
    for video in videos:
        er = calculate_engagement_rate(
            video[5] or 0,
            video[6] or 0,
            video[4] or 0
        )
        engagement_rates.append(er)
    
    avg_engagement_rate = sum(engagement_rates) / len(engagement_rates) if engagement_rates else 0
    
    # 统计频道数量
    channels = set([video[2] for video in videos])
    channel_count = len(channels)
    
    # 显示核心指标
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric("总视频数", len(videos))
    
    with col2:
        st.metric("总频道数", channel_count)
    
    with col3:
        st.metric("总观看量", format_number(total_views))
    
    with col4:
        st.metric("总点赞量", format_number(total_likes))
    
    with col5:
        st.metric("平均互动率", format_percentage(avg_engagement_rate))
    
    st.markdown("---")
    
    # ==================== 2. 观看趋势 ====================
    st.subheader("📈 观看趋势")
    
    # 创建趋势图表
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("### 观看量排行 Top 10")
        
        video_list = []
        for video in videos:
            video_list.append({
                "视频标题": truncate_text(video[1], 40),
                "频道": video[2],
                "观看量": video[4] or 0,
                "点赞量": video[5] or 0,
                "评论量": video[6] or 0,
                "互动率": calculate_engagement_rate(video[5] or 0, video[6] or 0, video[4] or 0)
            })
        
        df = pd.DataFrame(video_list)
        df_sorted = df.sort_values("观看量", ascending=False).head(10)
        
        fig = px.bar(
            df_sorted,
            x="观看量",
            y="视频标题",
            orientation="h",
            color="观看量",
            color_continuous_scale="viridis",
            title="观看量 Top 10"
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            height=500,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.write("### 互动率排行 Top 10")
        
        df_engagement = df.sort_values("互动率", ascending=False).head(10)
        
        fig = px.bar(
            df_engagement,
            x="互动率",
            y="视频标题",
            orientation="h",
            color="互动率",
            color_continuous_scale="plasma",
            title="互动率 Top 10"
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            height=500,
            margin=dict(l=0, r=0, t=30, b=0)
        )
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    # ==================== 3. 内容表现分布 ====================
    st.subheader("📊 内容表现分布")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.write("#### 观看量分布")
        
        view_ranges = pd.cut(df["观看量"], bins=5, labels=[
            "0-1K", "1K-10K", "10K-50K", "50K-100K", "100K+"
        ])
        view_dist = pd.DataFrame({"观看量范围": view_ranges})
        view_counts = view_dist["观看量范围"].value_counts().sort_index()
        
        fig = px.pie(
            values=view_counts.values,
            names=view_counts.index,
            title="观看量分布",
            hole=0.3
        )
        fig.update_layout(
            template="plotly_dark",
            font=dict(color="#ffffff"),
            height=400
        )
        st.plotly_chart(fig, width='stretch')
    
    with col2:
        st.write("#### 互动率分布")
        
        er_ranges = pd.cut(df["互动率"], bins=5, labels=[
            "0-2%", "2-4%", "4-6%", "6-8%", "8%+"
        ])
        er_dist = pd.DataFrame({"互动率范围": er_ranges})
        er_counts = er_dist["互动率范围"].value_counts().sort_index()
        
        fig = px.pie(
            values=er_counts.values,
            names=er_counts.index,
            title="互动率分布",
            hole=0.3
        )
        fig.update_layout(
            template="plotly_dark",
            font=dict(color="#ffffff"),
            height=400
        )
        st.plotly_chart(fig, width='stretch')
    
    with col3:
        st.write("#### 频道分布")
        
        channel_dist = df["频道"].value_counts().head(10)
        
        fig = px.bar(
            x=channel_dist.values,
            y=channel_dist.index,
            orientation="h",
            title="频道视频数量",
            color=channel_dist.values,
            color_continuous_scale="viridis"
        )
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#ffffff"),
            height=400
        )
        st.plotly_chart(fig, width='stretch')
    
    st.markdown("---")
    
    # ==================== 4. 关键洞察 ====================
    st.subheader("💡 关键洞察")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("#### 表现最佳")
        
        best_video = df.loc[df["观看量"].idxmax()]
        st.success(f"""
        **最高观看量**: {best_video['视频标题']}
        
        - 观看量: {format_number(best_video['观看量'])}
        - 互动率: {format_percentage(best_video['互动率'])}
        - 频道: {best_video['频道']}
        """)
    
    with col2:
        st.write("#### 互动最佳")
        
        best_engagement = df.loc[df["互动率"].idxmax()]
        st.info(f"""
        **最高互动率**: {best_engagement['视频标题']}
        
        - 观看量: {format_number(best_engagement['观看量'])}
        - 互动率: {format_percentage(best_engagement['互动率'])}
        - 点赞量: {format_number(best_engagement['点赞量'])}
        """)
    
    st.markdown("---")
    
    # ==================== 5. 优化建议 ====================
    st.subheader("🎯 优化建议")
    
    # 基于数据的建议
    suggestions = []
    
    # 1. 互动率分析
    low_engagement = df[df["互动率"] < 3]
    if len(low_engagement) > 0:
        suggestions.append({
            "type": "warning",
            "title": "部分视频互动率偏低",
            "message": f"有 {len(low_engagement)} 个视频的互动率低于 3%，建议：\n"
                      "- 在视频结尾提出问题引导评论\n"
                      "- 增加互动元素（投票、问答）\n"
                      "- 优化视频开头前 3 秒的吸引力"
        })
    else:
        suggestions.append({
            "type": "success",
            "title": "互动率表现优秀",
            "message": "所有视频的互动率都在合理范围内，继续保持！"
        })
    
    # 2. 观看量分析
    high_performers = df[df["观看量"] > 10000]
    if len(high_performers) > 0:
        suggestions.append({
            "type": "info",
            "title": "发现高表现视频",
            "message": f"有 {len(high_performers)} 个视频观看量超过 1万，建议分析这些视频的共同特点。"
        })
    
    # 3. 发布时间建议
    suggestions.append({
        "type": "info",
        "title": "发布时间优化",
        "message": "建议分析高表现视频的发布时间，找出最佳发布时段。"
    })
    
    # 显示建议
    for i, sugg in enumerate(suggestions, 1):
        if sugg["type"] == "warning":
            st.warning(f"**{i}. {sugg['title']}**\n\n{sugg['message']}")
        elif sugg["type"] == "success":
            st.success(f"**{i}. {sugg['title']}**\n\n{sugg['message']}")
        else:
            st.info(f"**{i}. {sugg['title']}**\n\n{sugg['message']}")
    
    st.markdown("---")
    
    # ==================== 6. 数据导出 ====================
    st.subheader("📥 数据导出")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("导出完整数据", type="primary"):
            csv = df.to_csv(index=False)
            st.download_button(
                label="下载 CSV",
                data=csv,
                file_name="youtube_dashboard_data.csv",
                mime="text/csv"
            )
    
    with col2:
        st.write("#### 数据说明")
        st.info("""
        导出的数据包含所有监控视频的核心指标：
        - 观看量、点赞量、评论量
        - 互动率
        - 频道信息
        """, icon="📊")


if __name__ == "__main__":
    # 初始化
    init_database()
    
    # 渲染增强的整体数据看板
    render_enhanced_overall_dashboard()
