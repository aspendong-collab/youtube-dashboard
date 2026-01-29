"""
工具函数模块
提供通用的辅助函数
"""

import time
from functools import wraps
from typing import List, Any
import streamlit as st


def retry_on_failure(max_retries: int = 3, delay: float = 1.0):
    """
    失败重试装饰器
    
    Args:
        max_retries: 最大重试次数
        delay: 重试间隔（秒）
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    if attempt < max_retries - 1:
                        time.sleep(delay)
            
            raise last_exception
        
        return wrapper
    return decorator


def format_number(num: int) -> str:
    """
    格式化数字（添加千位分隔符）
    
    Args:
        num: 数字
    
    Returns:
        格式化后的字符串
    """
    if num >= 1000000:
        return f"{num / 1000000:.1f}M"
    elif num >= 1000:
        return f"{num / 1000:.1f}K"
    else:
        return str(num)


def format_percentage(value: float) -> str:
    """
    格式化百分比
    
    Args:
        value: 小数值
    
    Returns:
        百分比字符串
    """
    return f"{value * 100:.2f}%"


def safe_divide(numerator: float, denominator: float, default: float = 0.0) -> float:
    """
    安全除法
    
    Args:
        numerator: 分子
        denominator: 分母
        default: 分母为 0 时的默认值
    
    Returns:
        除法结果
    """
    return numerator / denominator if denominator != 0 else default


def truncate_text(text: str, max_length: int = 100, suffix: str = "...") -> str:
    """
    截断文本
    
    Args:
        text: 原始文本
        max_length: 最大长度
        suffix: 后缀
    
    Returns:
        截断后的文本
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - len(suffix)] + suffix


def get_color_class(value: float, thresholds: List[float] = [0.5, 0.8]) -> str:
    """
    根据数值获取颜色类
    
    Args:
        value: 数值（0-1）
        thresholds: 阈值列表
    
    Returns:
        颜色类名
    """
    if value < thresholds[0]:
        return "accent-orange"
    elif value < thresholds[1]:
        return "accent-yellow"
    else:
        return "accent-green"


def show_loading(message: str = "加载中..."):
    """
    显示加载提示
    
    Args:
        message: 加载消息
    """
    with st.spinner(message):
        yield


def cache_key(*args, **kwargs) -> str:
    """
    生成缓存键
    
    Args:
        *args: 位置参数
        **kwargs: 关键字参数
    
    Returns:
        缓存键字符串
    """
    key_parts = [str(arg) for arg in args]
    key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
    return ":".join(key_parts)


def validate_video_id(video_id: str) -> bool:
    """
    验证视频 ID 是否有效
    
    Args:
        video_id: 视频 ID
    
    Returns:
        是否有效
    """
    import re
    return bool(re.match(r'^[a-zA-Z0-9_-]{11}$', video_id))


def parse_duration(duration_str: str) -> int:
    """
    解析 YouTube 视频时长
    
    Args:
        duration_str: ISO 8601 时长字符串（如 PT1H30M15S）
    
    Returns:
        时长（秒）
    """
    import re
    
    pattern = r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?'
    match = re.match(pattern, duration_str)
    
    if not match:
        return 0
    
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    
    return hours * 3600 + minutes * 60 + seconds


def format_duration(seconds: int) -> str:
    """
    格式化时长
    
    Args:
        seconds: 秒数
    
    Returns:
        格式化后的时长字符串（如 1:30:15）
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    seconds = seconds % 60
    
    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def calculate_engagement_rate(likes: int, comments: int, views: int) -> float:
    """
    计算互动率
    
    Args:
        likes: 点赞数
        comments: 评论数
        views: 观看数
    
    Returns:
        互动率（0-1）
    """
    return safe_divide(likes + comments, views, 0.0)


def get_video_age(published_at: str) -> str:
    """
    获取视频年龄
    
    Args:
        published_at: 发布时间（ISO 8601 格式）
    
    Returns:
        年龄字符串（如 "2 days ago"）
    """
    from datetime import datetime
    
    published = datetime.fromisoformat(published_at.replace("Z", "+00:00"))
    now = datetime.now(published.tzinfo)
    delta = now - published
    
    days = delta.days
    hours = delta.seconds // 3600
    
    if days > 0:
        return f"{days} 天前"
    elif hours > 0:
        return f"{hours} 小时前"
    else:
        return "刚刚"
