import streamlit as st
import pandas as pd
import sqlite3

st.title("学生成绩查询")

# 连接数据库
conn = sqlite3.connect("school.db")
cursor = conn.cursor()


def get_grade_list(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grade")
    return [i[0] for i in cursor.fetchall()]


def get_classrooms_by_grade(conn, grade, type):
    cursor.execute(
        "SELECT  名称 FROM classroom WHERE 年级=? AND 科目类型=? order by 名称",
        (grade, type),
    )
    return [i[0] for i in cursor.fetchall()]


def get_students_by_class(conn, grade, class_name):
    cursor.execute(
        "SELECT 学号, 姓名 FROM student WHERE 年级=? AND 班级=?", (grade, class_name)
    )
    return cursor.fetchall()


# 选择年级
grade_list = get_grade_list(conn)
grade = st.selectbox("请选择年级", grade_list)

# 选择班级类别
type = st.selectbox("请选择班级类别", ["物理类", "历史类"])

# 选择班级
class_list = get_classrooms_by_grade(conn, grade, type)
class_name = st.selectbox("请选择班级", class_list)

# 选择学生
student_list = get_students_by_class(conn, grade, class_name)
student = st.selectbox("请选择学生", student_list)

student_id = student[0]

# 查询学生成绩
cursor.execute("SELECT * FROM score WHERE 学号=? ORDER BY 考试编号", (student_id,))
score_list = cursor.fetchall()

# 获取 score 表的列名
column_names = [i[0] for i in cursor.description]

# 创建 DataFrame
df = pd.DataFrame(score_list, columns=column_names)

# 筛选列名
if type == "物理类":
    column_names = [
        "考试编号",
        "考试名称",
        "姓名",
        "语文",
        "数学",
        "英语",
        "物理",
        "化学",
        "生物",
        "总分",
    ]
else:
    column_names = [
        "考试编号",
        "考试名称",
        "姓名",
        "语文",
        "数学",
        "英语",
        "历史",
        "政治",
        "地理",
        "总分",
    ]

df = df[column_names]

st.write("学生成绩")
st.dataframe(df)
