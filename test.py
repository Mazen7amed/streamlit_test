import streamlit as st
from Scrapping import mobile_de_scrap

url = st.text_input("URL")
data = mobile_de_scrap(url)
st.write(data)