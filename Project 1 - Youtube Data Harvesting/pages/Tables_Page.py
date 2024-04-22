import googleapiclient.discovery
import streamlit as st
import mysql.connector
import pandas as pd

# SQL Connection

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database = "Project_1"
)
mycursor = mydb.cursor()

st.set_page_config(page_title="Tables_Page", page_icon=":tada:", layout="wide")

with st.container():
    st.header("VIEW TABLES")
    l_col, r_col= st.columns([2, 2])
    with l_col:
        option = st.selectbox("Select the option to view the tables",("Channel Table", "Video Table", "Comments Table"),index=None,placeholder="Select a table")

def channel_table():
        mycursor.execute("SELECT * FROM Channels_Table")
        channel_data = mycursor.fetchall()
        df = pd.DataFrame(channel_data, columns = mycursor.column_names)
        st.dataframe(df)

def video_table():
        mycursor.execute("SELECT * FROM Videos_Table ORDER BY Channel_Name")
        video_data = mycursor.fetchall()
        df1 = pd.DataFrame(video_data, columns = mycursor.column_names)
        st.dataframe(df1)

def comments_table():
        mycursor.execute("SELECT * FROM Comments_Table")
        comments_data = mycursor.fetchall()
        df2 = pd.DataFrame(comments_data, columns = mycursor.column_names)
        st.dataframe(df2)

if option == "Channel Table":
    channel_table()

if option == "Video Table":
    video_table()

if option == "Comments Table":
    comments_table()