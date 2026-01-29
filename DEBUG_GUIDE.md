# YouTube Dashboard - Streamlit Cloud 部署调试指南

## 问题修复记录

### 1. 依赖安装问题

**问题**: Streamlit Cloud 部署时出现 `Error installing requirements` 错误，提示 `distro-info==1.1+ubuntu0.2` 无法安装。

**解决方案**:
- 精简 `requirements.txt` 为最简版本，仅包含 3 个核心依赖：
  ```
  streamlit
  pandas
  plotly
  ```
- Streamlit Cloud 会自动管理这些依赖的子依赖，避免版本冲突。

**验证方法**:
- 查看 Streamlit Cloud 部署日志，确认 `Requirements file installation successful`

### 2. 数据库列缺失问题

**问题**: `OperationalError: no such column: recorded_at`

**解决方案**:
- 在 `database/connection.py` 的 `init_database()` 函数中添加了自动检测和修复逻辑：
  ```python
  # 检查并修复 video_stats 表的 recorded_at 列
  cursor.execute("PRAGMA table_info(video_stats)")
  columns = [column[1] for column in cursor.fetchall()]
  
  if 'recorded_at' not in columns:
      try:
          cursor.execute("ALTER TABLE video_stats ADD COLUMN recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
          conn.commit()
      except Exception as e:
          # 如果添加失败，忽略错误（可能是表已经正确）
          pass
  ```

**验证方法**:
- 应用启动时会自动检测并修复表结构
- 查看日志中是否有 `ALTER TABLE` 执行记录

### 3. 数据库路径问题

**问题**: `sqlite3.OperationalError` - 数据库文件路径不正确

**解决方案**:
- 修改 `get_db_connection()` 使用绝对路径：
  ```python
  db_path = os.path.join(os.getcwd(), "youtube_dashboard.db")
  ```

**验证方法**:
- 应用启动时应能正常连接数据库
- 左侧侧边栏应显示已添加的视频列表

## Streamlit Cloud 部署步骤

### 1. 准备 GitHub 仓库

确保你的 GitHub 仓库包含以下文件：
```
youtube-dashboard/
├── requirements.txt          # 已修复的精简版本
├── dashboard.py              # 应用入口
├── database/
│   ├── __init__.py
│   └── connection.py         # 已修复的数据库连接
├── api/
├── ui/
├── analytics/
└── utils/
```

### 2. 配置 Streamlit Cloud Secrets

在 Streamlit Cloud 的应用设置中，配置以下 Secrets：

```
YOUTUBE_API_KEY=your_youtube_api_key_here
```

**获取 YouTube API Key 的步骤**:
1. 访问 [Google Cloud Console](https://console.cloud.google.com/)
2. 创建新项目或选择现有项目
3. 启用 YouTube Data API v3
4. 创建凭据 → API 密钥
5. 限制密钥的使用（推荐）
6. 复制 API 密钥

### 3. 连接 GitHub 仓库

1. 访问 [Streamlit Cloud](https://share.streamlit.io/)
2. 点击 "New app"
3. 选择你的 GitHub 仓库
4. 选择分支（通常是 `main` 或 `master`）
5. 设置主文件路径为 `dashboard.py`
6. 点击 "Deploy"

### 4. 验证部署

**成功标志**:
- 应用启动成功，无错误日志
- 界面正常加载，显示左侧侧边栏
- 顶部导航栏显示"概览"、"视频分析"、"评论分析"等标签

**常见问题检查**:

1. **左侧列表为空**:
   - 检查 Secrets 中是否配置了 `YOUTUBE_API_KEY`
   - 在搜索框中输入 YouTube 视频链接或 ID，添加视频

2. **应用无法启动**:
   - 检查部署日志中的依赖安装情况
   - 确认 `requirements.txt` 是精简版本（仅 3 行）

3. **图表无法显示**:
   - 检查浏览器控制台是否有 JavaScript 错误
   - 确认数据库中有数据

## 本地开发调试

### 安装依赖

```bash
pip install streamlit pandas plotly
```

### 设置环境变量

**Linux/Mac**:
```bash
export YOUTUBE_API_KEY=your_key_here
```

**Windows (PowerShell)**:
```powershell
$env:YOUTUBE_API_KEY="your_key_here"
```

**Windows (CMD)**:
```cmd
set YOUTUBE_API_KEY=your_key_here
```

### 运行应用

```bash
streamlit run dashboard.py
```

### 调试模式

在 `dashboard.py` 开头添加调试代码：

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 数据库管理

### 查看数据库内容

```bash
sqlite3 youtube_dashboard.db
```

在 SQLite 命令行中：

```sql
-- 查看所有表
.tables

-- 查看视频表结构
.schema videos

-- 查看视频统计表结构
.schema video_stats

-- 查看数据
SELECT * FROM videos;
SELECT * FROM video_stats ORDER BY recorded_at DESC LIMIT 10;
```

### 重置数据库

如果需要清空数据库并重新开始：

```python
import os
os.remove("youtube_dashboard.db")
```

然后重启应用，会自动创建新的数据库。

## 性能优化建议

1. **限制视频数量**:
   - 建议监控不超过 10 个视频
   - 避免一次性抓取所有视频的评论

2. **数据抓取频率**:
   - 统计数据：每小时或每天更新一次
   - 评论数据：每周更新一次（评论数据量大）

3. **缓存策略**:
   - 应用已使用 `st.cache_data` 缓存查询结果
   - 修改数据后需要清除缓存：在 Streamlit 菜单 → "Rerun"

## 常见错误及解决方案

### 1. `No module named 'plotly'`

**原因**: 依赖未正确安装

**解决**:
```bash
pip install plotly
```

### 2. `OperationalError: unable to open database file`

**原因**: 数据库文件权限或路径问题

**解决**:
- 确保应用有写入权限
- 检查 `os.getcwd()` 返回的路径
- 手动指定数据库绝对路径

### 3. `403 Forbidden` - YouTube API 错误

**原因**: API Key 配额耗尽或未启用 API

**解决**:
- 检查 Google Cloud Console 中的配额
- 确认已启用 YouTube Data API v3
- 验证 API Key 是否正确

### 4. 应用加载缓慢

**原因**: 数据量过大或网络请求多

**解决**:
- 减少监控的视频数量
- 限制抓取的评论数量
- 使用 Streamlit Cloud 的缓存功能

## 联系支持

如果遇到其他问题，请检查：

1. **Streamlit Cloud 日志**: 在应用设置中查看部署日志
2. **GitHub Issues**: 搜索是否有类似问题
3. **Streamlit 社区**: https://discuss.streamlit.io/

## 版本信息

- Streamlit: 1.53.1
- Pandas: 2.3.3
- Plotly: 6.5.2
- Python: 3.9+

最后更新: 2025-06-20
