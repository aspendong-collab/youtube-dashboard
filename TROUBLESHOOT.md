# 🔧 Streamlit Cloud 部署故障排除

## ❌ 问题：Error installing requirements

### 原因
`requirements.txt` 包含了太多不必要的依赖，包括：
- 系统特定的包（`dbus-python`, `python-apt`）
- 开发工具（`pytest`, `pylint`）
- 不兼容的包（`distro-info`, `coze-workload-identity`）

### ✅ 已修复
已将 `requirements.txt` 精简为仅包含核心依赖：

```
streamlit>=1.53.0
pandas>=2.3.0
plotly>=6.5.0
requests>=2.32.0
python-dateutil>=2.9.0
pytz>=2025.0
```

**最新提交**：`a883e04`

---

## 🚀 现在请重新部署

### 方法一：在 Streamlit Cloud 上重新部署

1. 访问：https://share.streamlit.io
2. 找到您的应用：`youtube-analytics-v2`
3. 点击右上角 **"..."** → **"Settings"**
4. 找到 **"Update and redeploy"** 或 **"Re-deploy"**
5. 点击 **"Redeploy"** 按钮

### 方法二：删除并重新创建应用（推荐）

如果重新部署还是失败，建议删除旧应用并重新创建：

1. 在 Streamlit Cloud，找到应用 `youtube-analytics-v2`
2. 点击右上角 **"..."** → **"Delete app"**
3. 确认删除
4. 点击 **"New app"**
5. 重新填写信息：
   ```
   App name: youtube-analytics-v2
   Repository: aspendong-collab/youtube-dashboard
   Branch: main
   Main file path: dashboard.py
   ```
6. 点击 **"Deploy"**

---

## 📊 部署检查清单

在重新部署前，确认：

- [ ] 最新代码已推送到 GitHub（提交：a883e04）
- [ ] `requirements.txt` 已精简（仅6个核心依赖）
- [ ] `dashboard.py` 存在且无语法错误
- [ ] `youtube_dashboard.db` 已提交到 Git

---

## 🔍 查看部署日志

如果还是失败：

1. 访问 Streamlit Cloud
2. 找到您的应用
3. 点击 **"..."** → **"Manage app"**
4. 查看终端（Terminal）输出
5. 找到具体的错误信息

**常见错误**：

| 错误 | 原因 | 解决 |
|------|------|------|
| `No matching distribution` | 包名或版本错误 | 检查 requirements.txt |
| `Permission denied` | 系统包冲突 | 使用 `--ignore-installed` |
| `ModuleNotFoundError` | 包未安装 | 添加到 requirements.txt |

---

## 🎯 确认修复成功

部署成功后，您应该看到：

1. **Streamlit Cloud 界面**
   - 状态：**Running** 🟢
   - 无错误信息

2. **应用界面**
   - 深蓝色渐变背景
   - 分组侧边栏导航
   - 现代化卡片布局

3. **功能正常**
   - 可以添加视频
   - 可以查看数据
   - 可以访问所有页面

---

## 📞 如果还是不行

### 步骤 1：验证 GitHub 仓库

访问：https://github.com/aspendong-collab/youtube-dashboard

检查：
- ✅ `requirements.txt` 内容（应该只有6行）
- ✅ 最新提交是 `a883e04`
- ✅ `dashboard.py` 存在

### 步骤 2：完全重新创建应用

1. 删除旧应用 `youtube-analytics-v2`
2. 删除所有失败的应用
3. 点击 **"New app"**
4. 填写：
   ```
   App name: youtube-analytics-v3
   Repository: aspendong-collab/youtube-dashboard
   Branch: main
   Main file path: dashboard.py
   ```
5. 点击 **"Deploy"**

### 步骤 3：联系支持

如果所有方法都失败：

1. 查看 Streamlit Cloud 部署日志
2. 截图错误信息
3. 在 Streamlit 论坛发帖：https://discuss.streamlit.io

---

## 🚀 快速重新部署命令

如果使用 Streamlit CLI：

```bash
cd /workspace/projects

# 重新登录
streamlit login

# 重新部署
streamlit deploy --force
```

---

## ✅ 当前状态

| 项目 | 状态 |
|------|------|
| GitHub 仓库 | ✅ 已更新（最新提交：a883e04） |
| requirements.txt | ✅ 已精简（6个核心依赖） |
| 部署状态 | ⏳ 等待重新部署 |

---

## 📝 修复历史

| 提交 | 内容 |
|------|------|
| a883e04 | fix: 精简 requirements.txt，仅保留核心依赖 |
| 54ecae4 | docs: 新增完整的 Streamlit Cloud 部署指南 |
| e119c44 | docs: 新增 Streamlit Cloud 部署说明 |

---

**现在就去重新部署吧！应该能成功了！** 🚀

访问：https://share.streamlit.io
