#!/usr/bin/env python3
"""更新视频缩略图 URL"""

import sys
from database import init_database, get_videos, get_video_info, get_db_connection

def generate_thumbnail_url(video_id):
    """生成 YouTube 视频缩略图 URL"""
    # YouTube 标准缩略图格式: https://img.youtube.com/vi/<video_id>/maxresdefault.jpg
    return f"https://img.youtube.com/vi/{video_id}/maxresdefault.jpg"

def main():
    print("开始更新视频缩略图 URL...")
    
    # 初始化数据库
    init_database()
    
    # 获取所有视频
    videos = get_videos()
    print(f"找到 {len(videos)} 个视频\n")
    
    # 更新每个视频的缩略图
    updated_count = 0
    
    with get_db_connection() as conn:
        cursor = conn.cursor()
        
        for video in videos:
            video_id = video[0]
            video_title = video[1]
            
            # 生成缩略图 URL
            thumbnail_url = generate_thumbnail_url(video_id)
            
            # 更新数据库
            cursor.execute("""
                UPDATE videos
                SET thumbnail_url = ?
                WHERE video_id = ?
            """, (thumbnail_url, video_id))
            
            updated_count += 1
            print(f"✅ {updated_count}. {video_title[:40]}... -> {thumbnail_url}")
        
        # 提交更改
        conn.commit()
    
    print(f"\n✅ 成功更新 {updated_count} 个视频的缩略图 URL")

if __name__ == "__main__":
    main()
