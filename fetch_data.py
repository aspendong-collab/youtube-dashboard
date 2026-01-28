#!/usr/bin/env python3
"""
YouTube 数据更新脚本
从 YouTube API 获取视频数据并存储到数据库
"""

import requests
import sqlite3
from datetime import datetime, timedelta
import os


# ==================== 配置 ====================

def get_api_key():
    """获取 YouTube API Key"""
    # 尝试从环境变量获取
    api_key = os.getenv('COZE_YOUTUBE_DATA_API_7600312097678868486')
    if not api_key:
        # 尝试从另一个环境变量获取（GitHub Actions）
        api_key = os.getenv('YOUTUBE_API_KEY')
    if not api_key:
        raise ValueError("请设置 YouTube API Key！\n\n在 Streamlit Cloud：Settings → Secrets\n在 GitHub：Settings → Secrets and variables → Actions")
    return api_key


# ==================== YouTube API ====================

def fetch_video_info(api_key, video_id):
    """从 YouTube API 获取视频信息"""
    url = f"https://www.googleapis.com/youtube/v3/videos?part=snippet,contentDetails,statistics&id={video_id}&key={api_key}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        if 'items' not in data or len(data['items']) == 0:
            raise Exception(f"视频 {video_id} 不存在或无法访问")

        video_data = data['items'][0]

        # 提取数据
        snippet = video_data.get('snippet', {})
        statistics = video_data.get('statistics', {})

        return {
            'video_id': video_id,
            'title': snippet.get('title', '未知'),
            'channel_title': snippet.get('channelTitle', '未知'),
            'published_at': snippet.get('publishedAt'),
            'view_count': int(statistics.get('viewCount', 0)),
            'like_count': int(statistics.get('likeCount', 0)),
            'comment_count': int(statistics.get('commentCount', 0)),
        }
    except requests.exceptions.RequestException as e:
        raise Exception(f"网络请求失败: {str(e)}")
    except Exception as e:
        raise Exception(f"获取视频信息失败: {str(e)}")


def fetch_video_comments(api_key, video_id, max_comments=100):
    """获取视频评论"""
    url = f"https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&videoId={video_id}&maxResults={max_comments}&order=relevance&key={api_key}"

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        data = response.json()

        if 'items' not in data or len(data['items']) == 0:
            return []

        comments = []
        for item in data['items']:
            snippet = item['snippet']['topLevelComment']['snippet']
            comment_text = snippet.get('textDisplay', '').strip()
            if comment_text and len(comment_text) > 2:  # 过滤太短的评论
                comments.append(comment_text)

        return comments
    except Exception as e:
        print(f"  ⚠️ 获取评论失败: {e}")
        return []


# ==================== 数据库操作 ====================

def get_connection():
    """获取数据库连接"""
    conn = sqlite3.connect('youtube_dashboard.db')
    conn.row_factory = sqlite3.Row
    return conn


def save_comments_to_db(cursor, video_id, comments):
    """保存评论到数据库"""
    # 先删除旧评论
    cursor.execute('DELETE FROM video_comments WHERE video_id = ?', (video_id,))

    # 插入新评论
    for comment in comments:
        cursor.execute('''
            INSERT INTO video_comments (video_id, comment_text, fetched_at)
            VALUES (?, ?, ?)
        ''', (video_id, comment, datetime.now()))


def update_video_data(conn, video_data, api_key, update_time):
    """更新视频数据到数据库"""
    cursor = conn.cursor()

    # 更新视频基本信息
    cursor.execute('''
        UPDATE videos
        SET title = ?, channel_title = ?
        WHERE video_id = ?
    ''', (video_data['title'], video_data['channel_title'], video_data['video_id']))

    # 检查今天是否已有数据
    today = datetime.now().strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT id FROM video_stats
        WHERE video_id = ? AND date = ?
    ''', (video_data['video_id'], today))

    existing = cursor.fetchone()

    # 计算互动率
    if video_data['view_count'] > 0:
        engagement_rate = ((video_data['like_count'] + video_data['comment_count']) / video_data['view_count']) * 100
    else:
        engagement_rate = 0

    # 获取昨天的数据用于计算增长
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    cursor.execute('''
        SELECT view_count FROM video_stats
        WHERE video_id = ? AND date = ?
    ''', (video_data['video_id'], yesterday))

    yesterday_stats = cursor.fetchone()
    yesterday_views = yesterday_stats['view_count'] if yesterday_stats else 0

    # 计算今日增长
    today_growth = video_data['view_count'] - yesterday_views

    if existing:
        # 更新今天的数据
        cursor.execute('''
            UPDATE video_stats
            SET view_count = ?, like_count = ?, comment_count = ?, engagement_rate = ?, fetch_time = ?
            WHERE video_id = ? AND date = ?
        ''', (
            video_data['view_count'],
            video_data['like_count'],
            video_data['comment_count'],
            engagement_rate,
            datetime.now(),
            video_data['video_id'],
            today
        ))
    else:
        # 插入新的数据
        cursor.execute('''
            INSERT INTO video_stats (video_id, date, view_count, like_count, comment_count, engagement_rate, fetch_time)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            video_data['video_id'],
            today,
            video_data['view_count'],
            video_data['like_count'],
            video_data['comment_count'],
            engagement_rate,
            datetime.now()
        ))

    # 检查预警（传入更新时间和今日增长）
    check_alerts(cursor, video_data, engagement_rate, update_time, today_growth)

    # 获取评论
    comments = fetch_video_comments(api_key, video_data['video_id'])

    # 保存评论到数据库
    save_comments_to_db(cursor, video_data['video_id'], comments)

    conn.commit()
    return engagement_rate, comments


