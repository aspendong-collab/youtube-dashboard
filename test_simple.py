#!/usr/bin/env python3
"""简化版测试 - 验证侧边栏"""

import streamlit as st
from ui import render_sidebar
from database import init_database

# 初始化数据库
init_database()

# 主函数
def main():
    st.set_page_config(
        page_title="YouTube Analytics Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 渲染侧边栏
    current_page = render_sidebar()
    
    # 显示当前页面
    st.title(f"当前页面: {current_page}")
    st.write("侧边栏加载成功！")
    
    # 显示 session state
    st.write("Session State:", st.session_state)

if __name__ == "__main__":
    main()
