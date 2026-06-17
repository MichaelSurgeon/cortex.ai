import streamlit as st

st.set_page_config(
    page_title="About · Cortex AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.title("About Cortex AI")
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
        st.markdown(
            "- Posts are fetched every **10 minutes** via a background scheduler\n"
            "- Reddit is pulled via the public **RSS feed** (no API key needed)\n"
            "- Posts are cached in memory until the next refresh cycle"
        )

with col2:
    with st.container(border=True):
        st.subheader("🤖 AI Processing")
        st.markdown(
            "- Each post is **classified** for relevance to AI / ML engineers\n"
            "- Relevant posts are **summarised** in one plain-English sentence\n"
            "- Both steps use **GPT-4o mini** with structured output parsing"
        )

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
    st.markdown(
        "- **r/MachineLearning** — research papers, breakthroughs, discussions\n"
        "- **r/ArtificialIntelligence** — broader AI news and commentary"
    )
