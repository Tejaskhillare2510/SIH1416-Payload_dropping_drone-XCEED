from pathlib import Path
import PIL

import streamlit as st

import settings
import helper

# Setting page layout
st.set_page_config(
    page_title="Xceed [Webcam Output]",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Main page heading
st.title("Team:- Xceed [Webcam Output]")

confidence = 0.5

try:
    model = helper.load_model(settings.DETECTION_MODEL)
except Exception as ex:
    st.error(f"Unable to load model. Check the specified path: {settings.DETECTION_MODEL}")
    st.error(ex)

# Webcam Output
st.sidebar.header("Webcam Output")
address= input("Enter the address with the port number: ")
helper.play_webcam("http://" + address + "/stream.mjpg" ,confidence, model)
