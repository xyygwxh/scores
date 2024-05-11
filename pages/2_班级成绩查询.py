import streamlit as st
import pandas as pd
import sqlite3

if not st.session_state["authentication_status"]:
    st.switch_page("home.py")

st.title("班级成绩查询")

# 连接数据库
conn = sqlite3.connect("school.db")
cursor = conn.cursor()


def get_grade_list(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM grade")
    return [i[0] for i in cursor.fetchall()]


def get_classrooms_by_grade(conn, grade, type):
    cursor.execute(
        "SELECT DISTINCT 名称 FROM classroom WHERE 年级=? AND 科目类型=? order by 名称",
        (grade, type),
    )
    return [i[0] for i in cursor.fetchall()]


def get_exam_list_by_grade(conn, grade):
    cursor.execute(
        "SELECT DISTINCT 名称 FROM exam WHERE 年级=? order by 编号", (grade,)
    )
    return [i[0] for i in cursor.fetchall()]


# 选择年级
grade_list = get_grade_list(conn)
grade = st.selectbox("请选择年级", grade_list)

# 选择科目类型
type = st.selectbox("请选择科目类型", ["物理类", "历史类"])

# 选择班级
class_list = get_classrooms_by_grade(conn, grade, type)
class_name = st.selectbox("请选择班级", class_list)

# 选择考试
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
df.set_index("姓名", inplace=True)

if type == "物理类":
    df = df[["语文", "英语", "数学", "物理", "化学", "生物", "总分"]]
else:
    df = df[["语文", "英语", "数学", "历史", "政治", "地理", "总分"]]
st.dataframe(df, use_container_width=True)
