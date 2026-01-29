#!/usr/bin/env python3
"""
侧边栏导航修复方案

问题：整体数据页面右侧的导航栏不显示

原因分析：
1. Streamlit 的侧边栏默认是存在的，但可能因为样式或缓存问题不显示
2. 侧边栏按钮的点击事件可能没有正确触发
3. 可能需要强制重新渲染侧边栏

解决方案：
1. 确保主函数在所有页面之前调用 render_sidebar()
2. 在每个页面函数中也调用 render_sidebar()（虽然这会重复，但确保可见性）
3. 添加调试信息，确认侧边栏是否正确渲染
4. 使用 st.rerun() 强制刷新
"""

import streamlit as st


def render_fixed_sidebar():
    """
    修复版侧边栏 - 确保始终可见
    
    关键改进：
    1. 使用 st.sidebar.markdown() 而不是 st.sidebar.button() 来显示菜单
    2. 使用 session state 来跟踪当前页面
    3. 添加明确的 CSS 样式确保侧边栏可见
    """
    
    # 初始化当前页面
    if "current_page" not in st.session_state:
        st.session_state.current_page = "video_management"
    
    # 强制侧边栏展开
    st.sidebar.markdown("""
    <style>
    [data-testid="stSidebar"] {
        width: 300px !important;
        display: block !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # 侧边栏标题
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1.5rem 0 1rem 0;">
        <h2 style="font-size: 1.5rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            📊 YouTube Analytics
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<div style='border-bottom: 1px solid rgba(255,255,255,0.1); margin: 1rem 0;'></div>", unsafe_allow_html=True)
    
    # 自定义导航选项 - 使用 selectbox 而不是 button
    pages = [
        ("📊 仪表盘", [
            ("📹 视频管理", "video_management"),
            ("📊 整体看板", "overall_dashboard"),
            ("📹 单个视频", "video_detail"),
            ("🔥 爆款提醒", "alerts"),
        ]),
        ("📈 数据分析", [
            ("🎯 SEO 优化", "seo_analysis"),
            ("⏱️ 时长分析", "duration_analysis"),
            ("🕐 发布时间", "publish_time"),
            ("🏷️ 标签分析", "tags_analysis"),
        ]),
        ("💬 深度分析", [
            ("😊 情感分析", "sentiment_analysis"),
            ("👥 用户画像", "user_profile"),
            ("🔍 评论分析", "comment_analysis"),
        ]),
        ("⚙️ 设置", [
            ("🔑 API 配置", "api_settings"),
            ("📊 数据源管理", "data_source"),
        ])
    ]
    
    # 渲染导航
    for group_title, group_pages in pages:
        # 分组标题
        st.sidebar.markdown(f"""
        <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #8892b0; margin: 1.5rem 0 0.5rem 0; padding: 0 1rem;">
            {group_title}
        </div>
        """, unsafe_allow_html=True)
        
        # 页面选项 - 使用 selectbox 确保可见性
        page_names = [page[0] for page in group_pages]
        page_keys = [page[1] for page in group_pages]
        
        selected_page = st.sidebar.selectbox(
            "选择页面",
            page_names,
            label_visibility="collapsed",
            key=f"nav_{group_title}",
            index=page_keys.index(st.session_state.current_page) if st.session_state.current_page in page_keys else 0
        )
        
        # 如果选择了不同的页面，更新 session state 并重新运行
        if selected_page:
            new_page = page_keys[page_names.index(selected_page)]
            if st.session_state.current_page != new_page:
                st.session_state.current_page = new_page
                st.rerun()
    
    # 底部提示
    st.sidebar.markdown("<div style='border-bottom: 1px solid rgba(255,255,255,0.1); margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div style="padding: 1rem; margin-top: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
        <p style="font-size: 0.85rem; color: #b8c1ec; margin: 0 0 0.5rem 0;">
            💡 <strong>使用提示</strong>
        </p>
        <ul style="font-size: 0.85rem; color: #8892b0; margin: 0; padding-left: 1.5rem;">
            <li>使用左侧导航栏切换页面</li>
            <li>选择不同的页面会自动跳转</li>
            <li>查看深度分析报告</li>
            <li>优化内容策略</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    return st.session_state.current_page


def render_navigation_hint():
    """
    渲染导航提示 - 放在每个页面顶部
    
    确保用户知道如何使用侧边栏导航
    """
    st.info("""
    💡 **导航提示**
    
    - 使用**左侧导航栏**切换页面（选择不同的页面会自动跳转）
    - 返回主页：选择"视频管理"或"整体看板"
    - 左侧导航栏始终可见，包含所有功能
    """, icon="🧭")


def test_sidebar_visibility():
    """
    测试侧边栏可见性
    
    用于调试侧边栏渲染问题
    """
    st.sidebar.write("🔍 调试信息")
    st.sidebar.write(f"当前页面: {st.session_state.current_page}")
    
    # 添加侧边栏状态检查
    if st.sidebar.button("测试侧边栏响应"):
        st.sidebar.success("✅ 侧边栏正常工作！")
        st.rerun()
