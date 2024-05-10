import streamlit as st
from streamlit_option_menu import option_menu
from manage.classroom import classroom_manage
from manage.grade import grade_manage


# 侧边栏显示站点管理导航菜单
with st.sidebar:
    selected = option_menu(
        "站点管理",
        ["年级管理", "班级管理", "学生管理", "考试管理"],
        icons=["house", "gear", "gear", "gear"],
        menu_icon="cast",
        default_index=1,
    )

if selected == "年级管理":
    grade_manage()
elif selected == "班级管理":
    classroom_manage()
elif selected == "学生管理":
    pass
elif selected == "考试管理":
    pass
