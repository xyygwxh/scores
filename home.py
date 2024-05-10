import streamlit as st

st.title("Home")

st.write(
    """
欢迎使用学生成绩查询系统。
"""
)
st.page_link("pages/1_学生成绩查询.py", icon="1️⃣")
st.page_link("pages/2_班级成绩查询.py", icon="2️⃣")
st.page_link("pages/3_管理.py", icon="3️⃣")

