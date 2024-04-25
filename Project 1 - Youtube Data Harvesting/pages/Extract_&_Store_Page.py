import googleapiclient.discovery
import streamlit as st
import mysql.connector
import base64
from datetime import datetime

# API 

api_service_name = "youtube"
api_version = "v3"
api_key = ""
youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=api_key)

# SQL Connection

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database = "Project_1"
)
mycursor = mydb.cursor()


st.set_page_config(page_title="Extract_Page", page_icon=":tada:", layout="wide")

# CSS 

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")

# To get Channel data

def channel_data(channel_id):
    ch_data = []
    request = youtube.channels().list(
        part="snippet,contentDetails,statistics",
        id=channel_id   
    )
    response = request.execute()
    for i in response['items']:
        data = {
                "Channel_Id" : i['id'],
                "Channel_Name" : i['snippet']['title'],
                "Channel_Description" : i['snippet']['description'],
                "Playlist_Id" : i['contentDetails']['relatedPlaylists']['uploads'],
                "Subscribers" : i['statistics']['subscriberCount'],
                "Total_Videos" : i['statistics']['videoCount'],
                "Views" : i['statistics']['viewCount']
        }
        ch_data.append(data)   
    return ch_data

# To get Video Ids

def videos_ids(channel_id):
    video_ids=[]
    response=youtube.channels().list(id=channel_id,
                                    part='contentDetails').execute()
    Playlist_Id=response['items'][0]['contentDetails']['relatedPlaylists']['uploads']
    next_page_token=None
    while True:
        response1=youtube.playlistItems().list(
                                            part='snippet',
                                            playlistId=Playlist_Id,
                                            maxResults=50,
                                            pageToken=next_page_token).execute()
        for i in range(len(response1['items'])):
            video_ids.append(response1['items'][i]['snippet']['resourceId']['videoId'])
        next_page_token=response1.get('nextPageToken')

        if next_page_token is None:
            break
    return video_ids

# TO get Video data

def videos_data(video_ids):
        video_data = []
        next_page_token=None
        for video_id in video_ids:
                request = youtube.videos().list(
                        part="snippet,contentDetails,statistics",
                        id = video_id,
                        maxResults = 50,
                        pageToken=next_page_token
                )
                response = request.execute()
                for i in response['items']:
                    content_details = i.get("contentDetails", {})
                    duration = content_details.get("duration", "")
                    duration = duration[2:]  # Remove "PT" from the beginning
                    hours = 0
                    minutes = 0
                    seconds = 0
                    if 'H' in duration:
                        hours_index = duration.index('H')
                        hours = int(duration[:hours_index])
                        duration = duration[hours_index + 1:]
                    if 'M' in duration:
                        minutes_index = duration.index('M')
                        minutes = int(duration[:minutes_index])
                        duration = duration[minutes_index + 1:]
                    if 'S' in duration:
                        seconds_index = duration.index('S')
                        seconds = int(duration[:seconds_index])
                    duration_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
                    data = {
                                "Channel_Id" : i['snippet']['channelId'],
                                "Channel_Name" : i['snippet']['channelTitle'],
                                "Video_Id" : i['id'],
                                "Video_Name" : i['snippet']['title'],
                                "Video_Description" : i['snippet']['description'],
                                "Tags" : i['snippet'].get('tags'),
                                "Published_At" : i['snippet']['publishedAt'],
                                "View_Count" : i['statistics'].get('viewCount'),
                                "Like_Count" : i['statistics'].get('likeCount'),
                                'Favorite_Count': i['statistics']['favoriteCount'],
                                'Comment_Counts' : i['statistics'].get('commentCount'),
                                "Duration" : duration_formatted,
                                "Thumbnails" : i['snippet']['thumbnails']['default']['url'],
                                "Caption_Status" : i['contentDetails']['caption']
                            }
                    video_data.append(data)
        return video_data

# To get Comments data

def comment_data(video_ids):
    Comments_data=[]
    try:
        for video_id in video_ids:
            request=youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                maxResults=50
            )
            response=request.execute()
            for i in response['items']:
                data = {                        
                        "Channel_Id" : i['snippet']['channelId'],
                        "Video_Id" : i['snippet']['topLevelComment']['snippet']['videoId'],
                        "Comment_Id" : i["snippet"]["topLevelComment"]["id"],
                        "Author_Name" : i['snippet']['topLevelComment']['snippet']['authorDisplayName'],
                        "Text_Display" : i['snippet']['topLevelComment']['snippet']['textDisplay'],
                        "Published_At" : i['snippet']['topLevelComment']['snippet']['publishedAt']
                    }
                Comments_data.append(data)
    except:
        pass       
    return Comments_data


with st.container():
    l_col, r_col= st.columns([1.5, 2])
    with l_col:
        channelId = st.text_input(label="Channel ID",placeholder="Enter channel ID")
        ll_col, mm_col, rr_col = st.columns(3)
        with ll_col:
            b1 = st.button(label='SUBMIT')
        with mm_col:
            b2 = st.button(label = "CLEAR")
        with rr_col:
            b3 = st.button(label="UPDATE")


