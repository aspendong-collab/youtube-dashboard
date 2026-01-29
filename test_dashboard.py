#!/usr/bin/env python3
"""
简单的测试 dashboard
"""

import streamlit as st
import sys

# 配置页面
st.set_page_config(
    page_title="Test Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 Test Dashboard")
st.write("如果你能看到这个页面，说明 Streamlit 已经成功启动！")

# 测试数据库
try:
    from database.connection import init_database, get_videos
    
    init_database()
    videos = get_videos()
    
    st.write(f"✅ 数据库连接成功")
    st.write(f"✅ 获取到 {len(videos)} 个视频")
    
    if videos:
        st.write("### 视频列表")
        for video in videos:
            st.write(f"- {video[1]} (ID: {video[0]})")
except Exception as e:
    st.error(f"❌ 错误: {e}")
    import traceback
    st.text(traceback.format_exc())

# 测试导航
if "page" not in st.session_state:
    st.session_state.page = "home"

st.sidebar.title("📊 导航")
if st.sidebar.button("首页"):
    st.session_state.page = "home"
if st.sidebar.button("测试页面"):
    st.session_state.page = "test"

if st.session_state.page == "home":
    st.write("### 首页")
    st.write("这是首页内容")
elif st.session_state.page == "test":
    st.write("### 测试页面")
    st.write("这是测试页面")
