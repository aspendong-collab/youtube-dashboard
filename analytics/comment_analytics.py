"""
评论分析模块
提供评论数据分析功能
"""

import pandas as pd
from collections import Counter
import re
from typing import List, Dict, Tuple
try:
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    HAS_WORDCLOUD = True
except ImportError:
    HAS_WORDCLOUD = False
from database import get_comments


def generate_word_cloud(video_id: str, max_words: int = 100):
    """
    生成评论词云
    
    Args:
        video_id: 视频 ID
        max_words: 最大词数
    
    Returns:
        WordCloud 对象或 None
    """
    if not HAS_WORDCLOUD:
        return None
        
    comments = get_comments(video_id, limit=500)
    
    if not comments:
        # 返回空词云
        wordcloud = WordCloud(width=800, height=400, background_color="rgba(0,0,0,0)")
        return wordcloud
    
    # 合并所有评论文本
    all_text = " ".join([comment[5] for comment in comments])  # comment[5] 是 text 字段
    
    # 清理文本
    all_text = clean_text(all_text)
    
    # 生成词云
    try:
        wordcloud = WordCloud(
            width=800,
            height=400,
            background_color="rgba(0,0,0,0)",
            max_words=max_words,
            colormap="viridis",
            contour_width=1,
            contour_color="steelblue"
        ).generate(all_text)
        
        return wordcloud
        
    except Exception as e:
        # 如果生成失败，返回空词云
        wordcloud = WordCloud(width=800, height=400, background_color="rgba(0,0,0,0)")
        return wordcloud


def clean_text(text: str) -> str:
    """
    清理文本
    
    Args:
        text: 原始文本
    
    Returns:
        清理后的文本
    """
    # 移除 URL
    text = re.sub(r'http\S+', '', text)
    
    # 移除特殊字符（保留中文、英文、数字）
    text = re.sub(r'[^\w\s\u4e00-\u9fff]', ' ', text)
    
    # 转换为小写
    text = text.lower()
    
    # 移除停用词
    stopwords = set([
        "the", "a", "an", "is", "are", "was", "were", "be", "been", "being",
        "have", "has", "had", "do", "does", "did", "will", "would", "could",
        "should", "may", "might", "must", "shall", "can", "need", "dare",
        "this", "that", "these", "those", "i", "you", "he", "she", "it", "we",
        "they", "me", "him", "her", "us", "them", "my", "your", "his", "its",
        "our", "their", "mine", "yours", "hers", "ours", "theirs", "what",
        "which", "who", "whom", "whose", "when", "where", "why", "how", "if",
        "then", "else", "because", "although", "though", "but", "and", "or",
        "so", "for", "nor", "yet", "both", "either", "neither", "not", "only",
        "own", "same", "than", "too", "very", "just", "also", "now", "here",
        "there", "when", "where", "why", "how", "all", "any", "some", "no",
        "each", "every", "both", "few", "many", "much", "more", "most", "less",
        "least", "another", "such", "what", "which", "whatever", "whichever",
        "的", "了", "是", "在", "我", "有", "和", "就", "不", "人", "都", "一",
        "一个", "上", "也", "很", "到", "说", "要", "去", "你", "会", "着", "没有",
        "看", "好", "自己", "这"
    ])
    
    words = text.split()
    words = [word for word in words if word not in stopwords and len(word) > 2]
    
    return " ".join(words)


def analyze_comment_sentiment(video_id: str) -> Dict[str, any]:
    """
    分析评论情感（简化版）
    
    Args:
        video_id: 视频 ID
    
    Returns:
        情感分析结果
    """
    comments = get_comments(video_id, limit=500)
    
    if not comments:
        return {
            "positive": 0,
            "neutral": 0,
            "negative": 0,
            "total": 0
        }
    
    positive_words = ["好", "棒", "赞", "喜欢", "爱", "great", "good", "love", "like", "amazing", "excellent", "awesome"]
    negative_words = ["差", "坏", "讨厌", "不好", "hate", "bad", "terrible", "awful", "worst", "dislike"]
    
    positive_count = 0
    negative_count = 0
    neutral_count = 0
    
    for comment in comments:
        text = comment[5].lower()  # comment[5] 是 text 字段
        
        # 检查正面词汇
        if any(word in text for word in positive_words):
            positive_count += 1
        # 检查负面词汇
        elif any(word in text for word in negative_words):
            negative_count += 1
        else:
            neutral_count += 1
    
    return {
        "positive": positive_count,
        "neutral": neutral_count,
        "negative": negative_count,
        "total": len(comments)
    }


def get_top_commenters(video_id: str, limit: int = 10) -> List[Dict]:
    """
    获取最活跃评论者
    
    Args:
        video_id: 视频 ID
        limit: 返回数量
    
    Returns:
        评论者列表
    """
    comments = get_comments(video_id, limit=1000)
    
    if not comments:
        return []
    
    # 统计每个评论者的评论数
    commenter_counts = Counter()
    commenter_channels = {}
    
    for comment in comments:
        author_name = comment[3]  # comment[3] 是 author_name 字段
        author_channel_url = comment[4]  # comment[4] 是 author_channel_url 字段
        
        commenter_counts[author_name] += 1
        if author_name not in commenter_channels:
            commenter_channels[author_name] = author_channel_url
    
    # 获取最活跃的评论者
    top_commenters = []
    for author_name, count in commenter_counts.most_common(limit):
        top_commenters.append({
            "author_name": author_name,
            "comment_count": count,
            "channel_url": commenter_channels[author_name]
        })
    
    return top_commenters


def get_most_liked_comments(video_id: str, limit: int = 10) -> List[Dict]:
    """
    获取最多点赞的评论
    
    Args:
        video_id: 视频 ID
        limit: 返回数量
    
    Returns:
        评论列表
    """
    comments = get_comments(video_id, limit=limit)
    
    if not comments:
        return []
    
    # 转换为字典列表
    top_comments = []
    for comment in comments:
        top_comments.append({
            "author_name": comment[3],
            "like_count": comment[5],
            "text": comment[6],
            "published_at": comment[7]
        })
    
    # 按点赞数排序
    top_comments.sort(key=lambda x: x["like_count"], reverse=True)
    
    return top_comments[:limit]
