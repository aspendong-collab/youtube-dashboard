"""
YouTube API 封装模块
封装 YouTube Data API v3 的调用
"""

import requests
from typing import List, Dict, Optional
import streamlit as st
import os


class YouTubeAPI:
    """YouTube API 客户端"""
    
    def __init__(self, api_key: str = None):
        """
        初始化 YouTube API 客户端
        
        Args:
            api_key: YouTube Data API 密钥
        """
        self.api_key = api_key or os.environ.get("YOUTUBE_API_KEY")
        self.base_url = "https://www.googleapis.com/youtube/v3"
        
        if not self.api_key:
            st.warning("未设置 YouTube API 密钥，部分功能可能无法使用")
    
    def _make_request(self, endpoint: str, params: dict) -> Optional[dict]:
        """
        发送 API 请求
        
        Args:
            endpoint: API 端点
            params: 请求参数
        
        Returns:
            响应数据字典，失败时返回 None
        """
        try:
            params["key"] = self.api_key
            url = f"{self.base_url}/{endpoint}"
            
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            return response.json()
            
        except requests.exceptions.RequestException as e:
            st.error(f"API 请求失败: {str(e)}")
            return None
    
    def get_video_info(self, video_ids: List[str]) -> List[Dict]:
        """
        获取视频信息
        
        Args:
            video_ids: 视频 ID 列表（最多 50 个）
        
        Returns:
            视频信息列表
        """
        if not self.api_key:
            return []
        
        params = {
            "part": "snippet,contentDetails,statistics",
            "id": ",".join(video_ids)
        }
        
        data = self._make_request("videos", params)
        
        if data and "items" in data:
            videos = []
            for item in data["items"]:
                videos.append({
                    "video_id": item["id"],
                    "title": item["snippet"]["title"],
                    "channel_id": item["snippet"]["channelId"],
                    "channel_title": item["snippet"]["channelTitle"],
                    "thumbnail_url": item["snippet"]["thumbnails"]["high"]["url"],
                    "published_at": item["snippet"]["publishedAt"],
                    "duration": item["contentDetails"]["duration"],
                    "category_id": item["snippet"]["categoryId"],
                    "tags": item["snippet"].get("tags", []),
                    "description": item["snippet"]["description"],
                    "view_count": int(item["statistics"].get("viewCount", 0)),
                    "like_count": int(item["statistics"].get("likeCount", 0)),
                    "comment_count": int(item["statistics"].get("commentCount", 0)),
                    "favorite_count": int(item["statistics"].get("favoriteCount", 0))
                })
            return videos
        
        return []
    
    def search_videos(self, query: str, max_results: int = 10) -> List[Dict]:
        """
        搜索视频
        
        Args:
            query: 搜索关键词
            max_results: 最大结果数
        
        Returns:
            视频信息列表
        """
        if not self.api_key:
            return []
        
        params = {
            "part": "snippet",
            "q": query,
            "type": "video",
            "maxResults": min(max_results, 50)
        }
        
        data = self._make_request("search", params)
        
        if data and "items" in data:
            video_ids = [item["id"]["videoId"] for item in data["items"]]
            return self.get_video_info(video_ids)
        
        return []
    
    def get_video_comments(self, video_id: str, max_results: int = 100) -> List[Dict]:
        """
        获取视频评论
        
        Args:
            video_id: 视频 ID
            max_results: 最大结果数
        
        Returns:
            评论列表
        """
        if not self.api_key:
            return []
        
        comments = []
        next_page_token = None
        
        while len(comments) < max_results:
            params = {
                "part": "snippet",
                "videoId": video_id,
                "maxResults": min(100, max_results - len(comments)),
                "order": "relevance"
            }
            
            if next_page_token:
                params["pageToken"] = next_page_token
            
            data = self._make_request("commentThreads", params)
            
            if not data or "items" not in data:
                break
            
            for item in data["items"]:
                comment = item["snippet"]["topLevelComment"]["snippet"]
                comments.append({
                    "comment_id": item["id"],
                    "author_name": comment["authorDisplayName"],
                    "author_channel_url": comment.get("authorChannelUrl", ""),
                    "like_count": comment.get("likeCount", 0),
                    "text": comment["textDisplay"],
                    "published_at": comment["publishedAt"],
                    "updated_at": comment.get("updatedAt", comment["publishedAt"])
                })
            
            next_page_token = data.get("nextPageToken")
            if not next_page_token:
                break
        
        return comments[:max_results]
    
    def get_channel_info(self, channel_id: str) -> Optional[Dict]:
        """
        获取频道信息
        
        Args:
            channel_id: 频道 ID
        
        Returns:
            频道信息字典，失败时返回 None
        """
        if not self.api_key:
            return None
        
        params = {
            "part": "snippet,statistics",
            "id": channel_id
        }
        
        data = self._make_request("channels", params)
        
        if data and "items" in data:
            item = data["items"][0]
            return {
                "channel_id": item["id"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "thumbnail_url": item["snippet"]["thumbnails"]["high"]["url"],
                "subscriber_count": int(item["statistics"].get("subscriberCount", 0)),
                "video_count": int(item["statistics"].get("videoCount", 0)),
                "view_count": int(item["statistics"].get("viewCount", 0))
            }
        
        return None


def extract_video_id(url_or_id: str) -> Optional[str]:
    """
    从 URL 或 ID 中提取视频 ID
    
    Args:
        url_or_id: YouTube URL 或视频 ID
    
    Returns:
        视频 ID，如果无效则返回 None
    """
    import re
    
    # 如果已经是 ID（11位字母数字）
    if re.match(r'^[a-zA-Z0-9_-]{11}$', url_or_id):
        return url_or_id
    
    # 尝试从各种 URL 格式中提取 ID
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/shorts\/([a-zA-Z0-9_-]{11})',
        r'youtube\.com\/v\/([a-zA-Z0-9_-]{11})'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url_or_id)
        if match:
            return match.group(1)
    
    return None
