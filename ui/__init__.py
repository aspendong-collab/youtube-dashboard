"""
UI 模块初始化文件
"""

from .sidebar import render_sidebar, get_current_page, set_current_page
from .components import (
    render_metric_card,
    render_info_box,
    render_warning_box,
    render_success_box,
    render_error_box,
    render_chart_container,
    render_section_title,
    render_empty_state,
    render_loading_state,
    render_separator,
)
from .styles import get_custom_styles, get_sidebar_styles

__all__ = [
    "render_sidebar",
    "get_current_page",
    "set_current_page",
    "render_metric_card",
    "render_info_box",
    "render_warning_box",
    "render_success_box",
    "render_error_box",
    "render_chart_container",
    "render_section_title",
    "render_empty_state",
    "render_loading_state",
    "render_separator",
    "get_custom_styles",
    "get_sidebar_styles",
]
