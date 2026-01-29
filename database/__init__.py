"""
数据库模块初始化文件
"""

from .connection import (
    get_db_connection,
    init_database,
    get_video_ids,
    get_videos,
    get_video_info,
    get_latest_stats,
    get_video_stats_history,
    add_video,
    save_video_stats,
    get_comments,
    save_comment,
    save_tags,
    get_all_tags,
    create_alert,
    get_unread_alerts,
    mark_alert_as_read,
)

__all__ = [
    "get_db_connection",
    "init_database",
    "get_video_ids",
    "get_videos",
    "get_video_info",
    "get_latest_stats",
    "get_video_stats_history",
    "add_video",
    "save_video_stats",
    "get_comments",
    "save_comment",
    "save_tags",
    "get_all_tags",
    "create_alert",
    "get_unread_alerts",
    "mark_alert_as_read",
]
