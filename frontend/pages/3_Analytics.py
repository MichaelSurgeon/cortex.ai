from collections import Counter
from datetime import UTC, datetime
from pathlib import Path

import pandas as pd
import streamlit as st
from utils.api import fetch_feed

st.set_page_config(
    page_title="Analytics · Cortex AI",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

_css = (Path(__file__).parent.parent / "styles" / "main.css").read_text()
st.html(f"<style>{_css}</style>")

if "analytics_posts" not in st.session_state:
    st.session_state.analytics_posts = []
if "analytics_error" not in st.session_state:
    st.session_state.analytics_error = None


def do_refresh() -> None:
    with st.spinner("Loading feed data…"):
        posts, error = fetch_feed()
    st.session_state.analytics_posts = posts
    st.session_state.analytics_error = error


if not st.session_state.analytics_posts and st.session_state.analytics_error is None:
    do_refresh()

with st.sidebar:
    st.write("")
    if st.button("↺ Refresh", width="stretch"):
        do_refresh()
        st.rerun()

posts: list[dict] = st.session_state.analytics_posts
error: str | None = st.session_state.analytics_error

st.title("📊 Analytics")
st.caption(datetime.now(UTC).strftime("%A, %d %B %Y"))
st.divider()

if error:
    st.error(error, icon="🔌")
    st.stop()

if not posts:
    st.info(
        "The backend is still fetching and processing posts. "
        "This can take a few minutes on first start — hit **↺ Refresh** to check again.",
        icon="⏳",
    )
    st.stop()

# ── Top-level metrics ─────────────────────────────────────────────────────────
confidence_scores = [p["confidence"] for p in posts if p.get("confidence") is not None]
avg_confidence = sum(confidence_scores) / len(confidence_scores) if confidence_scores else None

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Stories", len(posts))
col2.metric("Sources Active", len({p.get("source") for p in posts}))
col3.metric("Avg Confidence", f"{avg_confidence:.0%}" if avg_confidence is not None else "—")
col4.metric("Cache Usage", f"{len(posts)} / 200")

st.write("")
st.caption(
    "**Confidence** is an LLM-as-judge score — GPT-4o-mini rates its own certainty "
    "(0–100%) on whether a post is relevant and that the category is correct. "
    "🟢 ≥ 85% · 🟡 65–84% · 🔴 < 65%"
)
st.write("")

# ── Distributions ─────────────────────────────────────────────────────────────
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("By Category")
    cat_counts = Counter(p.get("category", "Unknown") for p in posts if p.get("category"))
    df_cats = pd.DataFrame(list(cat_counts.items()), columns=["Category", "Posts"])
    st.bar_chart(df_cats, x="Category", y="Posts", width="stretch")

with col_right:
    st.subheader("By Source")
    src_counts = Counter(p.get("source", "unknown").capitalize() for p in posts)
    df_src = pd.DataFrame(list(src_counts.items()), columns=["Source", "Posts"])
    st.bar_chart(df_src, x="Source", y="Posts", width="stretch")

st.write("")

# ── Confidence by category ────────────────────────────────────────────────────
if confidence_scores:
    st.subheader("Avg Confidence by Category")
    cat_conf: dict[str, list[float]] = {}
    for p in posts:
        cat = p.get("category")
        conf = p.get("confidence")
        if cat and conf is not None:
            cat_conf.setdefault(cat, []).append(conf)

    avg_by_cat = sorted(
        {cat: sum(scores) / len(scores) for cat, scores in cat_conf.items()}.items()
    )

    cols = st.columns(len(avg_by_cat))
    for col, (cat, avg) in zip(cols, avg_by_cat, strict=True):
        icon = "🟢" if avg >= 0.85 else "🟡" if avg >= 0.65 else "🔴"
        col.metric(f"{icon} {cat}", f"{avg:.0%}")
