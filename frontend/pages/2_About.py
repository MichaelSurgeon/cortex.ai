from pathlib import Path

import streamlit as st

st.set_page_config(
    page_title="About · Cortex AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

_css = (Path(__file__).parent.parent / "styles" / "main.css").read_text()
st.html(f"<style>{_css}</style>")

st.title("🧠 About Cortex AI")
st.caption("How it works and what powers it")

st.divider()

with st.container(border=True):
    st.subheader("What is Cortex AI?")
    st.write(
        "Cortex AI is a personal AI news aggregator. It continuously pulls posts from "
        "Reddit and X (Twitter), uses GPT-4o mini to filter out noise and irrelevant "
        "content, then writes a concise plain-English summary for everything that "
        "makes the cut — so you get the signal without the scroll."
    )

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.subheader("🔄 Data Pipeline")
        st.write("- Posts are fetched every **10 minutes** via a background scheduler")
        st.write("- Reddit is pulled via the public **RSS feed** (no API key needed)")
        st.write("- Posts are cached in memory until the next refresh cycle")

with col2:
    with st.container(border=True):
        st.subheader("🤖 AI Processing")
        st.write("- Each post is **classified** for relevance to AI / ML engineers")
        st.write("- Relevant posts are **summarised** in one plain-English sentence")
        st.write("- Both steps use **GPT-4o mini** with structured output parsing")

with st.container(border=True):
    st.subheader("🛠 Tech Stack")
    cols = st.columns(4)
    techs = [
        "FastAPI",
        "Streamlit",
        "OpenAI GPT-4o mini",
        "Pydantic",
        "APScheduler",
        "feedparser",
        "httpx",
        "Python 3.10+",
    ]
    for i, tech in enumerate(techs):
        cols[i % 4].code(tech, language=None)

with st.container(border=True):
    st.subheader("📡 Sources")
    st.write("- **r/MachineLearning** — research papers, breakthroughs, discussions")
    st.write("- **r/ArtificialIntelligence** — broader AI news and commentary")
