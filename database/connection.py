"""
数据库连接模块
封装数据库连接和基础操作
"""

import sqlite3
from contextlib import contextmanager
from typing import List, Tuple, Any, Optional
import streamlit as st


@contextmanager
def get_db_connection():
    """
    获取数据库连接上下文管理器
    
    使用示例:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM videos")
            rows = cursor.fetchall()
    """
    conn = sqlite3.connect("youtube_dashboard.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()


def init_database():
    """
    初始化数据库表结构
    
    如果表不存在，则创建必要的表
    如果表存在但缺少列，则自动添加缺失的列
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        # 创建视频表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS videos (
            video_id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            channel_id TEXT,
            channel_title TEXT,
            thumbnail_url TEXT,
            published_at TEXT,
            duration TEXT,
            category_id TEXT,
            tags TEXT,
            description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # 创建视频统计表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS video_stats (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            view_count INTEGER,
            like_count INTEGER,
            comment_count INTEGER,
            favorite_count INTEGER,
            recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos(video_id)
        )
        """)
        
        # 检查并修复 video_stats 表的 recorded_at 列
        try:
            cursor.execute("SELECT recorded_at FROM video_stats LIMIT 1")
        except sqlite3.OperationalError:
            # 列不存在，添加列
            cursor.execute("ALTER TABLE video_stats ADD COLUMN recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
            conn.commit()
        
        # 创建评论表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            comment_id TEXT UNIQUE,
            author_name TEXT,
            author_channel_url TEXT,
            like_count INTEGER,
            text TEXT,
            published_at TEXT,
            updated_at TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos(video_id)
        )
        """)
        
        # 创建标签表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tags (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            tag TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos(video_id)
        )
        """)
        
        # 创建预警表
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            video_id TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            threshold_value INTEGER,
            current_value INTEGER,
            message TEXT,
            is_read BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (video_id) REFERENCES videos(video_id)
        )
        """)
        
        conn.commit()


def get_video_ids() -> List[str]:
    """
    获取所有视频 ID
    
    Returns:
        视频ID列表
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT video_id FROM videos ORDER BY published_at DESC")
        rows = cursor.fetchall()
        return [row[0] for row in rows]


def get_videos() -> List[Tuple[Any, ...]]:
    """
    获取所有视频信息
    
    Returns:
        视频信息列表
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                video_id, title, channel_title, published_at, 
                view_count, like_count, comment_count
            FROM videos v
            LEFT JOIN (
                SELECT video_id, view_count, like_count, comment_count,
                       ROW_NUMBER() OVER (PARTITION BY video_id ORDER BY recorded_at DESC) as rn
                FROM video_stats
            ) vs ON v.video_id = vs.video_id AND vs.rn = 1
            ORDER BY v.published_at DESC
        """)
        return cursor.fetchall()


def get_video_info(video_id: str) -> Optional[sqlite3.Row]:
    """
    获取单个视频信息
    
    Args:
        video_id: 视频 ID
    
    Returns:
        视频信息字典，如果不存在则返回 None
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM videos WHERE video_id = ?", (video_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_latest_stats(video_id: str) -> Optional[sqlite3.Row]:
    """
    获取视频的最新统计数据
    
    Args:
        video_id: 视频 ID
    
    Returns:
        最新统计数据，如果不存在则返回 None
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM video_stats 
            WHERE video_id = ? 
            ORDER BY recorded_at DESC 
            LIMIT 1
        """, (video_id,))
        row = cursor.fetchone()
        return dict(row) if row else None


def get_video_stats_history(video_id: str, days: int = 30) -> List[Tuple[Any, ...]]:
    """
    获取视频统计数据历史
    
    Args:
        video_id: 视频 ID
        days: 获取最近多少天的数据
    
    Returns:
        统计数据历史列表
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                DATE(recorded_at) as date,
                AVG(view_count) as avg_views,
                AVG(like_count) as avg_likes,
                AVG(comment_count) as avg_comments
            FROM video_stats
            WHERE video_id = ? 
                AND recorded_at >= DATE('now', ? || ' days')
            GROUP BY DATE(recorded_at)
            ORDER BY date ASC
        """, (video_id, -days))
        return cursor.fetchall()


def add_video(video_data: dict) -> bool:
    """
    添加视频
    
    Args:
        video_data: 视频数据字典
    
    Returns:
        是否成功
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO videos 
                (video_id, title, channel_id, channel_title, thumbnail_url, 
                 published_at, duration, category_id, tags, description)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                video_data.get("video_id"),
                video_data.get("title"),
                video_data.get("channel_id"),
                video_data.get("channel_title"),
                video_data.get("thumbnail_url"),
                video_data.get("published_at"),
                video_data.get("duration"),
                video_data.get("category_id"),
                video_data.get("tags"),
                video_data.get("description")
            ))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"添加视频失败: {str(e)}")
        return False


