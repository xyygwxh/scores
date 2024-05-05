import streamlit as st
import pandas as pd
import sqlite3

st.title("班级成绩查询")

# 连接数据库
conn = sqlite3.connect("school.db")
cursor = conn.cursor()


def get_grade_list(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grade")
    return [i[0] for i in cursor.fetchall()]


def get_classrooms_by_grade(conn, grade):
    cursor.execute(
        "SELECT DISTINCT 班级 FROM student WHERE 年级=? order by 班级", (grade,)
    )
    return [i[0] for i in cursor.fetchall()]


def get_exam_list_by_grade(conn, grade):
    cursor.execute(
        "SELECT DISTINCT 名称 FROM exam WHERE 年级=? order by 编号", (grade,)
    )
    return [i[0] for i in cursor.fetchall()]


grade_list = get_grade_list(conn)
grade = st.selectbox("请选择年级", grade_list)


class_list = get_classrooms_by_grade(conn, grade)
class_name = st.selectbox("请选择班级", class_list)

exam_list = get_exam_list_by_grade(conn, grade)
exam_name = st.selectbox("请选择考试", exam_list)


cursor.execute(
    "SELECT * FROM score WHERE 考试名称 = ? AND 年级 = ? AND 班级 = ?",
    (exam_name, grade, class_name),
)
result = cursor.fetchall()

# 获取列名
column_names = [i[0] for i in cursor.description]

# 创建DataFrame
df = pd.DataFrame(result, columns=column_names)
st.dataframe(df)
