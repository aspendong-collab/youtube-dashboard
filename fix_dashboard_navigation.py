#!/usr/bin/env python3
"""修复 dashboard 导航问题"""

import re

# 读取文件
with open('dashboard.py', 'r') as f:
    content = f.read()

# 在每个页面函数的开头添加导航提示
# 查找所有 "def render_" 函数

functions_to_update = [
    'render_overall_dashboard',
    'render_video_detail',
    'render_alerts',
    'render_seo_analysis',
    'render_duration_analysis',
    'render_publish_time_analysis',
    'render_tags_analysis',
    'render_sentiment_analysis',
    'render_user_profile',
    'render_comment_analysis',
    'render_api_settings',
    'render_data_source',
]

for func_name in functions_to_update:
    # 查找函数定义
    pattern = rf'(def {func_name}\([^)]*\):\s*""""[^"]*"""[^\n]*\n)'
    
    # 检查是否已经有导航提示
    navigation_hint = '    # 导航提示\n    st.info("""💡 **导航提示**\n    \n    - 使用左侧导航栏切换页面\n    - 返回主页点击"视频管理"或"整体看板"\n    """, icon="🧭")\n    \n    st.markdown("---")\n'
    
    # 在函数定义后添加导航提示
    def_pattern = rf'(def {func_name}\([^)]*\):\s*""""[^"]*"""[^\n]*\n)'
    
    def replacement = r'\1' + navigation_hint
    
    # 只在函数体为空或只有占位符时添加
    if "功能开发中" in content or "此功能正在开发中" in content:
        content = re.sub(def_pattern, replacement, content)

# 写回文件
with open('dashboard.py', 'w') as f:
    f.write(content)

print("✅ 已添加导航提示到所有页面")
