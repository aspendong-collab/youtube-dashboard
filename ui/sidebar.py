"""
侧边栏组件
自定义侧边栏导航，实现可点击变色的效果
"""

import streamlit as st
from .styles import get_custom_styles, get_sidebar_styles


def render_sidebar():
    """渲染自定义侧边栏"""
    
    # 应用自定义样式
    st.markdown(get_custom_styles(), unsafe_allow_html=True)
    st.markdown(get_sidebar_styles(), unsafe_allow_html=True)
    
    # 初始化当前页面
    if "current_page" not in st.session_state:
        st.session_state.current_page = "video_management"
    
    # 使用 st.sidebar 的 radio 组件，但通过 CSS 隐藏默认样式
    # 侧边栏标题
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1.5rem 0 1rem 0;">
        <h2 style="font-size: 1.5rem; font-weight: 700; margin: 0; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">
            📊 YouTube Analytics
        </h2>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("<div style='border-bottom: 1px solid rgba(255,255,255,0.1); margin: 1rem 0;'></div>", unsafe_allow_html=True)
    
    # 自定义导航选项
    pages = [
        {"group": "📊 仪表盘", "pages": [
            ("📹 视频管理", "video_management"),
            ("📊 整体看板", "overall_dashboard"),
            ("📹 单个视频", "video_detail"),
            ("🔥 爆款提醒", "alerts"),
        ]},
        {"group": "📈 数据分析", "pages": [
            ("🎯 SEO 优化", "seo_analysis"),
            ("⏱️ 时长分析", "duration_analysis"),
            ("🕐 发布时间", "publish_time"),
            ("🏷️ 标签分析", "tags_analysis"),
        ]},
        {"group": "💬 深度分析", "pages": [
            ("😊 情感分析", "sentiment_analysis"),
            ("👥 用户画像", "user_profile"),
            ("🔍 评论分析", "comment_analysis"),
        ]},
        {"group": "⚙️ 设置", "pages": [
            ("🔑 API 配置", "api_settings"),
            ("📊 数据源管理", "data_source"),
        ]}
    ]
    
    # 渲染导航
    for group in pages:
        # 分组标题
        st.sidebar.markdown(f"""
        <div style="font-size: 0.75rem; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #8892b0; margin: 1.5rem 0 0.5rem 0; padding: 0 1rem;">
            {group["group"]}
        </div>
        """, unsafe_allow_html=True)
        
        # 页面选项
        for page_name, page_key in group["pages"]:
            # 判断是否是当前页面
            is_active = st.session_state.current_page == page_key
            
            # 根据激活状态设置样式
            if is_active:
                bg_style = "linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
                border_style = "transparent"
                icon_color = "#ffffff"
                text_color = "#ffffff"
                transform = "none"
            else:
                bg_style = "rgba(255, 255, 255, 0.05)"
                border_style = "rgba(255, 255, 255, 0.1)"
                icon_color = "#8892b0"
                text_color = "#b8c1ec"
                transform = "translateX(4px)"
            
            # 使用 button 来实现导航
            button_key = f"nav_{page_key}"
            if st.sidebar.button(
                page_name,
                key=button_key,
                use_container_width=True,
                help=f"跳转到{page_name}",
            ):
                st.session_state.current_page = page_key
                st.rerun()
    
    # 底部提示
    st.sidebar.markdown("<div style='border-bottom: 1px solid rgba(255,255,255,0.1); margin: 2rem 0;'></div>", unsafe_allow_html=True)
    
    st.sidebar.markdown("""
    <div style="padding: 1rem; margin-top: 1rem; background: rgba(102, 126, 234, 0.1); border-radius: 8px; border: 1px solid rgba(255,255,255,0.1);">
        <p style="font-size: 0.85rem; color: #b8c1ec; margin: 0 0 0.5rem 0;">
            💡 <strong>使用提示</strong>
        </p>
        <ul style="font-size: 0.85rem; color: #8892b0; margin: 0; padding-left: 1.5rem;">
            <li>在"视频管理"添加视频</li>
            <li>实时获取数据（1-2秒）</li>
            <li>查看深度分析报告</li>
            <li>优化内容策略</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    return st.session_state.current_page


def get_current_page():
    """获取当前选中的页面"""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "video_management"
    return st.session_state.current_page


def set_current_page(page):
    """设置当前页面"""
    st.session_state.current_page = page
    st.rerun()

