# 🔍 诊断页面空白问题 - 用户指南

## ✅ 已完成的修复

### 修复 1: 图片参数错误（已完成）
**问题**: `st.image()` 使用了无效参数 `width="stretch"`  
**修复**: 改为 `use_column_width=True`  
**状态**: ✅ 已推送

### 修复 2: 添加调试模式（已完成）
**位置**: 侧边栏 → "🔧 调试模式"  
**功能**: 显示当前页面、API Key 状态、视频数量等  
**状态**: ✅ 已推送

### 修复 3: 添加错误处理（已完成）
**位置**: 所有页面渲染函数  
**功能**: 捕获并显示运行时错误  
**状态**: ✅ 已推送

---

## 🎯 立即执行的诊断步骤

### 步骤 1: 刷新应用
1. 访问你的应用 URL
2. 按 `Ctrl + F5` 或 `Cmd + Shift + R` 强制刷新
3. 等待 30-60 秒让应用更新

### 步骤 2: 检查调试模式
1. 在左侧边栏找到 **"🔧 调试模式"**
2. 点击展开
3. 查看显示的信息：
   - **当前页面**: 应该是 "overview"、"video_management" 等
   - **API Key 已配置**: 应该显示 `True`
   - **视频数量**: 应该显示一个数字（如 15）

### 步骤 3: 根据调试信息判断

#### 情况 A: 显示 "视频数量: 0"
**原因**: 数据库中没有视频数据  
**解决方案**:
1. 在侧边栏点击 **"📹 视频管理"**
2. 输入 YouTube URL 或视频 ID
3. 点击 **"添加视频"** 按钮
4. 等待视频信息加载

#### 情况 B: 显示 "API Key 已配置: False"
**原因**: YouTube API 密钥未配置  
**解决方案**:
1. 访问 Streamlit Cloud 管理页面
2. 点击 **"Settings"** → **"Secrets"**
3. 添加以下内容：
   ```
   YOUTUBE_API_KEY=你的YouTube_API密钥
   ```
4. 保存后等待应用自动重新部署

#### 情况 C: 显示错误信息
**原因**: 数据库或其他运行时错误  
**解决方案**:
1. 查看 Streamlit Cloud 日志
2. 将错误信息发送给我

#### 情况 D: 调试模式显示正常，但页面仍然空白
**原因**: 可能是 CSS 或 JavaScript 问题  
**解决方案**:
1. 尝试使用不同的浏览器（Chrome, Firefox, Safari）
2. 检查浏览器控制台是否有错误（F12 → Console）
3. 清除浏览器缓存和 Cookie

---

## 📊 查看完整日志

### 方法 1: Streamlit Cloud 网页界面
1. 访问 https://share.streamlit.io/
2. 找到你的应用并点击 **"Manage app"**
3. 在右侧面板查看 **"Logs"**
4. 搜索关键词：`ERROR`, `Exception`, `Traceback`

### 方法 2: 查看最新日志
在日志页面搜索以下内容：
```
Starting up repository
Cloning repository
Installing dependencies
Application is running
```

---

## 🚨 常见错误及解决方案

### 错误 1: ModuleNotFoundError
**症状**: `ModuleNotFoundError: No module named 'xxx'`  
**原因**: 某个依赖包未安装  
**解决方案**: 检查 `requirements.txt` 是否包含所有必需的包

### 错误 2: SQLite database error
**症状**: `sqlite3.OperationalError: no such table: videos`  
**原因**: 数据库未正确初始化  
**解决方案**: 检查 `database.py` 中的 `init_database()` 函数

### 错误 3: YouTube API error
**症状**: `Error 403: quotaExceeded` 或 `Error 400: keyInvalid`  
**原因**: API 密钥无效或配额已用完  
**解决方案**:
1. 检查 API 密钥是否正确
2. 检查 Google Cloud Console 中的配额使用情况
3. 重置配额或升级 API 套餐

### 错误 4: Network error
**症状**: `requests.exceptions.ConnectionError`  
**原因**: Streamlit Cloud 无法访问 YouTube API  
**解决方案**: 检查网络连接和防火墙设置

---

## 🔧 临时解决方案

### 方案 1: 使用测试页面
如果主应用无法工作，可以临时切换到测试页面：

1. 访问 Streamlit Cloud 管理页面
2. 点击 **"Settings"**
3. 修改 **"Main file path"** 为 `test_simple.py`
4. 保存并等待重新部署

### 方案 2: 降级 Streamlit 版本
如果 Streamlit 版本有问题，可以降级到稳定版本：

编辑 `requirements.txt`：
```
streamlit==1.40.0
pandas==2.3.3
plotly==6.5.2
requests==2.32.5
```

### 方案 3: 清空数据库
如果数据库损坏，可以删除并重新创建：

1. 在 Streamlit Cloud 终端执行：
   ```bash
   rm youtube_dashboard.db
   ```
2. 重启应用，数据库会自动重建

---

## 📞 获取帮助

### 需要提供的信息
如果问题仍然存在，请提供以下信息：

1. **调试模式显示的内容**
   - 当前页面
   - API Key 状态
   - 视频数量
   - 任何错误信息

2. **Streamlit Cloud 日志**
   - 最近的 50 行日志
   - 任何 ERROR 或 Exception 信息

3. **浏览器控制台错误**
   - 按 F12 打开开发者工具
   - 查看 Console 标签页
   - 截图或复制错误信息

4. **访问的 URL**
   - 完整的应用 URL

---

## ✨ 预期结果

修复后，应用应该显示：
- ✅ 左侧边栏有导航菜单
- ✅ 主页面显示 "YouTube Analytics Dashboard"
- ✅ 调试模式可以正常展开
- ✅ 如果有数据，显示视频统计信息
- ✅ 如果没有数据，显示提示信息

---

## 📝 更新历史

- **2026-01-30 03:50**: 修复 st.image() 参数
- **2026-01-30 04:00**: 添加调试模式和错误处理
- **2026-01-30 04:05**: 创建诊断指南

---

**最后更新**: 2026-01-30 04:05  
**状态**: 等待用户反馈调试信息
