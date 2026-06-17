import streamlit as st

feed_page = st.Page("pages/1_Feed.py", title="Feed", icon="📰", default=True)
about_page = st.Page("pages/2_About.py", title="About", icon="ℹ️")

pg = st.navigation([feed_page, about_page])
pg.run()
