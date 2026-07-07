import streamlit as st

feed_page = st.Page("pages/1_Feed.py", title="Feed", icon="📰", default=True)
analytics_page = st.Page("pages/3_Analytics.py", title="Analytics", icon="📊")
about_page = st.Page("pages/2_About.py", title="About", icon="ℹ️")

pg = st.navigation([feed_page, analytics_page, about_page])
pg.run()
