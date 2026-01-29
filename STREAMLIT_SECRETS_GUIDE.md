# Streamlit Cloud Secrets 配置详细指南

## 找到 Secrets 配置入口

### 方法 1：通过 Manage App 进入（推荐）

1. **进入你的应用列表**
   - 访问 https://share.streamlit.io/
   - 登录你的账号
   - 找到你的 YouTube Dashboard 应用

2. **点击应用卡片**
   - 点击应用卡片，进入应用详情页

3. **点击 "Manage App"**
   - 在应用详情页，点击右上角的 "Manage App" 按钮

4. **进入应用设置页面**
   - 在管理页面，点击左侧菜单的 **"Settings"**
   - 找到 **"Secrets"** 选项卡

5. **配置 Secrets**
   - 点击 "Secrets" 选项卡
   - 在编辑器中添加以下内容：

```toml
YOUTUBE_API_KEY = "your_youtube_api_key_here"
```

6. **保存并重新部署**
   - 点击 "Save" 按钮
   - 返回应用详情页
   - 点击 "Re-deploy" 按钮重新部署应用

### 方法 2：通过 Settings 直接进入

如果你已经在 Manage App 页面：

1. 点击左侧菜单的 **"Settings"**
2. 点击 **"Secrets"** 选项卡
3. 添加 API Key 并保存

### 方法 3：部署时配置（首次部署）

如果你还没有部署应用：

1. 点击 "Deploy an app" 按钮
2. 选择 "From GitHub"
3. 选择你的仓库
4. 在 "Settings" 部分，找到 "Secrets" 选项卡
5. 添加 API Key
6. 点击 "Deploy"

## 截图说明

### 应用列表页面
```
┌─────────────────────────────────────┐
│  Your apps                          │
├─────────────────────────────────────┤
│  [YouTube Dashboard Card]           │
│  Manage App  ▼                      │
└─────────────────────────────────────┘
```

### Manage App 页面
```
┌─────────────────────────────────────┐
│  Manage App - YouTube Dashboard     │
├─────────────────────────────────────┤
│  ▸ Overview                         │
│  ▸ Settings ← 点击这里              │
│  ▸ Logs                             │
│  ▸ Usage                            │
└─────────────────────────────────────┘
```

### Settings 页面
```
┌─────────────────────────────────────┐
│  Settings                           │
├─────────────────────────────────────┤
│  ▸ Secrets ← 点击这里              │
│  ▸ General                          │
│  ▸ Repository                       │
│  ▸ Environment                      │
└─────────────────────────────────────┘
```

### Secrets 页面
```
┌─────────────────────────────────────┐
│  Secrets                            │
├─────────────────────────────────────┤
│  Add new secrets:                   │
│  ┌─────────────────────────────┐    │
│  │ YOUTUBE_API_KEY = "xxx"    │    │
│  └─────────────────────────────┘    │
│                                     │
│  [Save]  [Cancel]                   │
└─────────────────────────────────────┘
```

## 常见问题

### Q1: 我只看到 "Rerun", "Settings", "Print", "Record a screencast"

**A:** 这些是应用运行时的顶部菜单，不是管理界面。

**正确的步骤：**
1. 退出当前应用（返回 https://share.streamlit.io/）
2. 在应用卡片上点击 **"Manage App"**（不是进入应用内部）
3. 在管理页面找到 Settings → Secrets

### Q2: 找不到 "Manage App" 按钮

**A:** 检查以下几点：
- 确认你使用的是正确的账号
- 确认你有该应用的管理权限
- 尝试刷新页面
- 检查应用是否已部署成功

### Q3: Secrets 选项卡是空的

**A:** 这是正常的。第一次配置时，Secrets 页面是空的，你需要手动添加。

### Q4: 配置后没有生效

**A:** 配置 Secrets 后，必须：
1. 保存 Secrets
2. 重新部署应用（点击 "Re-deploy"）
3. 等待部署完成（通常 1-2 分钟）

## 验证配置是否成功

### 方法 1：查看应用日志

1. 进入 Manage App → Logs
2. 查看是否有 "未配置 YouTube API Key" 的错误
3. 如果没有该错误，说明配置成功

### 方法 2：测试添加视频

1. 访问应用
2. 进入"视频管理"页面
3. 输入一个 YouTube 视频地址
4. 点击"添加视频"
5. 如果 1-2 秒内显示"✅ 成功添加 1 个视频并获取数据！"，说明配置成功

### 方法 3：查看 Secrets

1. 进入 Manage App → Settings → Secrets
2. 检查是否显示 `YOUTUBE_API_KEY`
3. 如果显示，说明配置成功

## 获取 YouTube API Key

### 详细步骤

1. **访问 Google Cloud Console**
   - 打开 https://console.cloud.google.com/
   - 登录你的 Google 账号

2. **创建项目**
   - 点击顶部的项目选择器
   - 点击"新建项目"
   - 输入项目名称（如"YouTube Dashboard"）
   - 点击"创建"

3. **启用 YouTube Data API v3**
   - 在顶部搜索框搜索"YouTube Data API v3"
   - 点击搜索结果
   - 点击"启用"按钮

4. **创建 API Key**
   - 点击左侧菜单的"凭据"
   - 点击"创建凭据" → "API 密钥"
   - 复制生成的 API Key

5. **配置到 Streamlit Cloud**
   - 按照"找到 Secrets 配置入口"的步骤配置
   - 将 API Key 粘贴到 `YOUTUBE_API_KEY` 中

## 注意事项

1. **不要**将 API Key 提交到 Git
2. **不要**在代码中硬编码 API Key
3. **定期**更换 API Key
4. **监控** API 使用情况（Google Cloud Console）
5. **限制** API Key 的使用范围（可选）

## 本地开发配置

如果你在本地开发：

1. 在项目根目录创建 `.streamlit` 文件夹
2. 在 `.streamlit` 文件夹中创建 `secrets.toml` 文件
3. 添加以下内容：

```toml
YOUTUBE_API_KEY = "your_youtube_api_key_here"
```

4. **重要**：将 `.streamlit/secrets.toml` 添加到 `.gitignore`

## 技术支持

如果仍然无法配置：

1. 查看 [Streamlit Cloud 官方文档](https://docs.streamlit.io/streamlit-cloud/get-started/deploy-an-app/connect-to-data-sources/secrets-management)
2. 查看 [YouTube Data API 文档](https://developers.google.com/youtube/v3/getting-started)
3. 检查 Streamlit Cloud 的 [状态页面](https://status.streamlit.io/)

## 快速参考

```
应用列表 → Manage App → Settings → Secrets → 添加 API Key → Save → Re-deploy
```

记住这个路径，配置就很简单了！
