import streamlit as st
import pandas as pd
import sqlite3


# 连接数据库
conn = sqlite3.connect("school.db")
cursor = conn.cursor()

st.title("考试管理")

# 创建考试表
cursor.execute(
    """CREATE TABLE IF NOT EXISTS exams (
                    编号 TEXT PRIMARY KEY,
                    名称 TEXT NOT NULL,              
                    年级 TEXT NOT NULL)"""
)

conn.commit()


# 创建成绩表
cursor.execute(
    """CREATE TABLE IF NOT EXISTS scores (
                    编号 TEXT PRIMARY KEY,
                    考试编号 TEXT NOT NULL, 
                    考试名称 TEXT NOT NULL,
                    年级 INTEGER NOT NULL,
                    班级 INTEGER NOT NULL,             
                    学号 TEXT NOT NULL, 
                    姓名 TEXT NOT NULL,
                    语文 REAL NOT NULL, 
                    语文班名次 INTEGER NOT NULL,
                    语文校名次 INTEGER NOT NULL,
                    数学 REAL NOT NULL,
                    数学班名次 INTEGER NOT NULL,
                    数学校名次 INTEGER NOT NULL,
                    英语 REAL NOT NULL,
                    英语班名次 INTEGER NOT NULL,
                    英语校名次 INTEGER NOT NULL,
                    物理 REAL NOT NULL,
                    物理班名次 INTEGER NOT NULL,
                    物理校名次 INTEGER NOT NULL,
                    化学 REAL NOT NULL,
                    化学赋分 REAL NOT NULL,
                    化学班名次 INTEGER NOT NULL,
                    化学校名次 INTEGER NOT NULL,
                    生物 REAL NOT NULL,
                    生物赋分 REAL NOT NULL,
                    生物班名次 INTEGER NOT NULL,
                    生物校名次 INTEGER NOT NULL,
                    历史 REAL NOT NULL,
                    历史班名次 INTEGER NOT NULL,
                    历史校名次 INTEGER NOT NULL,
                    政治 REAL NOT NULL,
                    政治赋分 REAL NOT NULL,
                    政治班名次 INTEGER NOT NULL,
                    政治校名次 INTEGER NOT NULL,
                    地理 REAL NOT NULL,
                    地理赋分 REAL NOT NULL,
                    地理班名次 INTEGER NOT NULL,
                    地理校名次 INTEGER NOT NULL,
                    总分 REAL NOT NULL,
                    总分班名次 INTEGER NOT NULL,
                    总分校名次 INTEGER NOT NULL)"""
)
conn.commit()
