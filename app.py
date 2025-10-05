import streamlit as st
import os
import database_config as db_con
import chatbot as cb

st.set_page_config(
    page_title='Database Builder Assistant',
    layout='wide',
    initial_sidebar_state='expanded'
)

page = st.sidebar.selectbox('Choses Page:', ('DB Config', 'Query Builder Assistant'))

if page == 'DB Config':
    db_con.run()
else:
    cb.run()

