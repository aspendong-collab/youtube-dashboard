#!/usr/bin/env python3
"""测试 render_video_detail 函数"""

import sys
from database import init_database, get_videos, get_video_info, get_latest_stats
from analytics import create_performance_chart, generate_optimization_suggestions

init_database()
videos = get_videos()

print(f"找到 {len(videos)} 个视频\n")

# 测试第一个视频
video = videos[0]
video_id = video[0]
video_title = video[1]

print(f"测试视频: {video_title}")
print(f"Video ID: {video_id}\n")

# 获取视频信息
print("1. 获取视频信息...")
video_info = get_video_info(video_id)
if video_info:
    print(f"✅ 成功获取视频信息")
    print(f"   - 标题: {video_info.get('title', 'N/A')}")
    print(f"   - 频道: {video_info.get('channel_title', 'N/A')}")
else:
    print("❌ 未找到视频信息")
    sys.exit(1)

# 获取最新统计
print("\n2. 获取最新统计...")
latest_stats = get_latest_stats(video_id)
if latest_stats:
    print(f"✅ 成功获取最新统计")
    print(f"   - 观看量: {latest_stats.get('view_count', 0)}")
    print(f"   - 点赞量: {latest_stats.get('like_count', 0)}")
    print(f"   - 评论量: {latest_stats.get('comment_count', 0)}")
else:
    print("⚠️  未找到统计数据")

# 创建数据趋势图
print("\n3. 创建数据趋势图...")
try:
    from database import get_video_stats_history
    history = get_video_stats_history(video_id, days=30)
    print(f"   历史数据: {len(history)} 条")
    
    fig = create_performance_chart(video_id, days=30)
    print(f"✅ 成功创建图表: {type(fig)}")
except Exception as e:
    print(f"❌ 创建图表失败: {e}")
    import traceback
    traceback.print_exc()

# 生成优化建议
print("\n4. 生成优化建议...")
try:
    suggestions = generate_optimization_suggestions(video_id)
    if suggestions:
        print(f"✅ 成功生成建议: {len(suggestions)} 条")
        for i, sugg in enumerate(suggestions[:3], 1):
            print(f"   {i}. {sugg}")
    else:
        print("⚠️  没有生成建议")
except Exception as e:
    print(f"⚠️  生成建议失败: {e}")

print("\n✅ 所有测试完成")
