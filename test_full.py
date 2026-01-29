#!/usr/bin/env python3
"""测试 dashboard 的所有页面"""

import sys
from database import (
    init_database, get_videos, get_latest_stats, get_video_stats_history
)
from analytics import create_performance_chart

print("测试 Dashboard")

init_database()
videos = get_videos()
video_id = videos[0][0]

print(f"测试视频: {video_id}")

# 测试创建图表
try:
    history = get_video_stats_history(video_id, days=30)
    print(f"历史数据: {len(history)} 条")
    
    fig = create_performance_chart(video_id, days=30)
    print(f"✅ 图表创建成功: {type(fig)}")
except Exception as e:
    print(f"❌ 错误: {e}")
    import traceback
    traceback.print_exc()
