"""UI组件 - 侧边栏"""

import streamlit as st


def render_sidebar():
    """渲染自定义侧边栏"""
    
    # 初始化当前页面
    if "current_page" not in st.session_state:
        st.session_state.current_page = "overview"
    
    # 侧边栏标题
    st.sidebar.write("📊 YouTube Analytics")
    
    # 终极精简导航结构（5 个主页面）
    pages = [
        {"group": "主功能", "pages": [
            ("📊 数据概览", "overview"),
            ("📹 视频管理", "video_management"),
            ("📈 深度分析", "deep_analysis"),
            ("⚙️ 系统设置", "settings"),
        ]}
    ]
    
    # 渲染导航
    for group in pages:
        # 分组标题
        st.sidebar.write(group["group"])
        
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
                width='stretch',
                help=f"跳转到{page_name}",
            ):
                st.session_state.current_page = page_key
                st.rerun()
    
    # 底部提示
    st.sidebar.write("---")
    
    st.sidebar.write("""
**使用提示:**
- 在"视频管理"添加视频
- 实时获取数据（1-2秒）
- 查看深度分析报告
- 优化内容策略
    """)
    
    return st.session_state.current_page


def get_current_page():
    """获取当前选中的页面"""
    if "current_page" not in st.session_state:
        st.session_state.current_page = "overview"
    return st.session_state.current_page


def set_current_page(page):
    """设置当前页面"""
    st.session_state.current_page = page
    st.rerun()
