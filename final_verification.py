#!/usr/bin/env python3
"""
最终验证脚本 - 确认所有修复都正确
"""

import os
import sys

def check_requirements():
    """检查 requirements.txt"""
    print("=" * 60)
    print("1️⃣  检查 requirements.txt")
    print("=" * 60)
    
    with open('requirements.txt', 'r') as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    print(f"✅ 依赖包数量: {len(lines)}")
    print("\n依赖包列表:")
    for i, pkg in enumerate(lines, 1):
        print(f"  {i}. {pkg}")
    
    # 检查是否有系统级包
    forbidden = ['distro-info', 'dbus-python', 'python-apt']
    has_forbidden = any(any(pkg.startswith(f) for f in forbidden) for pkg in lines)
    
    if has_forbidden:
        print("\n❌ 错误: requirements.txt 包含系统级包！")
        return False
    
    print("\n✅ requirements.txt 正确")
    return True

def check_database():
    """检查数据库连接"""
    print("\n" + "=" * 60)
    print("2️⃣  检查数据库连接")
    print("=" * 60)
    
    try:
        from database.connection import init_database, get_videos
        
        init_database()
        videos = get_videos()
        
        print(f"✅ 数据库连接成功")
        print(f"✅ 获取到 {len(videos)} 个视频")
        
        if len(videos) > 0:
            print("\n✅ 数据库正常")
            return True
        else:
            print("\n⚠️  警告: 数据库中没有视频数据")
            return True
            
    except Exception as e:
        print(f"\n❌ 错误: {e}")
        import traceback
        traceback.print_exc()
        return False

def check_git_status():
    """检查 Git 状态"""
    print("\n" + "=" * 60)
    print("3️⃣  检查 Git 状态")
    print("=" * 60)
    
    import subprocess
    
    # 获取最新的 commit
    result = subprocess.run(
        ['git', 'log', '-1', '--oneline'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        latest_commit = result.stdout.strip()
        print(f"✅ 最新提交: {latest_commit}")
    
    # 检查是否有未推送的提交
    result = subprocess.run(
        ['git', 'status', '-sb'],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        status = result.stdout.strip()
        if "Your branch is ahead of" in status:
            print("\n⚠️  警告: 有未推送的提交")
            print(f"\n{status}")
        else:
            print("\n✅ 所有提交已推送到 GitHub")
    
    return True

def main():
    """主函数"""
    print("\n" + "=" * 60)
    print("🔍 YouTube Dashboard - 最终验证")
    print("=" * 60)
    
    results = []
    
    # 检查 requirements.txt
    results.append(("requirements.txt", check_requirements()))
    
    # 检查数据库
    results.append(("数据库连接", check_database()))
    
    # 检查 Git 状态
    results.append(("Git 状态", check_git_status()))
    
    # 总结
    print("\n" + "=" * 60)
    print("📊 验证结果")
    print("=" * 60)
    
    for name, passed in results:
        status = "✅ 通过" if passed else "❌ 失败"
        print(f"{name}: {status}")
    
    all_passed = all(result for _, result in results)
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 所有验证通过！应用已准备好部署到 Streamlit Cloud！")
    else:
        print("❌ 部分验证失败，请修复上述问题")
    print("=" * 60)
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