if b1:
    with r_col:
        if __name__ == "__main__":
            st.write(channel_data(channelId))
            st.write(videos_data(videos_ids(channelId)))
            st.write(comment_data(videos_ids(channelId)))
if b2:
    if __name__ == "__main__":
        st.empty()

# SQL Code

def channel_sqltable():
        mycursor.execute("""CREATE TABLE IF NOT EXISTS Channels_Table (
                                                Channel_Id VARCHAR(100),
                                                Channel_Name VARCHAR(150),
                                                Channel_Description TEXT,
                                                Playlist_Id VARCHAR(100),
                                                Subscribers BIGINT,
                                                Total_Videos INT,
                                                Views BIGINT,
                                                PRIMARY KEY (Channel_Id))""")

        mydb.commit()

# ---------------------------------------------------------------------------------------

def video_sqltable():
    mycursor.execute("""CREATE TABLE IF NOT EXISTS Videos_Table(
                            Channel_Id VARCHAR(100), 
                            Channel_Name VARCHAR(150),
                            Video_Id VARCHAR(100),
                            Video_Name VARCHAR(150),
                            Video_Description TEXT,
                            Tags TEXT,
                            Published_At TIMESTAMP,
                            View_Count BIGINT,
                            Like_Count BIGINT,
                            Favorite_Count INT,
                            Comment_Counts INT,
                            Duration VARCHAR(200),
                            Thumbnails VARCHAR(200),
                            Caption_Status VARCHAR(200),
                            PRIMARY KEY (Video_Id),
                            FOREIGN KEY (Channel_Id) REFERENCES Channels_Table(Channel_Id))""")
    mydb.commit()   
    
# ---------------------------------------------------------------------------------------

def comments_sqltable():
        mycursor.execute("""CREATE TABLE IF NOT EXISTS Comments_Table (
                                                Channel_Id VARCHAR(100),
                                                Video_Id VARCHAR(100),
                                                Comment_Id VARCHAR(100),
                                                Author_Name VARCHAR(150),
                                                Text_Display TEXT,
                                                Published_At TIMESTAMP,
                                                FOREIGN KEY (Channel_Id) REFERENCES Channels_Table(Channel_Id),
                                                FOREIGN KEY (Video_Id) REFERENCES Videos_Table(Video_Id),
                                                PRIMARY KEY (Comment_Id))""")
        
        mydb.commit()


# ---------------------------------------------------------------------------------------

def upload_table():
    try:
        channel_details = channel_data(channelId)
        video_details = videos_data(videos_ids(channelId))
        comment_details = comment_data(videos_ids(channelId))
        for item in channel_details:
            ch_values = (
                item['Channel_Id'],
                item['Channel_Name'],
                item['Channel_Description'],
                item['Playlist_Id'],
                item['Subscribers'],
                item['Total_Videos'],
                item['Views']
            )
        mycursor.execute('''INSERT INTO Channels_Table (
                                    Channel_Id,
                                    Channel_Name,
                                    Channel_Description,
                                    Playlist_Id,
                                    Subscribers,
                                    Total_Videos,
                                    Views) VALUES (%s, %s, %s, %s, %s, %s, %s)''',ch_values)
        
        for item in video_details:
            v_values = (
                item['Channel_Id'],
                str(item['Channel_Name']),
                item['Video_Id'],
                str(item['Video_Name']),
                str(item['Video_Description']),
                str(item['Tags']),
                item['Published_At'],
                item['View_Count'],
                item['Like_Count'],
                item['Favorite_Count'],
                item['Comment_Counts'],
                str(item['Duration']),
                str(item['Thumbnails']),
                str(item['Caption_Status'])
            )
            mycursor.execute('''INSERT INTO Videos_Table (
                                    Channel_Id,
                                    Channel_Name,
                                    Video_Id,
                                    Video_Name,
                                    Video_Description,
                                    Tags,
                                    Published_At,
                                    View_Count,
                                    Like_Count,
                                    Favorite_Count,
                                    Comment_Counts,
                                    Duration,
                                    Thumbnails,
                                    Caption_Status) VALUES (%s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s)''',v_values)
        for item in comment_details:
            c_values = (
                item['Channel_Id'],
                item['Video_Id'],
                item['Comment_Id'],
                item['Author_Name'],
                item['Text_Display'],
                item['Published_At']
            )
            mycursor.execute('''INSERT INTO Comments_Table (
                                    Channel_Id,
                                    Video_Id,
                                    Comment_Id, 
                                    Author_Name,
                                    Text_Display,
                                    Published_At) VALUES (%s, %s, %s, %s, %s, %s)''',c_values)       
            
    
        mydb.commit()
        st.success("Uploaded Successfully")
    except:
        st.warning("Channel already exists")
        
# --------------------------------------------------------------------------------------

if b3:
    with r_col:   
        if __name__ == "__main__":
            channel_sqltable()
            video_sqltable()
            comments_sqltable()
            upload_table()
            

