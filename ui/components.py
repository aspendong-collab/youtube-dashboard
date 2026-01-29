"""
UI 组件库
提供通用的 UI 组件
"""

import streamlit as st
from .styles import get_custom_styles


def render_metric_card(title, value, delta=None, delta_color="normal", help_text=None):
    """
    渲染指标卡片
    
    Args:
        title: 卡片标题
        value: 卡片值
        delta: 变化量（可选）
        delta_color: 变化量颜色（normal/inverse/off）
        help_text: 帮助文本（可选）
    """
    col = st.columns([1, 4, 1])
    
    with col[0]:
        st.write("")
    
    with col[1]:
        st.markdown(get_custom_styles(), unsafe_allow_html=True)
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 0.9rem; color: #b8c1ec; margin-bottom: 0.5rem;">
                {title}
            </div>
            <div style="font-size: 2rem; font-weight: 700; color: #ffffff; margin-bottom: 0.25rem;">
                {value}
            </div>
        """, unsafe_allow_html=True)
        
        if delta is not None:
            delta_sign = "↑" if delta > 0 else "↓"
            delta_color_class = "accent-green" if delta > 0 else "accent-orange"
            st.markdown(f"""
            <div style="font-size: 0.85rem; color: {delta_color_class};">
                {delta_sign} {abs(delta):.1f}% 较上周
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        if help_text:
            st.help(help_text)
    
    with col[2]:
        st.write("")


def render_info_box(title, content, icon="ℹ️"):
    """
    渲染信息框
    
    Args:
        title: 标题
        content: 内容
        icon: 图标（默认为信息图标）
    """
    st.markdown(get_custom_styles(), unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stInfo">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="font-size: 1.5rem;">{icon}</div>
            <div>
                <div style="font-weight: 600; font-size: 1rem; margin-bottom: 0.25rem;">
                    {title}
                </div>
                <div style="font-size: 0.9rem; color: #b8c1ec;">
                    {content}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_warning_box(title, content, icon="⚠️"):
    """
    渲染警告框
    
    Args:
        title: 标题
        content: 内容
        icon: 图标（默认为警告图标）
    """
    st.markdown(get_custom_styles(), unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stWarning">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="font-size: 1.5rem;">{icon}</div>
            <div>
                <div style="font-weight: 600; font-size: 1rem; margin-bottom: 0.25rem;">
                    {title}
                </div>
                <div style="font-size: 0.9rem; color: #b8c1ec;">
                    {content}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_success_box(title, content, icon="✅"):
    """
    渲染成功框
    
    Args:
        title: 标题
        content: 内容
        icon: 图标（默认为成功图标）
    """
    st.markdown(get_custom_styles(), unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stSuccess">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="font-size: 1.5rem;">{icon}</div>
            <div>
                <div style="font-weight: 600; font-size: 1rem; margin-bottom: 0.25rem;">
                    {title}
                </div>
                <div style="font-size: 0.9rem; color: #b8c1ec;">
                    {content}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_error_box(title, content, icon="❌"):
    """
    渲染错误框
    
    Args:
        title: 标题
        content: 内容
        icon: 图标（默认为错误图标）
    """
    st.markdown(get_custom_styles(), unsafe_allow_html=True)
    st.markdown(f"""
    <div class="stError">
        <div style="display: flex; align-items: center; gap: 0.75rem;">
            <div style="font-size: 1.5rem;">{icon}</div>
            <div>
                <div style="font-weight: 600; font-size: 1rem; margin-bottom: 0.25rem;">
                    {title}
                </div>
                <div style="font-size: 0.9rem; color: #b8c1ec;">
                    {content}
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)


def render_chart_container(title, chart, description=None):
    """
    渲染图表容器
    
    Args:
        title: 图表标题
        chart: Plotly 图表对象
        description: 图表描述（可选）
    """
    st.markdown(get_custom_styles(), unsafe_allow_html=True)
    st.markdown(f"""
    <div class="metric-card">
        <h3>{title}</h3>
        {f'<p style="color: #b8c1ec; font-size: 0.9rem; margin-bottom: 1rem;">{description}</p>' if description else ''}
    </div>
    """, unsafe_allow_html=True)
    
    st.plotly_chart(chart, width='stretch', theme="plotly_dark")


def render_section_title(title, description=None, icon=None):
    """
    渲染区块标题
    
    Args:
        title: 标题
        description: 描述（可选）
        icon: 图标（可选）
    """
    if icon:
        st.markdown(f"""
        <h2 style="display: flex; align-items: center; gap: 0.75rem;">
            <span style="font-size: 1.75rem;">{icon}</span>
            <span>{title}</span>
        </h2>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"<h2>{title}</h2>", unsafe_allow_html=True)
    
    if description:
        st.markdown(f"""
        <p style="color: #b8c1ec; font-size: 1rem; margin-bottom: 1.5rem;">
            {description}
        </p>
        """, unsafe_allow_html=True)


def render_empty_state(message, icon="📭"):
    """
    渲染空状态
    
    Args:
        message: 空状态消息
        icon: 图标（默认为空文件夹图标）
    """
    st.markdown(f"""
    <div style="text-align: center; padding: 3rem 1rem; color: #8892b0;">
        <div style="font-size: 4rem; margin-bottom: 1rem;">{icon}</div>
        <div style="font-size: 1.1rem;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def render_loading_state(message="加载中...", size="large"):
    """
    渲染加载状态
    
    Args:
        message: 加载消息
        size: 大小（small/medium/large）
    """
    size_map = {
        "small": "1rem",
        "medium": "1.5rem",
        "large": "2rem"
    }
    
    size_value = size_map.get(size, "1.5rem")
    
    st.markdown(f"""
    <div style="display: flex; align-items: center; gap: 1rem; padding: 1rem;">
        <div class="animate-pulse" style="font-size: {size_value};">
            ⏳
        </div>
        <div style="color: #b8c1ec;">{message}</div>
    </div>
    """, unsafe_allow_html=True)


def render_separator(text=None):
    """
    渲染分隔线
    
    Args:
        text: 分隔线文本（可选）
    """
    if text:
        st.markdown(f"""
        <div style="position: relative; margin: 2rem 0;">
            <hr>
            <div style="
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                background: linear-gradient(135deg, #0a0e27 0%, #16213e 100%);
                padding: 0 1rem;
                color: #8892b0;
                font-size: 0.9rem;
            ">
                {text}
            </div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<hr>", unsafe_allow_html=True)
