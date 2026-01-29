"""
分析模块初始化文件
"""

from .video_analytics import (
    analyze_video_performance,
    create_performance_chart,
    create_comparison_chart,
    generate_optimization_suggestions,
)
from .comment_analytics import (
    generate_word_cloud,
    clean_text,
    analyze_comment_sentiment,
    get_top_commenters,
    get_most_liked_comments,
)

__all__ = [
    "analyze_video_performance",
    "create_performance_chart",
    "create_comparison_chart",
    "generate_optimization_suggestions",
    "generate_word_cloud",
    "clean_text",
    "analyze_comment_sentiment",
    "get_top_commenters",
    "get_most_liked_comments",
]
