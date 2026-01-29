"""
UI 样式管理
定义全局 CSS 样式，融合 Adjust 和 Apple 设计风格
"""

def get_custom_styles():
    """获取自定义 CSS 样式"""
    return """
    <style>
    /* ==================== 全局样式 ==================== */
    
    /* 深色主题背景 */
    .stApp {
        background: linear-gradient(135deg, #0a0e27 0%, #16213e 100%);
        color: #ffffff;
    }
    
    /* 主容器 */
    .main .block-container {
        max-width: 1400px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    
    /* ==================== 侧边栏样式 ==================== */
    
    /* 侧边栏背景 */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #16213e 0%, #1a1a2e 100%) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* 隐藏 Streamlit 默认侧边栏装饰 */
    section[data-testid="stSidebar"] > div:first-child {
        display: none;
    }
    
    /* 优化按钮样式 */
    .stButton > button {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: #b8c1ec !important;
        padding: 0.75rem 1rem !important;
        font-weight: 500 !important;
        text-align: left !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
    }
    
    .stButton > button:hover {
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: rgba(102, 126, 234, 0.3) !important;
        color: #ffffff !important;
        transform: translateX(4px);
    }
    
    /* ==================== 卡片样式 ==================== */
    
    .metric-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 30px rgba(0, 0, 0, 0.2);
        border-color: rgba(102, 126, 234, 0.3);
    }
    
    /* ==================== 主要按钮样式 ==================== */
    
    div[data-testid="stForm"] .stButton > button,
    .stButton > button[type="submit"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.6rem 1.5rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3) !important;
    }
    
    div[data-testid="stForm"] .stButton > button:hover,
    .stButton > button[type="submit"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
    }
    
    /* ==================== 输入框样式 ==================== */
    
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 8px !important;
        color: #ffffff !important;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1) !important;
    }
    
    /* ==================== 标题样式 ==================== */
    
    h1 {
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        background: linear-gradient(135deg, #ffffff 0%, #b8c1ec 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    h2 {
        font-size: 1.75rem;
        font-weight: 600;
        margin: 1.5rem 0 1rem 0;
        color: #ffffff;
    }
    
    h3 {
        font-size: 1.25rem;
        font-weight: 600;
        margin: 1rem 0 0.75rem 0;
        color: #b8c1ec;
    }
    
    /* ==================== 分隔线样式 ==================== */
    
    hr {
        border: none;
        height: 1px;
        background: linear-gradient(90deg, 
            rgba(255, 255, 255, 0) 0%, 
            rgba(255, 255, 255, 0.2) 50%, 
            rgba(255, 255, 255, 0) 100%);
        margin: 2rem 0;
    }
    
    /* ==================== 数据表格样式 ==================== */
    
    .stDataFrame {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        overflow: hidden;
    }
    
    .stDataFrame table {
        width: 100%;
        border-collapse: collapse;
    }
    
    .stDataFrame th {
        background: rgba(102, 126, 234, 0.2) !important;
        color: #ffffff !important;
        font-weight: 600;
        padding: 1rem;
        text-align: left;
    }
    
    .stDataFrame td {
        padding: 0.75rem 1rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
        color: #ffffff;
    }
    
    .stDataFrame tr:hover {
        background: rgba(255, 255, 255, 0.05);
    }
    
    /* ==================== 成功/警告/错误框样式 ==================== */
    
    .stSuccess {
        background: linear-gradient(135deg, rgba(67, 233, 123, 0.1) 0%, rgba(56, 249, 215, 0.1) 100%);
        border-left: 4px solid #43e97b;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stWarning {
        background: linear-gradient(135deg, rgba(255, 159, 64, 0.1) 0%, rgba(255, 69, 0, 0.1) 100%);
        border-left: 4px solid #ff9f40;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stError {
        background: linear-gradient(135deg, rgba(255, 107, 107, 0.1) 0%, rgba(220, 38, 38, 0.1) 100%);
        border-left: 4px solid #ff6b6b;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .stInfo {
        background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
        border-left: 4px solid #667eea;
        border-radius: 8px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    /* ==================== Metric 样式优化 ==================== */
    
    [data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #b8c1ec !important;
        font-size: 1rem !important;
        font-weight: 500 !important;
    }
    
    /* ==================== 图表样式 ==================== */
    
    .js-plotly-plot {
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        border-radius: 12px !important;
        padding: 1rem;
    }
    
    /* ==================== 动画效果 ==================== */
    
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .animate-fade-in {
        animation: fadeIn 0.5s ease-out;
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.5;
        }
    }
    
    .animate-pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* ==================== 响应式设计 ==================== */
    
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1rem;
        }
        
        h1 {
            font-size: 1.75rem;
        }
        
        h2 {
            font-size: 1.25rem;
        }
        
        .metric-card {
            padding: 1rem;
        }
    }
    </style>
    """


def get_sidebar_styles():
    """获取侧边栏专用样式"""
    return """
    <style>
    /* 隐藏 Streamlit 默认侧边栏元素 */
    [data-testid="stSidebar"] > div:first-child {
        display: none !important;
    }
    
    /* 侧边栏内容容器 */
    [data-testid="stSidebar"] > div:nth-child(2) {
        padding: 0 !important;
    }
    </style>
    """
