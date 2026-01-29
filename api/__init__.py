"""
API 模块初始化文件
"""

from .youtube_api import YouTubeAPI, extract_video_id

__all__ = [
    "YouTubeAPI",
    "extract_video_id",
]
