# YouTube Dashboard

一个基于 Streamlit 的 YouTube 视频数据分析仪表盘。

## ✨ 特性

- 📊 视频性能分析
- 📈 互动指标追踪（观看数、点赞数、评论数）
- 🔍 多视频对比分析
- 📉 历史趋势图表
- 🎨 现代化 UI 设计

## 🚀 快速开始

### 本地运行

1. 安装依赖：
```bash
pip install -r requirements.txt
```

2. 运行应用：
```bash
streamlit run dashboard.py
```

3. 访问 `http://localhost:8501`

### 部署到 Streamlit Cloud

1. **验证应用（推荐）**
```bash
python3 verify_deployment.py
```

2. **推送到 GitHub**
```bash
git add .
git commit -m "Ready for deployment"
git push origin main
```

3. **在 [share.streamlit.io](https://share.streamlit.io) 创建应用**
   - 选择你的 GitHub 仓库
   - 设置 Main file path 为 `dashboard.py`
   - 点击 "Deploy"

4. **访问你的应用**
   ```
   https://your-app-name.streamlit.app
   ```

详细部署说明请参阅 [DEPLOY_INSTRUCTIONS.md](DEPLOY_INSTRUCTIONS.md)

## 📦 核心依赖

```txt
streamlit==1.39.0
google-api-python-client==2.154.0
pandas==2.2.3
plotly==5.24.1
```

## 📁 项目结构

```
youtube-dashboard/
├── dashboard.py              # 主应用
├── requirements.txt          # 依赖列表
├── youtube_dashboard.db      # SQLite 数据库
├── config.py                 # 配置
├── database/                 # 数据库模块
├── api/                      # YouTube API 模块
├── analytics/                # 数据分析模块
├── ui/                       # UI 组件
└── utils/                    # 工具函数
```

## 📊 功能说明

### Dashboard
- 显示所有视频列表
- 总体统计概览
- 快速性能指标

### Video Analysis
- 单个视频详细分析
- 性能趋势图表
- 互动指标追踪

### Comparison
- 多视频横向对比
- 性能对比图表

### Settings
- 数据刷新选项
- 配置管理

## 🐛 问题排查

### 常见问题

**Q: 部署后显示 "No data found"**
- 检查 `youtube_dashboard.db` 是否在 GitHub 仓库中
- 确认数据库文件大小 > 0 KB

**Q: 页面加载慢**
- 首次加载可能较慢（Streamlit Cloud 冷启动）
- 后续访问会更快

**Q: 模块导入错误**
- 确保所有必需文件已提交到 GitHub
- 运行 `python3 verify_deployment.py` 验证

## 📖 文档

- [DEPLOY_INSTRUCTIONS.md](DEPLOY_INSTRUCTIONS.md) - 详细部署指南
- [FINAL_USER_REPORT.md](FINAL_USER_REPORT.md) - 完整测试报告
- [verify_deployment.py](verify_deployment.py) - 部署前验证脚本

## 📝 更新日志

### v1.0.0 (2025-01-29)

✅ **核心功能完成**
- 视频数据展示
- 性能分析
- 对比功能

✅ **Bug 修复**
- 修复数据库列名错误（recorded_at → fetch_time）
- 优化依赖包（144 个 → 4 个）
- 修复模块导入问题

✅ **部署就绪**
- 完整测试通过
- 部署文档齐全
- 验证脚本提供

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**状态**: ✅ Ready for Deployment
**版本**: 1.0.0
**最后更新**: 2025-01-29
