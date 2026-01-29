#!/usr/bin/env python3
"""
部署前验证脚本
在部署到 Streamlit Cloud 之前运行此脚本，确保所有功能正常
"""

import sys
import os

# 添加当前目录到 Python 路径
sys.path.insert(0, os.path.dirname(__file__))

def print_header(text):
    """打印标题"""
    print(f"\n{'=' * 70}")
    print(f"  {text}")
    print('=' * 70)

def print_test(name, passed, details=""):
    """打印测试结果"""
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")
    if details:
        print(f"     {details}")

def main():
    """主验证流程"""
    print_header("🧪 Streamlit Cloud 部署前验证")
    
    all_passed = True
    
    # 测试 1: 文件结构检查
    print("\n[1/8] 检查必要文件...")
    required_files = [
        'dashboard.py',
        'requirements.txt',
        'config.py',
        'database/__init__.py',
        'database/connection.py',
        'api/__init__.py',
        'analytics/__init__.py',
        'ui/__init__.py',
    ]
    
    files_missing = []
    for file in required_files:
        if os.path.exists(file):
            print_test(f"文件存在: {file}", True)
        else:
            print_test(f"文件缺失: {file}", False)
            files_missing.append(file)
            all_passed = False
    
    if files_missing:
        print(f"\n❌ 缺失的文件: {', '.join(files_missing)}")
        return False
    
    # 测试 2: 数据库检查
    print("\n[2/8] 检查数据库...")
    db_exists = os.path.exists('youtube_dashboard.db')
    print_test("数据库文件存在", db_exists)
    
    if not db_exists:
        print("   ⚠️  数据库不存在，应用会在首次运行时自动创建")
    else:
        db_size = os.path.getsize('youtube_dashboard.db')
        print_test(f"数据库文件大小: {db_size / 1024:.2f} KB", db_size > 0)
        if db_size == 0:
            print("   ❌ 数据库文件为空")
            all_passed = False
    
    # 测试 3: 数据库初始化
    print("\n[3/8] 测试数据库初始化...")
    try:
        from database.connection import init_database, get_videos
        init_database()
        videos = get_videos()
        print_test(f"数据库初始化成功", True, f"包含 {len(videos)} 个视频")
        if len(videos) == 0:
            print("   ⚠️  数据库中没有视频数据")
    except Exception as e:
        print_test("数据库初始化失败", False, str(e))
        all_passed = False
    
    # 测试 4: 核心模块导入
    print("\n[4/8] 测试核心模块导入...")
    try:
        from database import connection
        print_test("database.connection 模块", True)
    except Exception as e:
        print_test("database.connection 模块", False, str(e))
        all_passed = False
    
    try:
        from api import youtube_api
        print_test("api.youtube_api 模块", True)
    except Exception as e:
        print_test("api.youtube_api 模块", False, str(e))
        all_passed = False
    
    try:
        from analytics import (
            analyze_video_performance,
            create_performance_chart,
            generate_word_cloud,
        )
        print_test("analytics 模块", True)
    except Exception as e:
        print_test("analytics 模块", False, str(e))
        all_passed = False
    
    # 测试 5: 数据库查询功能
    print("\n[5/8] 测试数据库查询功能...")
    try:
        from database.connection import (
            get_video_info,
            get_latest_stats,
            get_video_stats_history,
        )
        
        if videos:
            video_id = videos[0][0]
            
            # 测试获取视频信息
            info = get_video_info(video_id)
            print_test("获取视频信息", info is not None)
            
            # 测试获取最新统计
            stats = get_latest_stats(video_id)
            print_test("获取最新统计", stats is not None)
            
            # 测试获取历史数据
            history = get_video_stats_history(video_id, days=30)
            print_test("获取历史数据", True, f"{len(history)} 条记录")
    except Exception as e:
        print_test("数据库查询", False, str(e))
        all_passed = False
    
    # 测试 6: Dashboard 主模块
    print("\n[6/8] 测试 Dashboard 主模块...")
    try:
        import dashboard
        print_test("dashboard 模块导入", True)
    except Exception as e:
        print_test("dashboard 模块导入", False, str(e))
        all_passed = False
    
    # 测试 7: requirements.txt
    print("\n[7/8] 验证 requirements.txt...")
    try:
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        required_packages = ['streamlit', 'google-api-python-client', 'pandas', 'plotly']
        packages_found = []
        packages_missing = []
        
        for pkg in required_packages:
            pkg_lower = pkg.lower()
            found = any(pkg_lower in req.lower() for req in requirements)
            if found:
                packages_found.append(pkg)
            else:
                packages_missing.append(pkg)
        
        print_test(f"找到 {len(packages_found)}/{len(required_packages)} 个必需包", len(packages_missing) == 0)
        
        if packages_missing:
            print(f"   ⚠️  缺失的包: {', '.join(packages_missing)}")
            all_passed = False
        
        print(f"   📋 共 {len(requirements)} 个依赖包")
    except Exception as e:
        print_test("读取 requirements.txt", False, str(e))
        all_passed = False
    
    # 测试 8: 分析功能
    print("\n[8/8] 测试分析功能...")
    try:
        if videos:
            video_id = videos[0][0]
            stats = analyze_video_performance(video_id)
            print_test("视频性能分析", True, f"观看数: {stats.get('views', 0)}")
    except Exception as e:
        print_test("视频性能分析", False, str(e))
        all_passed = False
    
    # 总结
    print_header("验证结果")
    
    if all_passed:
        print("\n✅ 所有测试通过！")
        print("\n🎉 应用已准备好部署到 Streamlit Cloud！")
        print("\n下一步：")
        print("   1. 确保代码已推送到 GitHub")
        print("   2. 访问 https://share.streamlit.io")
        print("   3. 点击 'New app' 并选择你的仓库")
        print("   4. 配置 Main file path 为 'dashboard.py'")
        print("   5. 点击 'Deploy'")
        print("\n详细部署说明请参阅: DEPLOY_INSTRUCTIONS.md")
        return 0
    else:
        print("\n❌ 部分测试失败")
        print("\n请修复上述问题后再部署")
        print("\n常见问题：")
        print("   - 检查数据库文件是否正确上传")
        print("   - 确认 requirements.txt 包含所有必需的包")
        print("   - 查看错误日志获取详细信息")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
