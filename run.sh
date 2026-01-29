#!/bin/bash

# YouTube Analytics Dashboard - 快速启动脚本

echo "=========================================="
echo "YouTube Analytics Dashboard"
echo "=========================================="
echo ""

# 检查 Python 版本
echo "检查 Python 版本..."
python3 --version

# 检查依赖
echo ""
echo "检查依赖..."
if ! python3 -c "import streamlit" 2>/dev/null; then
    echo "⚠️  Streamlit 未安装，正在安装..."
    pip install -r requirements.txt
fi

echo ""
echo "✅ 依赖检查完成"
echo ""

# 启动应用
echo "启动应用..."
echo "访问地址: http://localhost:8501"
echo ""
echo "=========================================="
streamlit run dashboard.py
