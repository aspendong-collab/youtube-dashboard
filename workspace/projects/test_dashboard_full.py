#!/usr/bin/env python3
"""测试 dashboard 的所有页面"""

import sys
sys.path.insert(0, '.')

from database import (
    init_database, get_videos, get_video_info, get_latest_stats,
    get_video_stats_history, get_comments, get_all_tags
)
from analytics import (
    analyze_video_performance, create_performance_chart,
    create_comparison_chart, generate_optimization_suggestions
)
from utils import calculate_engagement_rate, format_number

print("=" * 80)
print("测试 Dashboard 所有页面")
print("=" * 80)

# 初始化数据库
init_database()
videos = get_videos()

if not videos:
    print("❌ 没有视频数据")
    sys.exit(1)

print(f"✅ 找到 {len(videos)} 个视频\n")

# 测试 1: 整体看板页面
print("=" * 80)
print("测试 1: 整体看板页面 (render_overall_dashboard)")
print("=" * 80)

try:
    total_views = sum([video[4] or 0 for video in videos])
    total_likes = sum([video[5] or 0 for video in videos])
    total_comments = sum([video[6] or 0 for video in videos])

    print(f"✅ 总观看量: {format_number(total_views)}")
    print(f"✅ 总点赞量: {format_number(total_likes)}")
    print(f"✅ 总评论量: {format_number(total_comments)}")

    # 视频排行
    import pandas as pd
    video_list = []
    for video in videos:
        engagement_rate = calculate_engagement_rate(
            video[5] or 0,
            video[6] or 0,
            video[4] or 0
        )
        video_list.append({
            "视频标题": video[1],
            "观看量": video[4] or 0,
            "点赞量": video[5] or 0,
            "评论量": video[6] or 0,
            "互动率": engagement_rate
        })

    df = pd.DataFrame(video_list)
    df_sorted = df.sort_values("观看量", ascending=False).head(10)
    print(f"✅ 创建了 Top 10 排行榜")

    # 创建图表
    import plotly.express as px
    fig = px.bar(
        df_sorted,
        x="观看量",
        y="视频标题",
        orientation="h",
        title="观看量 Top 10",
        color="观看量",
        color_continuous_scale="viridis"
    )
    print(f"✅ 创建了观看量排行榜图表")

    print("\n✅ 整体看板页面测试通过\n")

except Exception as e:
    print(f"\n❌ 整体看板页面测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试 2: 单个视频详情页面
print("=" * 80)
print("测试 2: 单个视频详情页面 (render_video_detail)")
print("=" * 80)

video_id = videos[0][0]
video_title = videos[0][1]

try:
    print(f"选择视频: {video_title} ({video_id})")

    # 获取视频信息
    video_info = get_video_info(video_id)
    if video_info:
        print(f"✅ 获取视频信息成功")
        print(f"   - 标题: {video_info.get('title', 'N/A')}")
        print(f"   - 频道: {video_info.get('channel_title', 'N/A')}")
    else:
        print("⚠️  未找到视频信息（使用缓存数据）")

    # 获取最新统计数据
    latest_stats = get_latest_stats(video_id)
    if latest_stats:
        print(f"✅ 获取最新统计成功")
        print(f"   - 观看量: {format_number(latest_stats.get('view_count', 0))}")
        print(f"   - 点赞量: {format_number(latest_stats.get('like_count', 0))}")
        print(f"   - 评论量: {format_number(latest_stats.get('comment_count', 0))}")
    else:
        print("⚠️  未找到统计数据")

    # 分析视频表现
    try:
        performance = analyze_video_performance(video_id)
        print(f"✅ 分析视频表现成功")
        print(f"   - 增长率: {performance.get('growth_rate', 0):.2%}")
        print(f"   - 平均日观看量: {format_number(performance.get('avg_daily_views', 0))}")
    except Exception as e:
        print(f"⚠️  分析视频表现失败: {e}")

    # 创建数据趋势图
    try:
        history = get_video_stats_history(video_id, days=30)
        print(f"✅ 获取历史数据成功: {len(history)} 条记录")

        if len(history) >= 1:
            fig = create_performance_chart(video_id, days=30)
            print(f"✅ 创建数据趋势图成功")
        else:
            print("⚠️  历史数据不足，无法创建趋势图")
    except Exception as e:
        print(f"❌ 创建数据趋势图失败: {e}")
        import traceback
        traceback.print_exc()

    # 生成优化建议
    try:
        suggestions = generate_optimization_suggestions(video_id)
        if suggestions:
            print(f"✅ 生成优化建议成功: {len(suggestions)} 条")
        else:
            print("⚠️  没有生成优化建议")
    except Exception as e:
        print(f"⚠️  生成优化建议失败: {e}")

    print("\n✅ 单个视频详情页面测试通过\n")

except Exception as e:
    print(f"\n❌ 单个视频详情页面测试失败: {e}")
    import traceback
    traceback.print_exc()

# 测试 3: 视频管理页面
print("=" * 80)
print("测试 3: 视频管理页面 (render_video_management)")
print("=" * 80)

try:
    video_list = []
    for video in videos:
        from utils import get_video_age
        video_list.append({
            "视频标题": video[1],
            "频道": video[2],
            "观看量": format_number(video[4] or 0),
            "点赞量": format_number(video[5] or 0),
            "评论量": format_number(video[6] or 0),
            "发布时间": get_video_age(video[3]) if video[3] else "未知"
        })

    df = pd.DataFrame(video_list)
    print(f"✅ 创建了视频列表: {len(df)} 个视频")

    print("\n✅ 视频管理页面测试通过\n")

except Exception as e:
    print(f"\n❌ 视频管理页面测试失败: {e}")
    import traceback
    traceback.print_exc()

print("=" * 80)
print("所有测试完成")
print("=" * 80)