def save_video_stats(video_id: str, stats: dict) -> bool:
    """
    保存视频统计数据
    
    Args:
        video_id: 视频 ID
        stats: 统计数据字典
    
    Returns:
        是否成功
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO video_stats 
                (video_id, view_count, like_count, comment_count, favorite_count)
                VALUES (?, ?, ?, ?, ?)
            """, (
                video_id,
                stats.get("view_count", 0),
                stats.get("like_count", 0),
                stats.get("comment_count", 0),
                stats.get("favorite_count", 0)
            ))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"保存统计数据失败: {str(e)}")
        return False


def get_comments(video_id: str, limit: int = 100) -> List[Tuple[Any, ...]]:
    """
    获取视频评论
    
    Args:
        video_id: 视频 ID
        limit: 获取评论数量限制
    
    Returns:
        评论列表
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM comments
            WHERE video_id = ?
            ORDER BY like_count DESC
            LIMIT ?
        """, (video_id, limit))
        return cursor.fetchall()


def save_comment(video_id: str, comment_data: dict) -> bool:
    """
    保存评论
    
    Args:
        video_id: 视频 ID
        comment_data: 评论数据字典
    
    Returns:
        是否成功
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO comments
                (video_id, comment_id, author_name, author_channel_url, 
                 like_count, text, published_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                video_id,
                comment_data.get("comment_id"),
                comment_data.get("author_name"),
                comment_data.get("author_channel_url"),
                comment_data.get("like_count", 0),
                comment_data.get("text"),
                comment_data.get("published_at"),
                comment_data.get("updated_at")
            ))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"保存评论失败: {str(e)}")
        return False


def save_tags(video_id: str, tags: List[str]) -> bool:
    """
    保存视频标签
    
    Args:
        video_id: 视频 ID
        tags: 标签列表
    
    Returns:
        是否成功
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            # 删除旧标签
            cursor.execute("DELETE FROM tags WHERE video_id = ?", (video_id,))
            
            # 插入新标签
            for tag in tags:
                cursor.execute("""
                    INSERT INTO tags (video_id, tag)
                    VALUES (?, ?)
                """, (video_id, tag))
            
            conn.commit()
            return True
    except Exception as e:
        st.error(f"保存标签失败: {str(e)}")
        return False


def get_all_tags(limit: int = 50) -> List[Tuple[Any, ...]]:
    """
    获取所有标签及其出现频率
    
    Args:
        limit: 获取标签数量限制
    
    Returns:
        标签列表（标签名, 出现次数）
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT tag, COUNT(*) as count
            FROM tags
            GROUP BY tag
            ORDER BY count DESC
            LIMIT ?
        """, (limit,))
        return cursor.fetchall()


def create_alert(video_id: str, alert_type: str, threshold_value: int, 
                 current_value: int, message: str) -> bool:
    """
    创建预警
    
    Args:
        video_id: 视频 ID
        alert_type: 预警类型
        threshold_value: 阈值
        current_value: 当前值
        message: 预警消息
    
    Returns:
        是否成功
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO alerts
                (video_id, alert_type, threshold_value, current_value, message)
                VALUES (?, ?, ?, ?, ?)
            """, (video_id, alert_type, threshold_value, current_value, message))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"创建预警失败: {str(e)}")
        return False


def get_unread_alerts() -> List[Tuple[Any, ...]]:
    """
    获取未读预警
    
    Returns:
        未读预警列表
    """
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.*, v.title
            FROM alerts a
            JOIN videos v ON a.video_id = v.video_id
            WHERE a.is_read = 0
            ORDER BY a.created_at DESC
        """)
        return cursor.fetchall()


def mark_alert_as_read(alert_id: int) -> bool:
    """
    标记预警为已读
    
    Args:
        alert_id: 预警 ID
    
    Returns:
        是否成功
    """
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE alerts SET is_read = 1 WHERE id = ?", (alert_id,))
            conn.commit()
            return True
    except Exception as e:
        st.error(f"标记预警失败: {str(e)}")
        return False
