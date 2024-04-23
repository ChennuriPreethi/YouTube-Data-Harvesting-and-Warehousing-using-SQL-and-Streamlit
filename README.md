# Youtube-Data-Harvesting-and-Warehousing-using-SQL-and-Streamlit

# Overview

YouTube Data Harvesting and Warehousing is a project that aims to allow users to access and analyze data from multiple YouTube channels. The project utilizes SQL and Streamlit to create a user-friendly application that allows users to retrieve, store and query.

# TOOLS AND LIBRARIES

STREAMLIT: Streamlit library was used to create a user-friendly UI that enables users to interact with the application and perform data retrieval and analysis tasks.

PYTHON: Python is the language used in this project for the development of the complete application, including data retrieval, processing, analysis, and visualisation.

GOOGLE API CLIENT: The googleapiclient library in Python facilitates the communication with different Google APIs. The purpose of this library in this project is to interact with YouTube's Data API v3, allowing the retrieval of essential information like channel details, video details, and comments details.

MySQL: MySQL is used for efficient storage and management of structured data, offering support for various data types and advanced SQL capabilities.

Pandas: A data manipulation library used for data processing and analysis.

# Workflow

1. In the Google Developer Console, create a new project or can use the existing project to generate Youtube API Key. This API key is used to retrive the channel, video and comments data from the youtube channel.

2. To start with the python program, I have installed googleapiclient libraries to make requests to the API. 
    
3. Using the Channel ID the user can extract the channel, videos and comments details of that particular youtube channel.

4. Once the data is retrieved from the YouTube API, the data is being stored/uploaded into MySQL databases into Project_1 database.

5. The database is divided into three tables and used sql queries to insert the data. In which the channel details are stored in "Channels_Table", video details are stored in "Videos_Table" and comments details are stored in "Comments_Table".

6. The user can provide the user input through "Channel ID" textbox and the data will be displayed in the streamlit app.

7. Altogether, this approach involves building a simple UI with Streamlit, retrieving data from the YouTube API, storing it in MySQL database, querying the data warehouse and displaying the data in the Streamlit app.
