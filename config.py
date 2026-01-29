"""
配置管理模块
"""
import os


class Config:
    """应用配置类"""
    
    # YouTube API
    YOUTUBE_API_KEY = os.environ.get("YOUTUBE_API_KEY", "")
    
    # 数据库
    DB_PATH = "youtube_dashboard.db"
    
    # 分页
    ITEMS_PER_PAGE = 20
    
    # 图表
    CHART_HEIGHT = 400
    WORD_CLOUD_WIDTH = 800
    WORD_CLOUD_HEIGHT = 400
    
    # 预警阈值
    ALERT_THRESHOLDS = {
        "view_count": 10000,      # 观看量预警阈值
        "like_count": 1000,       # 点赞量预警阈值
        "comment_count": 100,     # 评论量预警阈值
        "engagement_rate": 5      # 互动率预警阈值（%）
    }
    
    # 缓存
    CACHE_TTL = 300  # 缓存有效期（秒）
    
    # API 请求限制
    API_REQUEST_TIMEOUT = 10  # 超时时间（秒）
    API_MAX_RETRIES = 3      # 最大重试次数
    
    @classmethod
    def set_api_key(cls, api_key: str) -> None:
        """
        设置 YouTube API 密钥
        
        Args:
            api_key: API 密钥
        """
        cls.YOUTUBE_API_KEY = api_key
        os.environ["YOUTUBE_API_KEY"] = api_key


# 全局函数，方便导入
def set_api_key(api_key: str) -> None:
    """设置 YouTube API 密钥"""
    Config.set_api_key(api_key)
