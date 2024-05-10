import streamlit as st
import pandas as pd
import sqlite3


def show_grade_table():
    st.subheader("年级表")
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS grade (
            编号 INTEGER PRIMARY KEY,
            名称 TEXT NOT NULL
        )
        """
    )
    conn.commit()

    grade_list = cursor.execute("SELECT * FROM grade").fetchall()
    if grade_list:
        df = pd.DataFrame(grade_list, columns=["编号", "名称"])
        st.dataframe(df, use_container_width=True)
    else:
        st.info("暂无年级")


def add_grade():
    st.subheader("添加年级")
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    id = st.number_input("年级编号", value=2021, step=1, key="id")
    name = f"{id}级"
    if st.button("添加"):
        cursor.execute("SELECT * FROM grade WHERE 编号=?", (id,))
        if cursor.fetchone():
            st.error("该年级已存在")
        else:
            cursor.execute("INSERT INTO grade (编号, 名称) VALUES (?, ?)", (id, name))
            conn.commit()
            st.success("添加成功")
            st.experimental_rerun()


def delete_grade():
    st.subheader("删除年级")
    conn = sqlite3.connect("school.db")
    cursor = conn.cursor()
    id_to_delete = st.number_input("年级编号", value=2021, step=1, key="id_to_delete")
    if st.button("删除"):
        cursor.execute("SELECT * FROM grade WHERE 编号=?", (id_to_delete,))
        if not cursor.fetchone():
            st.error("该年级不存在")
        else:
            cursor.execute("DELETE FROM grade WHERE 编号=?", (id_to_delete,))
            conn.commit()
            st.success("删除成功")
            st.experimental_rerun()


def grade_manage():
    tabs = st.tabs(["年级表", "添加年级", "删除年级"])
    with tabs[0]:
        show_grade_table()
    with tabs[1]:
        add_grade()
    with tabs[2]:
        delete_grade()
