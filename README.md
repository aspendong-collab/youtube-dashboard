# 📊 YouTube Analytics Dashboard

> 融合 Adjust 和 Apple 设计风格的现代化 YouTube 数据分析平台

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.53+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## ✨ 特性

### 🎨 现代化 UI 设计
- **深色主题**：专业的深蓝色渐变背景
- **卡片式布局**：毛玻璃效果 + 柔和阴影
- **统一设计规范**：圆角、阴影、留白统一
- **响应式设计**：完美适配桌面和移动端

### 📊 强大的数据分析
- **整体看板**：总览所有视频的总体数据
- **单个视频分析**：深入分析每个视频的表现
- **智能优化建议**：基于数据的 SEO 优化建议
- **评论分析**：词云、情感分析、用户画像

### 🚀 高效功能
- **实时数据获取**：1-2 秒内获取最新数据
- **批量添加视频**：支持一次性添加多个视频
- **数据趋势图表**：可视化展示数据变化
- **爆款预警**：自动检测异常数据

---

## 🚀 快速开始

### 1. 克隆仓库

```bash
cd /workspace/projects
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置 API 密钥

从 [Google Cloud Console](https://console.cloud.google.com/) 获取 YouTube Data API v3 密钥。

### 4. 启动应用

```bash
streamlit run dashboard.py
# 或使用快速启动脚本
./run.sh
```

### 5. 访问应用

浏览器打开：`http://localhost:8501`

---

## 📁 项目结构

```
youtube-dashboard/
├── analytics/          # 数据分析模块
│   ├── comment_analytics.py  # 评论分析
│   └── video_analytics.py    # 视频分析
├── api/               # API 封装模块
│   └── youtube_api.py        # YouTube Data API 封装
├── database/          # 数据库操作模块
│   └── connection.py         # 数据库连接和操作
├── ui/                # UI 组件模块
│   ├── components.py         # 通用 UI 组件
│   ├── sidebar.py           # 侧边栏组件
│   └── styles.py            # CSS 样式
├── utils/             # 工具函数模块
│   └── helpers.py           # 辅助函数
├── config.py          # 配置管理
├── dashboard.py       # 主程序
├── requirements.txt   # 依赖管理
└── run.sh            # 快速启动脚本
```

---

## 🎯 功能页面

### 📹 视频管理
- 添加单个视频
- 批量添加视频
- 查看监控视频列表

### 📊 整体看板
- 总体数据统计
- 热门视频排行
- 互动率排行

### 📹 单个视频
- 视频详细信息
- 数据趋势图表
- 智能优化建议
- 评论词云
- 情感分析

### 🔥 爆款提醒
- 数据异常预警
- 实时提醒

### 🎯 SEO 优化
- 标题分析
- 描述分析
- 标签使用统计

### 💬 评论分析
- 最活跃评论者
- 最多点赞的评论

### 🔑 API 配置
- YouTube Data API 密钥管理

### 📊 数据源管理
- 数据库统计信息

---

## 🎨 设计系统

### 色彩规范

```css
/* 主色调 */
--bg-primary: #0a0e27
--bg-secondary: #16213e
--card-bg: rgba(255, 255, 255, 0.05)

/* 文本颜色 */
--text-primary: #ffffff
--text-secondary: #b8c1ec

/* 强调色（渐变） */
--gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
--accent-blue: #667eea
--accent-purple: #764ba2
--accent-green: #43e97b
--accent-orange: #ff6b6b
```

### 组件规范

| 组件 | 圆角 | 阴影 |
|------|------|------|
| 卡片 | 12px | 0 4px 20px rgba(0,0,0,0.15) |
| 按钮 | 8px | 0 4px 15px rgba(102,126,234,0.3) |
| 输入框 | 8px | 无 |

---

## 🔧 技术栈

- **前端框架**: Streamlit 1.53+
- **数据处理**: Pandas 2.3+
- **数据可视化**: Plotly 6.5+
- **HTTP 请求**: Requests 2.32+
- **数据库**: SQLite 3
- **API**: YouTube Data API v3

---

## 📚 文档

- **快速开始**: [QUICKSTART.md](QUICKSTART.md)
- **升级指南**: [UPGRADE_GUIDE.md](UPGRADE_GUIDE.md)
- **升级总结**: [UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md)
- **交付总结**: [DELIVERY_SUMMARY.md](DELIVERY_SUMMARY.md)

---

## 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

---

## 📄 许可证

本项目基于 MIT 许可证开源。

---

## 📞 联系方式

如有问题或建议，欢迎通过以下方式联系：

- 提交 Issue
- 发送邮件
- 在评论区留言

---

**立即体验全新的 YouTube Analytics Dashboard！** 🚀

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://youtube-analytics-dashboard.streamlit.app)
