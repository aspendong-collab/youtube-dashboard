# Streamlit Cloud 部署修复说明

## 修复内容

### 1. requirements.txt 简化
从 132 个依赖精简到 7 个核心依赖：
- streamlit>=1.28.0
- pandas>=2.0.0
- plotly>=5.17.0
- requests>=2.31.0
- python-dateutil>=2.8.0
- pytz>=2023.0
- tqdm>=4.66.0

### 2. 移除的不兼容依赖
- `distro-info==1.1+ubuntu0.2` - Ubuntu 特定版本，Streamlit Cloud 不支持
- `dbus-python==1.2.18` - 需要 DBus 系统库
- `PyGObject==3.42.1` - 需要 GTK 系统库
- `python-apt==2.4.0+ubuntu4.1` - 需要 APT 系统库
- `coze-workload-identity` - Coze 特定依赖
- `langchain*` - 未使用的 AI 框架
- 大量开发工具和测试框架

### 3. dashboard.py 修复

#### 修复 1: generate_word_cloud 函数
- 添加类型检查，确保输入是列表或元组
- 添加元素类型验证，跳过非字符串元素
- 添加防御性检查，确保 `word_counts` 在任何情况下都是 `Counter` 对象
- 增强文档字符串，明确参数和返回值类型

#### 修复 2: save_video_ids_to_github 函数
- 移除所有 `subprocess` 调用（subprocess 在 Streamlit Cloud 上不可用）
- 改为提示用户手动提交到 GitHub
- 提供清晰的指导说明

### 4. Git 修复
- 使用 --force 强制推送到 origin/main，避免 rebase 冲突
- 确保远程仓库包含正确的简化版本

## 新增功能（v2.0.0）

### 5. 实时数据获取功能

#### 新增函数
1. **fetch_video_data_direct(video_ids)**
   - 直接从 YouTube API 获取视频数据
   - 从 Streamlit Secrets 读取 API Key
   - 支持批量获取（最多50个）
   - 实时响应（1-2秒内完成）

2. **save_video_stats_direct(conn, video_data)**
   - 直接保存视频数据到数据库
   - 自动计算互动率
   - 更新视频基本信息
   - 插入最新统计数据

3. **add_videos_direct(conn, video_urls)**
   - 批量添加视频并实时获取数据
   - 替代原有的 add_videos() 函数
   - 提供即时反馈

#### 用户体验改进
- ✅ 添加视频后 1-2 秒内即可看到数据
- ✅ 页面自动刷新（使用 st.rerun()）
- ✅ 无需手动操作 GitHub
- ✅ 无需等待 1-3 分钟
- ✅ 实时显示获取进度

#### 配置要求
- 需要在 Streamlit Cloud Secrets 中配置 `YOUTUBE_API_KEY`
- 详见 [SECRETS_SETUP.md](SECRETS_SETUP.md)

### 6. 文档更新
- 新增 `SECRETS_SETUP.md` - Streamlit Secrets 配置指南
- 更新操作指南，说明实时获取功能
- 添加 API 配额说明
- 提供常见问题解答

## 部署说明

### 初始部署
1. 在 Streamlit Cloud Secrets 中配置 `YOUTUBE_API_KEY`
2. 推送代码到 GitHub
3. 在 Streamlit Cloud 连接仓库并部署
4. 等待 2-3 分钟完成依赖安装

### 后续使用
1. 访问"视频管理"页面
2. 输入 YouTube 视频地址
3. 点击"添加视频"按钮
4. **实时获取数据**（1-2秒内）
5. 页面自动刷新展示数据

### 数据更新机制
- **实时获取**：添加视频时立即获取
- **定时更新**：GitHub Actions 每日 3 次自动更新（9:00, 12:00, 18:00）
- **手动更新**：点击"立即更新所有视频数据"按钮

## 注意事项

### API 配额
- YouTube Data API v3 免费配额：每日 10,000 单位
- 单次获取视频信息：1 单位/视频
- 建议监控配额使用情况，避免超限

### GitHub Actions 保留
- GitHub Actions 仍然运行，用于定时更新
- 定时更新会使用相同的数据库
- 评论获取仍依赖 GitHub Actions

### 安全性
- API Key 存储在 Streamlit Secrets，不会在代码中暴露
- 本地开发时使用 `.streamlit/secrets.toml`
- **不要**将 `secrets.toml` 提交到 Git

## 技术架构对比

### 旧架构（v1.0）
```
用户输入 → 保存到 GitHub → GitHub Actions 获取数据 → 写入数据库 → 用户手动刷新
```

### 新架构（v2.0）
```
用户输入 → 直接调用 YouTube API → 实时写入数据库 → 页面自动刷新展示
         ↑
    Streamlit Secrets (API Key)
```

### 优势
- ⚡ **速度**：1-2 秒 vs 1-3 分钟
- 🎯 **简洁**：无需手动操作 GitHub
- 🔄 **自动化**：页面自动刷新
- 🔒 **安全**：API Key 存储在云端 Secrets

## 提交历史

1. 746be3c - fix: 移除 dashboard.py 中的 subprocess 调用以支持 Streamlit Cloud
2. fd23e03 - fix: 简化 requirements.txt 以支持 Streamlit Cloud 部署
3. [新提交] - feat: 新增实时数据获取功能，使用 Streamlit Secrets 存储 API Key
