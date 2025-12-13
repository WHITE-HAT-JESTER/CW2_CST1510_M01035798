import streamlit as st
from streamlit_option_menu import option_menu

#if it were a sidebar menu, you shouldn't include orientation to make it prettier
#with st.sidebar: puts menu in the sidebar
selected=option_menu(
    menu_title=None,
    options = [
            "Cybersecurity",
            "Datasets",
            "IT Tickets",
        ],#required dashboard pages
    icons=[
            "Shield exclamation",
            "Stickies fill",
            "Display",
        ],# icons to make it a little pretty
    default_index=0,
    orientation="horizontal", #to make the menu bar horizontal
                                 #on top of the page rather than a sidebar
    )

if selected == "Cybersecurity":
     st.title(f"{selected}")
     st.markdown()
if selected == "Datasets":
     st.title(f"{selected}")
if selected == "IT Tickets":
    st.title(f"{selected}")
