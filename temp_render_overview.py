def render_overview_simplified():
    """数据概览页面 - 精简紧凑版（解决侧边栏不显示问题）"""
    
    st.title("📊 数据概览")
    
    # 导航提示
    st.info("使用左侧导航栏切换页面", icon="🧭")
    
    videos = get_videos()
    
    if not videos:
        st.warning("暂无监控视频，请先添加视频", icon="📊")
        return
    
    # 准备数据
    video_list = []
    for video in videos:
        video_list.append({
            "视频标题": truncate_text(video[1], 30),
            "观看量": video[4] or 0,
            "互动率": calculate_engagement_rate(video[5] or 0, video[6] or 0, video[4] or 0)
        })
    
    df = pd.DataFrame(video_list)
    
    # 核心指标
    total_views = sum([video[4] or 0 for video in videos])
    total_likes = sum([video[5] or 0 for video in videos])
    
    st.write("#### 📈 核心指标")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("总视频数", len(videos))
    col2.metric("总观看量", format_number(total_views))
    col3.metric("总点赞量", format_number(total_likes))
    col4.metric("平均互动率", format_percentage(df["互动率"].mean()))
    
    st.markdown("---")
    
    # 观看趋势
    st.write("#### 📈 观看趋势")
    col1, col2 = st.columns(2)
    
    with col1:
        df_sorted = df.sort_values("观看量", ascending=False).head(10)
        fig = px.bar(df_sorted, x="观看量", y="视频标题", orientation="h", 
                    color="观看量", color_continuous_scale="viridis", height=400)
        fig.update_layout(template="plotly_dark", font=dict(color="#ffffff"))
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        df_engagement = df.sort_values("互动率", ascending=False).head(10)
        fig = px.bar(df_engagement, x="互动率", y="视频标题", orientation="h",
                    color="互动率", color_continuous_scale="plasma", height=400)
        fig.update_layout(template="plotly_dark", font=dict(color="#ffffff"))
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("---")
    
    # 数据导出
    st.write("#### 📥 数据导出")
    csv = df.to_csv(index=False)
    st.download_button("下载 CSV", csv, "youtube_dashboard_data.csv", "text/csv")
