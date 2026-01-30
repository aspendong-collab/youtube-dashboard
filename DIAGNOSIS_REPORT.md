# 🐛 诊断报告：页面空白问题

## 问题描述
- **症状**: 页面显示 `File: [assets/image.png]` 但没有实际内容展示
- **发生时间**: 部署后首次访问
- **影响范围**: 整个应用页面

## 已识别的问题

### 问题 1: st.image() 参数错误（已修复）
**位置**: dashboard.py 第 605 行  
**原始代码**:
```python
st.image(thumbnail_url, width="stretch")
```

**问题**: `width="stretch"` 不是 Streamlit `st.image()` 的有效参数  
**修复**:
```python
st.image(thumbnail_url, use_column_width=True)
```

### 可能的其他原因

#### 1. 数据库文件路径问题
- Streamlit Cloud 的文件系统路径可能与本地不同
- 数据库文件可能没有正确初始化

#### 2. API 密钥配置问题
- YouTube API 密钥可能未在 Streamlit Cloud Secrets 中配置
- 导致无法获取视频数据

#### 3. 空数据状态
- 数据库可能没有视频数据
- 导致页面显示空白

## 诊断步骤

### 步骤 1: 检查 Streamlit Cloud 日志
```
1. 访问 Streamlit Cloud 管理页面
2. 找到应用并点击 "Manage app"
3. 查看右侧的 "Logs" 面板
4. 搜索错误关键词：ERROR, Exception, Traceback
```

### 步骤 2: 检查 Secrets 配置
```
1. 在 Streamlit Cloud 管理页面
2. 点击 "Settings" → "Secrets"
3. 检查是否配置了 YOUTUBE_API_KEY
4. 如果没有，添加你的 YouTube API 密钥
```

### 步骤 3: 测试数据库连接
在 Streamlit Cloud 终端或添加调试代码：
```python
import os
import sqlite3

# 检查当前目录
print(f"Current directory: {os.getcwd()}")

# 检查数据库文件
db_path = os.path.join(os.getcwd(), 'youtube_dashboard.db')
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")

# 尝试连接数据库
try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM videos')
    count = cursor.fetchone()[0]
    print(f"Videos in database: {count}")
    conn.close()
except Exception as e:
    print(f"Database error: {e}")
```

### 步骤 4: 检查页面路由
```python
# 添加调试代码查看当前页面
print(f"Current page: {st.session_state.get('current_page', 'overview')}")
print(f"Available pages: {list(st.session_state.keys())}")
```

## 临时修复方案

### 方案 1: 简化页面，添加错误处理
在 dashboard.py 的 main() 函数开头添加：
```python
def main():
    """主函数"""
    try:
        # 渲染侧边栏
        current_page = render_sidebar()
        
        # 添加调试信息
        if st.sidebar.checkbox("显示调试信息"):
            st.write(f"当前页面: {current_page}")
            st.write(f"Session State: {list(st.session_state.keys())}")
            
            # 测试数据库
            try:
                from database import get_videos
                videos = get_videos()
                st.write(f"视频数量: {len(videos)}")
            except Exception as e:
                st.error(f"数据库错误: {e}")
        
        # 应用全局样式
        st.write("YouTube Analytics Dashboard")
        
        # 根据当前页面路由
        if current_page == "overview":
            render_overview()
        elif current_page == "video_management":
            render_video_management()
        elif current_page == "deep_analysis":
            render_deep_analysis()
        elif current_page == "settings":
            render_settings()
        else:
            render_overview()
    
    except Exception as e:
        st.error(f"应用运行错误: {e}")
        import traceback
        st.code(traceback.format_exc())
```

### 方案 2: 先使用测试页面验证
临时将 Streamlit Cloud 的主文件改为 `test_simple.py`，验证基础功能是否正常。

### 方案 3: 检查网络连接
YouTube API 需要 HTTPS 连接：
```python
import requests
response = requests.get('https://www.googleapis.com', timeout=5)
print(f"Network status: {response.status_code}")
```

## 下一步行动

1. **立即执行**: 提交图片参数修复
2. **查看日志**: 在 Streamlit Cloud 查看完整的错误日志
3. **配置 Secrets**: 确保 YouTube API 密钥已配置
4. **添加调试**: 在代码中添加调试输出，定位具体问题

## 预期修复时间
- 图片参数修复: 已完成 ✅
- 日志分析: 需要用户提供日志信息
- 问题定位: 根据日志确定
- 最终修复: 1-2 小时

---

**报告生成时间**: 2026-01-30  
**状态**: 已修复图片参数，等待日志信息
