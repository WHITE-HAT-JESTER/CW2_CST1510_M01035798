import streamlit as st
#Editing the display
st.set_page_config(page_title="Home Page", layout="wide")
st.title("Home Page") #Page label
st.header("Welcome Home!")

st.subheader("Categories Available:")
st.write("\n1. Cyber Incidents")
st.write("\n2. IT Tickets")
st.write("\n3. Dataset Metadata")

if st.button ("Login/Register"):
    st.switch_page("Pages/1_Login_Register.py")