def check_alerts(cursor, video_data, engagement_rate, update_time, today_growth):
    """检查是否需要发送预警"""
    today = datetime.now().strftime('%Y-%m-%d')

    # 获取更新时间的小时
    update_hour = update_time.hour

    # 根据更新时间确定阈值
    if update_hour == 9:  # 9:00 更新
        growth_threshold = 10000  # 增长 1 万
    elif update_hour == 12:  # 12:00 更新
        growth_threshold = 30000  # 增长 3 万
    elif update_hour == 18:  # 18:00 更新
        growth_threshold = 50000  # 增长 5 万
    else:
        growth_threshold = 0  # 其他时间不检查增长预警

    # 检查今日增长预警
    if growth_threshold > 0 and today_growth >= growth_threshold:
        # 检查今天是否已经发送过该类型的增长预警
        cursor.execute('''
            SELECT id FROM alerts
            WHERE video_id = ? AND alert_type = ? AND DATE(sent_at) = ?
        ''', (video_data['video_id'], f'growth_{growth_threshold}', today))

        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO alerts (video_id, alert_type, current_value, message, title)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                video_data['video_id'],
                f'growth_{growth_threshold}',
                today_growth,
                f"🔥 爆款提醒！视频「{video_data['title']}」今日播放量增长 {today_growth:,}！",
                video_data['title']
            ))

    # 10万播放预警（任何时候）
    if video_data['view_count'] >= 100000:
        # 检查是否已经发送过 10万预警
        cursor.execute('''
            SELECT id FROM alerts
            WHERE video_id = ? AND alert_type = '100k'
        ''', (video_data['video_id']))

        if not cursor.fetchone():
            cursor.execute('''
                INSERT INTO alerts (video_id, alert_type, current_value, message, title)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                video_data['video_id'],
                '100k',
                video_data['view_count'],
                f"🔥 爆款提醒！视频「{video_data['title']}」播放量突破 10 万！",
                video_data['title']
            ))


def check_data_anomaly(cursor, video_data):
    """检查数据异常（视频发布次日播放量低于5000）"""
    # 解析发布时间
    published_at = datetime.fromisoformat(video_data['published_at'].replace('Z', '+00:00'))
    
    # 计算发布后的第二天
    day_after_publish = (published_at + timedelta(days=1)).date()
    today = datetime.now().date()
    
    # 检查是否是发布后的第二天
    if today == day_after_publish:
        # 检查今日播放量
        today_stats = datetime.now().strftime('%Y-%m-%d')
        cursor.execute('''
            SELECT view_count FROM video_stats
            WHERE video_id = ? AND date = ?
        ''', (video_data['video_id'], today_stats))
        
        stats = cursor.fetchone()
        if stats and stats['view_count'] < 5000:
            # 检查今天是否已经发送过数据异常预警
            cursor.execute('''
                SELECT id FROM alerts
                WHERE video_id = ? AND alert_type = 'data_anomaly' AND DATE(sent_at) = ?
            ''', (video_data['video_id'], today_stats))
            
            if not cursor.fetchone():
                cursor.execute('''
                    INSERT INTO alerts (video_id, alert_type, current_value, message, title)
                    VALUES (?, ?, ?, ?, ?)
                ''', (
                    video_data['video_id'],
                    'data_anomaly',
                    stats['view_count'],
                    f"⚠️ 数据异常提醒！视频「{video_data['title']}」发布次日播放量仅 {stats['view_count']:,}，可能需要关注！",
                    video_data['title']
                ))


# ==================== 主程序 ====================

def main():
    """主函数"""
    print("=" * 50)
    print("YouTube 数据更新脚本")
    print("=" * 50)
    print(f"开始时间: {datetime.now()}")
    print()

    # 获取 API Key
    try:
        api_key = get_api_key()
        print(f"✅ API Key 已获取")
    except Exception as e:
        print(f"❌ 错误: {e}")
        return

    # 连接数据库
    conn = get_connection()
    print(f"✅ 数据库已连接")

    # 获取所有活跃视频
    cursor = conn.cursor()
    cursor.execute('SELECT video_id FROM videos WHERE is_active = 1')
    videos = cursor.fetchall()

    if not videos:
        print("⚠️ 暂无活跃视频，请先在 dashboard 中添加")
        conn.close()
        return

    print(f"✅ 找到 {len(videos)} 个活跃视频")
    print()

    # 更新每个视频的数据
    update_time = datetime.now()
    success_count = 0
    error_count = 0

    for i, video in enumerate(videos, 1):
        video_id = video['video_id']
        print(f"[{i}/{len(videos)}] 正在获取视频 {video_id} 的数据...")

        try:
            # 获取视频信息
            video_data = fetch_video_info(api_key, video_id)

            # 更新数据库（传入 api_key 和 update_time）
            engagement_rate, comments = update_video_data(conn, video_data, api_key, update_time)

            # 检查数据异常
            check_data_anomaly(cursor, video_data)

            print(f"  ✅ {video_data['title']}")
            print(f"     播放量: {video_data['view_count']:,}")
            print(f"     点赞数: {video_data['like_count']:,}")
            print(f"     评论数: {video_data['comment_count']:,}")
            print(f"     互动率: {engagement_rate:.2f}%")
            print(f"     评论数: {len(comments)}")
            print()

            success_count += 1

        except Exception as e:
            print(f"  ❌ 错误: {e}")
            print()
            error_count += 1
            continue

    # 关闭数据库
    conn.close()

    # 打印总结
    print("=" * 50)
    print("更新完成")
    print(f"✅ 成功: {success_count}")
    print(f"❌ 失败: {error_count}")
    print(f"结束时间: {datetime.now()}")
    print("=" * 50)


if __name__ == '__main__':
    main()
