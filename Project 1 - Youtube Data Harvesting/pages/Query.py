import googleapiclient.discovery
import streamlit as st
import mysql.connector
import pandas as pd
from tabulate import tabulate

# SQL Connection

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database = "Project_1"
)
mycursor = mydb.cursor()

st.set_page_config(page_title="Query_Page", page_icon=":tada:", layout="wide")

# CSS

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

local_css("style/style.css")

with st.container():
    st.header("QUESTIONS AND ANSWERS")
    option = st.selectbox("Select any question",
                            (
                                "1. What are the names of all the videos and their corresponding channels?",
                                "2. Which channels have the most number of videos, and how many videos do they have?",
                                "3. What are the top 10 most viewed videos and their respective channels?",
                                "4. How many comments were made on each video, and what are their corresponding video names?",
                                "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
                                "6. What is the total number of likes for each video, and what are their corresponding video names?",
                                "7. What is the total number of views for each channel, and what are their corresponding channel names?",
                                "8. What are the names of all the channels that have published videos in the year 2022?",
                                "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
                                "10. Which videos have the highest number of comments, and what are their corresponding channel names?"
                            ),
                            index=None,placeholder="Select any question")

if option == "1. What are the names of all the videos and their corresponding channels?":
    mycursor.execute("SELECT Channel_Name,Video_Name FROM Videos_Table ORDER BY Channel_Name")
    que1=mycursor.fetchall()
    df1 = pd.DataFrame(que1, columns = mycursor.column_names)
    st.dataframe(df1)

elif option == "2. Which channels have the most number of videos, and how many videos do they have?":
    mycursor.execute("SELECT Channel_Name, Total_Videos FROM Channels_Table ORDER BY Total_Videos DESC")
    que2=mycursor.fetchall()
    df2 = pd.DataFrame(que2, columns = mycursor.column_names)
    st.dataframe(df2)

elif option == "3. What are the top 10 most viewed videos and their respective channels?":
    mycursor.execute("SELECT Channel_Name, Video_Name, View_Count FROM Videos_Table ORDER BY View_Count DESC LIMIT 10")
    que3=mycursor.fetchall()
    df3 = pd.DataFrame(que3, columns = mycursor.column_names)
    st.dataframe(df3)

elif option == "4. How many comments were made on each video, and what are their corresponding video names?":
    mycursor.execute("SELECT Video_Name, Comment_Counts FROM Videos_Table")
    que4=mycursor.fetchall()
    df4 = pd.DataFrame(que4, columns = mycursor.column_names)
    st.dataframe(df4)

elif option == "5. Which videos have the highest number of likes, and what are their corresponding channel names?":
    mycursor.execute("SELECT Channel_Name, Video_Name, Like_Count FROM  Videos_Table ORDER BY Like_Count Desc")
    que5=mycursor.fetchall()
    df5 = pd.DataFrame(que5, columns = mycursor.column_names)
    st.dataframe(df5)

elif option == "6. What is the total number of likes for each video, and what are their corresponding video names?":
    mycursor.execute("SELECT Video_Name, Like_count FROM Videos_Table")
    que6=mycursor.fetchall()
    df6 = pd.DataFrame(que6, columns = mycursor.column_names)
    st.dataframe(df6)

elif option == "7. What is the total number of views for each channel, and what are their corresponding channel names?":
    mycursor.execute("SELECT Channel_Name, Views FROM Channels_Table")
    que7=mycursor.fetchall()
    df7 = pd.DataFrame(que7, columns = mycursor.column_names)
    st.dataframe(df7)

elif option == "8. What are the names of all the channels that have published videos in the year 2022?":
    mycursor.execute("SELECT Channel_Name, Published_At AS Published_in_2022 FROM Videos_Table WHERE extract(year FROM Published_At)=2022")
    que8=mycursor.fetchall()
    df8 = pd.DataFrame(que8, columns = mycursor.column_names)
    st.dataframe(df8)

elif option == "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?":
    mycursor.execute("SELECT Channel_Name, AVG(Duration) AS Average_Duration FROM Videos_Table GROUP BY Channel_Name")
    que9=mycursor.fetchall()
    df9 = pd.DataFrame(que9, columns = mycursor.column_names)
    st.dataframe(df9)

elif option == "10. Which videos have the highest number of comments, and what are their corresponding channel names?":
    mycursor.execute("SELECT Channel_Name, Video_name, Comment_counts FROM Videos_Table ORDER BY Comment_counts Desc")
    que10=mycursor.fetchall()
    df10 = pd.DataFrame(que10, columns = mycursor.column_names)
    st.dataframe(df10)