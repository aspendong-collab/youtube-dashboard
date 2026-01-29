#!/usr/bin/env python3
"""Streamlit Cloud 环境检查脚本"""

import sys
import os

print("=" * 80)
print("Streamlit Cloud 环境检查")
print("=" * 80)

# 1. 检查 Python 版本
print(f"\n1. Python 版本: {sys.version}")

# 2. 检查依赖包
print("\n2. 检查依赖包:")
packages = ['streamlit', 'pandas', 'plotly', 'requests']
for pkg in packages:
    try:
        mod = __import__(pkg)
        version = getattr(mod, '__version__', 'Unknown')
        print(f"   ✅ {pkg}: {version}")
    except ImportError as e:
        print(f"   ❌ {pkg}: {e}")

# 3. 检查数据库文件
print("\n3. 检查数据库文件:")
db_path = 'youtube_dashboard.db'
if os.path.exists(db_path):
    print(f"   ✅ 数据库文件存在: {db_path}")
    print(f"   文件大小: {os.path.getsize(db_path)} bytes")
else:
    print(f"   ❌ 数据库文件不存在: {db_path}")
    print(f"   当前目录: {os.getcwd()}")

# 4. 检查数据库连接
print("\n4. 检查数据库连接:")
try:
    from database import init_database, get_videos
    init_database()
    videos = get_videos()
    print(f"   ✅ 数据库连接成功")
    print(f"   视频数量: {len(videos)}")
except Exception as e:
    print(f"   ❌ 数据库连接失败: {e}")

# 5. 检查所有模块导入
print("\n5. 检查所有模块导入:")
modules = {
    'database': ['init_database', 'get_videos', 'get_video_info', 'get_latest_stats'],
    'analytics': ['analyze_video_performance', 'create_performance_chart'],
    'ui': ['render_sidebar', 'render_metric_card'],
    'utils': ['format_number', 'calculate_engagement_rate'],
}

for module_name, functions in modules.items():
    try:
        mod = __import__(module_name)
        print(f"   ✅ {module_name}")
        for func_name in functions:
            if hasattr(mod, func_name):
                print(f"      ✅ {func_name}")
            else:
                print(f"      ❌ {func_name} (not found)")
    except Exception as e:
        print(f"   ❌ {module_name}: {e}")

print("\n" + "=" * 80)
print("检查完成")
print("=" * 80)
