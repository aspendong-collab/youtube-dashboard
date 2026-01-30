#!/usr/bin/env python3
"""
测试 dashboard.py 的基本功能
"""

import sys
import traceback

def test_imports():
    """测试所有导入"""
    try:
        import streamlit as st
        print("✅ streamlit 导入成功")
    except Exception as e:
        print(f"❌ streamlit 导入失败: {e}")
        return False
    
    try:
        import pandas as pd
        print("✅ pandas 导入成功")
    except Exception as e:
        print(f"❌ pandas 导入失败: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ plotly 导入成功")
    except Exception as e:
        print(f"❌ plotly 导入失败: {e}")
        return False
    
    return True

def test_custom_modules():
    """测试自定义模块导入"""
    try:
        from ui import render_sidebar
        print("✅ ui 模块导入成功")
    except Exception as e:
        print(f"❌ ui 模块导入失败: {e}")
        traceback.print_exc()
        return False
    
    try:
        from database import init_database, get_videos
        print("✅ database 模块导入成功")
    except Exception as e:
        print(f"❌ database 模块导入失败: {e}")
        traceback.print_exc()
        return False
    
    try:
        from api import YouTubeAPI
        print("✅ api 模块导入成功")
    except Exception as e:
        print(f"❌ api 模块导入失败: {e}")
        traceback.print_exc()
        return False
    
    try:
        from analytics import create_performance_chart
        print("✅ analytics 模块导入成功")
    except Exception as e:
        print(f"❌ analytics 模块导入失败: {e}")
        traceback.print_exc()
        return False
    
    try:
        from utils import format_number
        print("✅ utils 模块导入成功")
    except Exception as e:
        print(f"❌ utils 模块导入失败: {e}")
        traceback.print_exc()
        return False
    
    try:
        from config import Config
        print("✅ config 模块导入成功")
    except Exception as e:
        print(f"❌ config 模块导入失败: {e}")
        traceback.print_exc()
        return False
    
    return True

def test_database():
    """测试数据库"""
    try:
        from database import init_database, get_videos
        init_database()
        videos = get_videos()
        print(f"✅ 数据库连接成功，共有 {len(videos)} 个视频")
        return True
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        traceback.print_exc()
        return False

def main():
    """主函数"""
    print("=" * 60)
    print("开始测试 dashboard.py 的依赖...")
    print("=" * 60)
    
    # 测试基本导入
    print("\n[1/3] 测试基本导入...")
    if not test_imports():
        print("\n❌ 基本导入测试失败")
        sys.exit(1)
    
    # 测试自定义模块
    print("\n[2/3] 测试自定义模块导入...")
    if not test_custom_modules():
        print("\n❌ 自定义模块导入测试失败")
        sys.exit(1)
    
    # 测试数据库
    print("\n[3/3] 测试数据库...")
    if not test_database():
        print("\n❌ 数据库测试失败")
        sys.exit(1)
    
    print("\n" + "=" * 60)
    print("✅ 所有测试通过！dashboard.py 应该可以正常运行")
    print("=" * 60)

if __name__ == "__main__":
    main()
