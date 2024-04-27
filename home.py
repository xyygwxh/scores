import streamlit as st

st.title("Home")

st.write(
    """
欢迎使用学生成绩查询系统。
"""
)
st.page_link("pages/1_学生成绩查询.py", icon="1️⃣")
st.page_link("pages/2_班级成绩查询.py", icon="2️⃣")
st.page_link("pages/3_年级管理.py", icon="3️⃣")
st.page_link("pages/4_班级管理.py", icon="4️⃣")
st.page_link("pages/5_学生管理.py", icon="5️⃣")
st.page_link("pages/6_考试管理.py", icon="6️⃣")
