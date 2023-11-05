import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="GetAround_Dashboard",
    page_icon="une-analyse.png",
    layout="wide",
)

st.subheader('Load Data')

if 'data1' in st.session_state and 'data2' in st.session_state:
    choice = st.selectbox("Select Data", ("Data 1", "Data 2"))

    if choice == "Data 1":
        df = st.session_state.data1
    else:
        df = st.session_state.data2

    if st.checkbox("Show Data"):
        st.subheader('Raw data')
        st.write(df)
    else:
        st.warning("Data not loaded yet. Please visit the Home page first.")
else:
    st.warning("Data not loaded yet. Please visit the Home page first.")