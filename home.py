import streamlit as st
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader
from admin.admin import admin_manage

# 设置页面配置
st.set_page_config(page_title="scores", page_icon=":books:", layout="wide")


def index():
    st.title("Home")
    st.write("欢迎使用学生成绩查询系统")
    st.page_link("pages/1_学生成绩查询.py", icon="1️⃣")
    st.page_link("pages/2_班级成绩查询.py", icon="2️⃣")


with open(".streamlit/config.yaml", "r", encoding="utf-8") as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config["credentials"],
    config["cookie"]["name"],
    config["cookie"]["key"],
    config["cookie"]["expiry_days"],
)

authenticator.login()

if st.session_state["authentication_status"]:
    authenticator.logout("退出", "sidebar", key="sidebar")
elif st.session_state["authentication_status"] is False:
    st.error("用户名或密码错误")
elif st.session_state["authentication_status"] is None:
    st.warning("请输入用户名和密码")


if st.session_state["username"] == "admin":
    admin_manage()
elif st.session_state["username"] == "xyyg":
    index()
    authenticator.logout("退出", "main", key="main")
