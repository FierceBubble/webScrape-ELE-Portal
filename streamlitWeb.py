import streamlit as st
import Scrape as scr

header = st.container()
user_input = st.container()

with header:
    st.title('My ELE Portal WebScrape!')
    st.text("This website will be used to scrape information from ELE Portal Website\nhttps://apps.ucsiuniversity.edu.my/ecas")

with user_input:
    if st.button("Scrape & Update"):
        scr.getEleInfo()
        st.text('Scrape & Database Update Done!\n')
