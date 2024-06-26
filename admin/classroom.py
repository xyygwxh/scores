import streamlit as st
import pandas as pd
import sqlite3


def get_grade_list():
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grade")
    return [i[0] for i in cursor.fetchall()]


def get_classrooms_by_grade(grade):
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classroom WHERE 年级=?", (grade,))
    return [i[0] for i in cursor.fetchall()]


# 主要功能定义
def display_class_table():
    st.subheader("班级表")
    conn = sqlite3.connect("school.db")
    st.dataframe(pd.read_sql("SELECT * FROM classroom", conn), use_container_width=True)


def import_classroom():
    st.subheader("导入班级")
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS classroom (
        编号 INTEGER,
        年级 INTEGER,
        名称 INTEGER,
        科目类型 TEXT,
        层级 TEXT)"""
    )
    conn.commit()
    df = st.file_uploader("选择班级表", type=["xlsx"])
    if df is not None:
        df = pd.read_excel(df)
        df.to_sql("classroom", conn, if_exists="replace", index=False)
        st.success("班级表导入成功")
        st.dataframe(df, use_container_width=True)


def add_classroom():
    st.subheader("添加班级")
    grades = get_grade_list()
    grade = st.selectbox("年级", grades, key="add_grade")
    name = st.number_input("名称", min_value=1, max_value=50)
    id = st.number_input("编号", grade * 100 + name, disabled=True)
    subject = st.selectbox("科目类型", ["物理类", "历史类"])
    level = st.selectbox("层级", ["A", "B"])
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classroom WHERE 编号 = ?", (id,))
    if cursor.fetchone():
        st.error("班级已存在")
    else:
        if st.button("添加"):
            cursor.execute(
                "INSERT INTO classroom (名称, 年级, 编号, 科目类型, 层级) VALUES (?, ?, ?, ?, ?)",
                (name, grade, id, subject, level),
            )
            conn.commit()
            st.success("班级添加成功")
            display_class_table()


def delete_classroom():
    st.subheader("删除班级")
    grade = st.selectbox("年级", get_grade_list(), key="delete_grade")
    classrooms = get_classrooms_by_grade(grade)
    classroom_id = st.selectbox("班级", classrooms)

    if st.button("删除"):
        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM classroom WHERE 编号 = ?", (classroom_id,))
        conn.commit()
        st.success("班级删除成功")
        display_class_table()


def update_classroom():
    st.subheader("修改班级")
    grade = st.selectbox("年级", get_grade_list(), key="update_grade")
    classrooms = get_classrooms_by_grade(grade)
    classroom_id = st.selectbox("班级", classrooms, key="update_classroom_id")
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM classroom WHERE 编号 = ?", (classroom_id,))
    classroom = cursor.fetchone()
    subject = st.selectbox(
        "科目类型",
        ["物理类", "历史类"],
        key="update_subject",
        index=0 if classroom[3] == "物理类" else 1,
    )
    level = st.selectbox(
        "层级",
        ["A", "B"],
        key="update_level",
        index=0 if classroom[4] == "A" else 1,
    )

    if classroom_id and subject and level:
        if st.button("修改"):
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE classroom SET 科目类型 = ?, 层级 = ? WHERE 编号 = ?",
                (subject, level, classroom_id),
            )
            conn.commit()
            st.success("班级修改成功")
            display_class_table()
    else:
        st.warning("请选择班级")


def classroom_manage():

    # 使用 st.tabs 组织功能
    tab_functions = {
        "班级表": display_class_table,
        "导入": import_classroom,
        "添加": add_classroom,
        "删除": delete_classroom,
        "更新": update_classroom,
    }

    tabs = st.tabs(list(tab_functions.keys()))

    for tab, func in zip(tabs, tab_functions.values()):
        with tab:
            func()
