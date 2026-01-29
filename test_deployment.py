import streamlit as st

st.title("测试页面")
st.write("如果能看到这个页面，说明 Streamlit Cloud 部署成功！")

st.write("---")
st.write("### 部署信息")
st.write(f"- 提交: `git log -1 --pretty=format:%h`")
st.write(f"- 时间: `date`")
st.write(f"- Python 版本: `python --version`")

st.write("---")
st.success("✅ Streamlit Cloud 部署成功！")
