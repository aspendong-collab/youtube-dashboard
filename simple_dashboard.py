#!/usr/bin/env python3
"""简化版 Dashboard - 仅测试侧边栏"""

import streamlit as st

# 初始化 session state
if "current_page" not in st.session_state:
    st.session_state.current_page = "video_management"

def main():
    st.set_page_config(
        page_title="YouTube Analytics Dashboard",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 侧边栏
    with st.sidebar:
        st.title("📊 YouTube Analytics")
        
        pages = [
            ("📹 视频管理", "video_management"),
            ("📊 整体看板", "overall_dashboard"),
            ("📹 单个视频", "video_detail"),
            ("🔥 爆款提醒", "alerts"),
        ]
        
        for page_name, page_key in pages:
            if st.button(page_name, key=f"nav_{page_key}", use_container_width=True):
                st.session_state.current_page = page_key
                st.rerun()
    
    # 主内容区
    st.title(f"当前页面: {st.session_state.current_page}")
    st.write("侧边栏正常工作！")
    
    if st.session_state.current_page == "video_management":
        st.write("📹 视频管理页面")
    elif st.session_state.current_page == "overall_dashboard":
        st.write("📊 整体看板页面")
    elif st.session_state.current_page == "video_detail":
        st.write("📹 单个视频页面")
    elif st.session_state.current_page == "alerts":
        st.write("🔥 爆款提醒页面")

if __name__ == "__main__":
    main()
