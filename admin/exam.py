import streamlit as st
import pandas as pd
import sqlite3
import time



def get_grade_list():
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grade")
    return [i[0] for i in cursor.fetchall()]


def display_exam_table():
    st.subheader("考试表")
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()

    # 创建考试表
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS exam (
                        编号 TEXT PRIMARY KEY,
                        名称 TEXT NOT NULL,              
                        年级 TEXT NOT NULL)"""
    )
    conn.commit()

    # 创建成绩表
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS score (
                        编号 INTEGER PRIMARY KEY,
                        考试编号 TEXT NOT NULL, 
                        考试名称 TEXT NOT NULL,
                        年级 INTEGER NOT NULL,
                        班级 INTEGER NOT NULL,             
                        学号 TEXT NOT NULL, 
                        姓名 TEXT NOT NULL,
                        语文 REAL , 
                        语文班名次 INTEGER,
                        语文校名次 INTEGER,
                        数学 REAL,
                        数学班名次 INTEGER,
                        数学校名次 INTEGER,
                        英语 REAL,
                        英语班名次 INTEGER,
                        英语校名次 INTEGER,
                        物理 REAL,
                        物理班名次 INTEGER,
                        物理校名次 INTEGER,
                        化学 REAL,
                        化学赋分 REAL,
                        化学班名次 INTEGER,
                        化学校名次 INTEGER,
                        生物 REAL,
                        生物赋分 REAL,
                        生物班名次 INTEGER,
                        生物校名次 INTEGER,
                        历史 REAL,
                        历史班名次 INTEGER,
                        历史校名次 INTEGER,
                        政治 REAL,
                        政治赋分 REAL,
                        政治班名次 INTEGER,
                        政治校名次 INTEGER,
                        地理 REAL,
                        地理赋分 REAL,
                        地理班名次 INTEGER,
                        地理校名次 INTEGER,
                        总分 REAL,
                        总分班名次 INTEGER,
                        总分校名次 INTEGER,
                        UNIQUE(考试编号, 学号))"""
    )
    conn.commit()

    cursor.execute("SELECT * FROM exam")
    data = cursor.fetchall()
    if data:
        df = pd.DataFrame(data, columns=["编号", "名称", "年级"])
        st.dataframe(df)
    else:
        st.warning("考试表为空")

def add_exam():
    st.subheader("添加考试")
    date_str = st.date_input("考试日期").strftime("%Y-%m-%d")
    name = st.text_input("考试名称")
    grade = st.selectbox("年级", get_grade_list())
    
    # 导入学生成绩
    file1 = st.file_uploader("上传物理类学生成绩", type=["xlsx"])
    file2 = st.file_uploader("上传历史类学生成绩", type=["xlsx"])
    if file1 and file2:
        df1 = pd.read_excel(file1)
        df2 = pd.read_excel(file2)
        df = pd.concat([df1, df2])
        if st.button("确认导入"):
            df["考试编号"] = date_str
            df["考试名称"] = name
            df["年级"] = grade

            # 添加成绩表数据
            conn = sqlite3.connect("school.db")
            df.to_sql("score", conn, if_exists="append", index=False)

            # 添加考试表数据
            cursor = conn.cursor()
            cursor.execute("INSERT INTO exam VALUES (?, ?, ?)", (date_str, name, grade))
            conn.commit()
            st.success("导入成功")
            time.sleep(2)
            st.experimental_rerun()

def delete_exam():
    st.subheader("删除考试")

    # 选择年级
    grade = st.selectbox("年级", get_grade_list(), key="grade2")

    # 获取考试列表
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM exam WHERE 年级=?", (grade,))
    exam_list = cursor.fetchall()
    exam_name = st.selectbox("考试", [i[1] for i in exam_list])
    if st.button("删除"):
        cursor.execute("DELETE FROM exam WHERE 名称=? AND 年级=?", (exam_name, grade))
        conn.commit()
        # 判断数据库操作是否成功
        if cursor.rowcount == 0:
            st.error("考试表删除失败")
        else:
            st.success("考试表删除成功")

        # 删除成绩表数据
        cursor.execute(
            "DELETE FROM score WHERE 考试名称=? AND 年级=?", (exam_name, grade)
        )
        conn.commit()
        if cursor.rowcount == 0:
            st.error("成绩表删除失败")
        else:
            st.success("成绩表删除成功")

        # 显示考试表
        cursor.execute("SELECT * FROM exam")
        data = cursor.fetchall()
        if data:
            df = pd.DataFrame(data, columns=["编号", "名称", "年级"])
            st.dataframe(df)
        else:
            st.warning("考试表为空")
        st.experimental_rerun()

def exam_manage():
    tabs = st.tabs(["考试表", "添加考试", "删除考试"])
    with tabs[0]:
        display_exam_table()
    with tabs[1]:
        add_exam()
    with tabs[2]:
        delete_exam()

