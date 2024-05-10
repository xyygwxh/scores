import streamlit as st
import pandas as pd
import sqlite3


# 辅助函数
def get_grade_list():
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT 年级 FROM student")
    return [i[0] for i in cursor.fetchall()]


def get_classrooms_by_grade(grade):
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute(
        "SELECT DISTINCT 班级 FROM student WHERE 年级=? ORDER BY 班级", (grade,)
    )
    return [i[0] for i in cursor.fetchall()]


# 各个功能的实现
def display_students():
    st.subheader("学生表")
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS student
    (学号 TEXT PRIMARY KEY,
    姓名 TEXT NOT NULL, 
    性别 TEXT NOT NULL, 
    年级 INTEGER NOT NULL, 
    班级 INTEGER NOT NULL)
    """
    )
    conn.commit()
    sql = "SELECT * FROM student"
    df = pd.read_sql_query(sql, conn)
    st.dataframe(df, use_container_width=True)

    # 将 df 导出 excel 文件
    if st.button("导出"):
        df.to_excel("student.xlsx", index=False)


def import_students():
    st.subheader("导入学生表")
    file = st.file_uploader("上传学生表", type=["xlsx"])
    if file:
        df = pd.read_excel(file)
        conn = sqlite3.connect("school.db")
        df.to_sql("student", conn, if_exists="replace", index=False)
        st.success("导入成功")


def search_students():
    st.subheader("查找学生")
    id_or_name = st.text_input("学号或姓名")
    if st.button("查找"):
        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM student WHERE 学号=? OR 姓名=?", (id_or_name, id_or_name)
        )
        students = cursor.fetchall()
        if students:
            st.success("找到学生")
            df = pd.DataFrame(
                students, columns=["学号", "姓名", "性别", "年级", "班级"]
            )
            st.dataframe(df)
        else:
            st.error("未找到学生")


def add_students():
    st.subheader("添加学生")
    id = st.text_input("学号", max_chars=18)
    name = st.text_input("姓名")
    gender = st.selectbox("性别", ["男", "女"])
    grade = st.selectbox("年级", get_grade_list())
    classroom = st.selectbox("班级", get_classrooms_by_grade(grade))
    if st.button("添加"):
        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO student VALUES (?, ?, ?, ?, ?)",
            (id, name, gender, grade, classroom),
        )
        conn.commit()
        st.success("添加成功")
        display_students()  # 重新显示学生表


def delete_students():
    st.subheader("删除学生")
    student_id = st.text_input("学号")
    if st.button("删除"):
        conn = sqlite3.connect("school.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM student WHERE 学号=?", (student_id,))
        conn.commit()
        if cursor.rowcount == 1:
            st.success("删除成功")
        else:
            st.error("未找到学生")


def update_students():
    st.subheader("更新学生信息")
    grades = get_grade_list()
    grade = st.selectbox("年级", grades, key="grade1")
    classrooms = get_classrooms_by_grade(grade)
    classroom = st.selectbox("班级", classrooms, key="classroom1")
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    students = cursor.execute(
        "SELECT * FROM student WHERE 年级=? AND 班级=?", (grade, classroom)
    ).fetchall()
    student = st.selectbox("学生", students)
    id, name, gender, _, _ = student
    new_name = st.text_input("姓名", name)
    new_gender = st.selectbox("性别", ["男", "女"], index=(0 if gender == "男" else 1))
    if st.button("更新"):
        cursor.execute(
            "UPDATE student SET 姓名=?, 性别=? WHERE 学号=?", (new_name, new_gender, id)
        )
        conn.commit()
        st.success("更新成功")
        display_students()  # 重新显示学生表


def student_manage():
    tab_functions = {
        "学生表": display_students,
        "导入": import_students,
        "查找": search_students,
        "添加": add_students,
        "删除": delete_students,
        "更新": update_students,
    }
    tabs = st.tabs(list(tab_functions.keys()))

    for tab, func in zip(tabs, tab_functions.values()):
        with tab:
            func()
