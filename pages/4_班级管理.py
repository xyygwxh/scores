import streamlit as st
import pandas as pd
import sqlite3


# 连接数据库
conn = sqlite3.connect("school.db")
cursor = conn.cursor()

st.title("班级管理")

# 创建班级表
cursor.execute(
    """CREATE TABLE IF NOT EXISTS classroom
            (编号 INTEGER PRIMARY KEY ,
            名称 INTEGER NOT NULL,
            年级 INTEGER NOT NULL,
            科目类型 TEXT NOT NULL,
            层级 TEXT NOT NULL)"""
)

# 显示班级表
st.divider()
st.subheader("班级表")
st.dataframe(pd.read_sql("SELECT * FROM classroom", conn), use_container_width=True)


# 从excel文件导入班级表
st.divider()
st.subheader("导入班级")
df = st.file_uploader("选择班级表", type=["xlsx"])
if df is not None:
    df = pd.read_excel(df)
    df.to_sql("classroom", conn, if_exists="replace", index=False)
    st.success("班级表导入成功")
    st.dataframe(df, use_container_width=True)


# 添加班级
st.divider()
st.subheader("添加班级")
st.write("请在下方输入班级信息")

cursor.execute("SELECT * FROM grade")  # 打开年级表
grade_list = cursor.fetchall()  # 获取年级
grades = [i[0] for i in grade_list]
name = st.number_input("名称", min_value=1, max_value=50)
grade = st.selectbox("年级", grades, key="grade1")
id = st.number_input("编号", grade * 100 + name, disabled=True)
subject = st.selectbox("科目类型", ["物理类", "历史类"])
level = st.selectbox("层级", ["A", "B"])

# 判断班级是否存在
cursor.execute("SELECT * FROM classroom WHERE 编号 = ?", (id,))
if cursor.fetchone():
    st.error("班级已存在")
else:
    if st.button("添加"):
        cursor.execute(
            "INSERT INTO classroom (名称, 年级,编号, 科目类型, 层级) VALUES (?, ?, ?,?, ?)",
            (name, grade, id, subject, level),
        )
        conn.commit()
        st.success("班级添加成功")
        st.dataframe(pd.read_sql("SELECT * FROM classroom", conn))

# 删除班级
st.divider()
st.subheader("删除班级")

cursor.execute("SELECT * FROM grade")  # 打开年级表
grade_list = cursor.fetchall()  # 获取年级
grades = [i[0] for i in grade_list]
grade = st.selectbox("年级", grades, key="grade2")

cursor.execute("SELECT * FROM classroom where 年级=?", (grade,))
classrooms = cursor.fetchall()
classrooms = [i[0] for i in classrooms]

classroom_id = st.selectbox("班级", classrooms)

if st.button("删除"):
    cursor.execute("DELETE FROM classroom WHERE 编号 = ?", (classroom_id,))
    conn.commit()
    st.success("班级删除成功")
    st.dataframe(pd.read_sql("SELECT * FROM classroom", conn))

# 修改班级
st.divider()
st.subheader("修改班级")

cursor.execute("SELECT * FROM grade")  # 打开年级表
grade_list = cursor.fetchall()  # 获取年级
grades = [i[0] for i in grade_list]
grade = st.selectbox("年级", grades, key="grade3")

cursor.execute("SELECT * FROM classroom where 年级=?", (grade,))
classrooms = cursor.fetchall()
classrooms = [i[0] for i in classrooms]

classroom_id = st.selectbox("班级", classrooms, key="classroom_id")
subject = st.selectbox("科目类型", ["物理类", "历史类"], key="subject2")
level = st.selectbox("层级", ["A", "B"], key="level2")

if classroom_id and subject and level:
    if st.button("修改"):
        cursor.execute(
            "UPDATE classroom SET 科目类型 = ?, 层级 = ? WHERE 编号 = ?",
            (subject, level, classroom_id),
        )
        conn.commit()
        st.success("班级修改成功")
        st.dataframe(pd.read_sql("SELECT * FROM classroom", conn))
else:
    st.warning("请选择班级")
