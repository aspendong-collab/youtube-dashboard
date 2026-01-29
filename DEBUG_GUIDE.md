# 调试指南 - 左侧列表为空

## 可能的原因

### 1. YouTube API Key 未配置
**症状**: 左侧列表为空，但应用可以正常加载

**解决方案**:
1. 访问 Streamlit Cloud 应用管理页面
2. 点击 "Manage app"
3. 滚动到 "Secrets" 部分
4. 添加以下 secret:
   ```
   YOUTUBE_API_KEY=your_youtube_api_key_here
   ```
5. 点击 "Save"
6. 重启应用

**如何获取 YouTube API Key**:
1. 访问 Google Cloud Console
2. 创建新项目或选择现有项目
3. 启用 YouTube Data API v3
4. 创建 OAuth 2.0 凭证（API Key）
5. 复制 API Key

### 2. 数据库文件路径问题
**症状**: 应用启动时报错，无法访问数据库

**解决方案**: 已修复
- 使用绝对路径代替相对路径
- 修改位置: `database/connection.py`

**修改内容**:
```python
# 旧代码
conn = sqlite3.connect("youtube_dashboard.db")

# 新代码
db_path = os.path.join(os.getcwd(), "youtube_dashboard.db")
conn = sqlite3.connect(db_path)
```

### 3. 数据库表结构未正确初始化
**症状**: 应用启动时报错 "no such column" 或 "no such table"

**解决方案**: 已修复
- 添加自动检查和升级逻辑
- 修改位置: `database/connection.py`

**修改内容**:
```python
# 检查并修复 video_stats 表的 recorded_at 列
cursor.execute("PRAGMA table_info(video_stats)")
columns = [column[1] for column in cursor.fetchall()]

if 'recorded_at' not in columns:
    try:
        cursor.execute("ALTER TABLE video_stats ADD COLUMN recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
        conn.commit()
    except Exception as e:
        pass
```

### 4. Streamlit Cloud 环境问题
**症状**: 应用频繁崩溃或无法加载

**解决方案**:
1. 检查 Streamlit Cloud 资源限制
2. 确认应用没有被暂停
3. 查看应用日志中的错误信息

---

## 调试步骤

### 第一步：查看应用日志

1. 访问 Streamlit Cloud 应用管理页面
2. 点击 "Manage app"
3. 查看 "Terminal" 或 "Logs" 部分
4. 复制完整的错误信息

### 第二步：检查 YouTube API Key

1. 访问 Streamlit Cloud Secrets
2. 确认 `YOUTUBE_API_KEY` 已设置
3. 尝试测试 API Key 是否有效

**测试方法**:
```bash
curl "https://www.googleapis.com/youtube/v3/search?key=YOUR_API_KEY&q=test&part=snippet"
```

### 第三步：检查数据库

1. 通过 Streamlit Cloud 终端连接到应用
2. 运行以下命令检查数据库:
```bash
ls -la youtube_dashboard.db
sqlite3 youtube_dashboard.db "SELECT * FROM videos;"
```

### 第四步：清除缓存

如果数据是旧的或损坏的，尝试清除缓存:
1. 访问 Streamlit Cloud 应用管理页面
2. 点击 "Manage app"
3. 滚动到 "Advanced" 部分
4. 点击 "Clear cache"
5. 重启应用

---

## 常见错误

### 错误 1: "This app has encountered an error"

**可能原因**:
- 数据库连接失败
- API Key 无效
- 代码逻辑错误

**解决方案**:
- 查看完整错误日志
- 确认 API Key 已设置
- 检查数据库文件是否存在

### 错误 2: "OperationalError: no such table"

**可能原因**:
- 数据库表未创建

**解决方案**:
- 已修复: `init_database()` 会自动创建表
- 重启应用

### 错误 3: "OperationalError: no such column"

**可能原因**:
- 数据库表结构不匹配

**解决方案**:
- 已修复: 自动添加缺失的列
- 重启应用

### 错误 4: "ModuleNotFoundError"

**可能原因**:
- 依赖未安装

**解决方案**:
- 检查 `requirements.txt`
- 确认所有依赖都已安装

---

## 联系支持

如果以上方法都无法解决问题，请提供以下信息:

1. **完整错误日志** (从 Streamlit Cloud Logs 复制)
2. **应用截图** (显示左侧列表为空)
3. **YouTube API Key 状态** (是否已配置)
4. **Streamlit Cloud 部署日志** (Terminal 输出)

---

## 最新修复

### 提交 7b9e0c1
```
fix: 修复 Streamlit Cloud 数据库路径问题，使用绝对路径
```

**修改内容**:
- 使用 `os.path.join(os.getcwd(), "youtube_dashboard.db")` 代替相对路径
- 确保数据库文件在正确位置创建

---

## 总结

| 问题 | 状态 | 解决方案 |
|------|------|---------|
| 数据库路径 | ✅ 已修复 | 使用绝对路径 |
| recorded_at 列 | ✅ 已修复 | 自动添加 |
| API Key 配置 | ⚠️ 需要用户配置 | 在 Secrets 中添加 |
| 表结构初始化 | ✅ 已修复 | 自动创建和升级 |

**请先配置 YouTube API Key，然后重启应用！**
