import streamlit as st
from streamlit_option_menu import option_menu
from student import student_app
from teacher import teacher_app
st.set_page_config(page_title="Hotu portfolio", page_icon=":tada:", layout="wide",initial_sidebar_state="collapsed")

selected3 = option_menu(None, ["Teacher", "Student"], 
    icons=['cloud-upload', "book"], 
    menu_icon="cast", default_index=0, orientation="horizontal",
    
)
if selected3=="Teacher":
    teacher_app()
if selected3=="Student":
    student_app()
