"""
视频分析模块
提供视频数据分析功能
"""

import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from typing import List, Tuple, Any
from database import get_video_stats_history, get_video_info, get_latest_stats


def analyze_video_performance(video_id: str, days: int = 30) -> dict:
    """
    分析视频表现
    
    Args:
        video_id: 视频 ID
        days: 分析天数
    
    Returns:
        分析结果字典
    """
    # 获取视频信息
    video_info = get_video_info(video_id)
    if not video_info:
        return None
    
    # 获取历史数据
    history = get_video_stats_history(video_id, days)
    
    if not history:
        return {
            "video_info": video_info,
            "trend": "无数据",
            "growth_rate": 0,
            "avg_daily_views": 0
        }
    
    # 转换为 DataFrame
    df = pd.DataFrame(history, columns=["date", "avg_views", "avg_likes", "avg_comments"])
    df["date"] = pd.to_datetime(df["date"])
    
    # 计算增长率
    first_views = df["avg_views"].iloc[0] if len(df) > 0 else 0
    last_views = df["avg_views"].iloc[-1] if len(df) > 0 else 0
    growth_rate = ((last_views - first_views) / first_views * 100) if first_views > 0 else 0
    
    # 计算日均观看量
    avg_daily_views = df["avg_views"].mean()
    
    # 判断趋势
    if growth_rate > 10:
        trend = "快速上升"
    elif growth_rate > 0:
        trend = "缓慢上升"
    elif growth_rate > -10:
        trend = "缓慢下降"
    else:
        trend = "快速下降"
    
    return {
        "video_info": video_info,
        "trend": trend,
        "growth_rate": growth_rate,
        "avg_daily_views": avg_daily_views,
        "history": df
    }


def create_performance_chart(video_id: str, days: int = 30) -> go.Figure:
    """
    创建视频表现图表
    
    Args:
        video_id: 视频 ID
        days: 显示天数
    
    Returns:
        Plotly 图表对象
    """
    history = get_video_stats_history(video_id, days)
    
    if not history:
        # 返回空图表
        fig = go.Figure()
        fig.add_annotation(
            text="暂无数据",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )
        return fig
    
    df = pd.DataFrame(history, columns=["date", "avg_views", "avg_likes", "avg_comments"])
    df["date"] = pd.to_datetime(df["date"])
    
    # 创建图表
    fig = go.Figure()
    
    # 观看量曲线
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["avg_views"],
        name="观看量",
        line=dict(color="#667eea", width=3),
        fill="tozeroy",
        fillcolor="rgba(102, 126, 234, 0.1)"
    ))
    
    # 点赞量曲线
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["avg_likes"],
        name="点赞量",
        line=dict(color="#43e97b", width=2)
    ))
    
    # 评论量曲线
    fig.add_trace(go.Scatter(
        x=df["date"],
        y=df["avg_comments"],
        name="评论量",
        line=dict(color="#ff6b6b", width=2)
    ))
    
    # 更新布局
    fig.update_layout(
        title="视频数据趋势",
        xaxis_title="日期",
        yaxis_title="数量",
        hovermode="x unified",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig


def create_comparison_chart(video_ids: List[str], metric: str = "view_count") -> go.Figure:
    """
    创建多视频对比图表
    
    Args:
        video_ids: 视频 ID 列表
        metric: 对比指标 (view_count/like_count/comment_count)
    
    Returns:
        Plotly 图表对象
    """
    data = []
    
    for video_id in video_ids:
        video_info = get_video_info(video_id)
        if video_info:
            latest_stats = get_latest_stats(video_id)
            if latest_stats:
                data.append({
                    "title": video_info["title"][:30] + "...",
                    "value": latest_stats.get(metric, 0)
                })
    
    if not data:
        fig = go.Figure()
        fig.add_annotation(
            text="暂无数据",
            xref="paper", yref="paper",
            x=0.5, y=0.5,
            showarrow=False
        )
        return fig
    
    df = pd.DataFrame(data)
    
    # 根据指标选择颜色
    color_map = {
        "view_count": "#667eea",
        "like_count": "#43e97b",
        "comment_count": "#ff6b6b"
    }
    color = color_map.get(metric, "#667eea")
    
    # 创建柱状图
    fig = go.Figure(data=[
        go.Bar(
            x=df["title"],
            y=df["value"],
            marker_color=color,
            text=df["value"],
            textposition="auto"
        )
    ])
    
    # 更新布局
    metric_name_map = {
        "view_count": "观看量",
        "like_count": "点赞量",
        "comment_count": "评论量"
    }
    
    fig.update_layout(
        title=f"{metric_name_map.get(metric, '数据')}对比",
        xaxis_title="视频",
        yaxis_title="数量",
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#ffffff"),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    
    return fig


def generate_optimization_suggestions(video_id: str) -> List[dict]:
    """
    生成优化建议
    
    Args:
        video_id: 视频 ID
    
    Returns:
        优化建议列表
    """
    suggestions = []
    
    # 获取视频信息和统计数据
    video_info = get_video_info(video_id)
    if not video_info:
        return suggestions
    
    latest_stats = get_latest_stats(video_id)
    if not latest_stats:
        return suggestions
    
    # 分析观看量
    view_count = latest_stats.get("view_count", 0)
    like_count = latest_stats.get("like_count", 0)
    comment_count = latest_stats.get("comment_count", 0)
    
    # 观看量建议
    if view_count < 1000:
        suggestions.append({
            "type": "warning",
            "title": "观看量较低",
            "message": f"当前观看量为 {view_count}，建议优化标题和缩略图，增加前30秒的吸引力。"
        })
    elif view_count < 10000:
        suggestions.append({
            "type": "info",
            "title": "观看量有提升空间",
            "message": f"当前观看量为 {view_count}，建议分析高观看量视频的共同特点，优化内容结构。"
        })
    
    # 互动率建议
    if like_count > 0:
        engagement_rate = (like_count / view_count) * 100
        if engagement_rate < 2:
            suggestions.append({
                "type": "warning",
                "title": "互动率偏低",
                "message": f"点赞率为 {engagement_rate:.2f}%，建议在视频中引导用户点赞和评论。"
            })
    
    # 评论建议
    if comment_count < 10:
        suggestions.append({
            "type": "info",
            "title": "评论较少",
            "message": "建议在视频结尾提出问题，引导用户参与讨论。"
        })
    
    # 标题建议
    title = video_info.get("title", "")
    if len(title) < 30:
        suggestions.append({
            "type": "info",
            "title": "标题较短",
            "message": "建议增加标题长度，包含更多关键词以提升搜索排名。"
        })
    elif len(title) > 100:
        suggestions.append({
            "type": "warning",
            "title": "标题过长",
            "message": "建议缩短标题，确保在前50个字符中包含关键信息。"
        })
    
    # 描述建议
    description = video_info.get("description", "")
    if len(description) < 200:
        suggestions.append({
            "type": "info",
            "title": "描述较短",
            "message": "建议在描述中添加更多关键词和视频内容概述，提升搜索排名。"
        })
    
    return suggestions
