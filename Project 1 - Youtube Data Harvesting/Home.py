import streamlit as st
import base64

st.set_page_config(page_title="Project 1", page_icon=":tada:", layout="wide")

# CSS 

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
local_css("style/style.css")

with st.container():
    st.write()
    img_col, tit_col = st.columns(2)
    with img_col:
        file_ = open("Images/Img5.gif", "rb")
        contents = file_.read()
        data_url = base64.b64encode(contents).decode("utf-8")
        file_.close()
        st.markdown(f'<img src="data:image/gif;base64,{data_url}" alt="data gif" width=100%>',unsafe_allow_html=True,)
    with tit_col:
        st.title(":orange[YOUTUBE DATA HARVESTING AND WAREHOUSING]")