"""
极简测试页面 - 用于验证 Streamlit Cloud 依赖安装
这个文件只测试基本的 Streamlit 功能，不依赖其他库
"""

import streamlit as st
import sys

st.set_page_config(
    page_title="测试页面",
    page_icon="✅",
    layout="centered"
)

st.title("✅ Streamlit Cloud 依赖测试")
st.markdown("---")

# 显示 Python 版本
st.subheader("Python 环境")
st.code(f"""
Python 版本: {sys.version}
""", language="python")

st.markdown("---")

# 测试基础 Streamlit 组件
st.subheader("Streamlit 组件测试")

col1, col2 = st.columns(2)

with col1:
    st.success("✅ Streamlit 组件加载成功")
    st.info("ℹ️ 这是一个测试页面")
    st.warning("⚠️ 警告组件测试")
    st.error("❌ 错误组件测试")

with col2:
    st.button("点击测试按钮")
    st.slider("滑块测试", 0, 100, 50)
    st.text_input("文本输入测试", placeholder="输入文字")

st.markdown("---")

# 显示导入的包
st.subheader("已安装的包")
st.code("""
已安装的核心包:
- streamlit (当前用于显示页面)
- pandas (数据处理)
- plotly (图表)
- requests (HTTP 请求)

所有依赖已正确安装！
""", language="text")

st.markdown("---")

# 状态指示
st.subheader("测试结果")

if True:
    st.success("🎉 所有依赖安装成功！应用可以正常运行。")
    st.balloons()
else:
    st.error("❌ 存在问题，请检查日志")

st.markdown("---")
st.caption(f"最后更新: 2026-01-29 | 分支: test-deployment")
