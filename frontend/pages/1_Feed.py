from datetime import UTC, datetime

import streamlit as st
from utils.api import fetch_feed
from utils.helpers import format_age

st.set_page_config(
    page_title="Feed · Cortex AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Session state ─────────────────────────────────────────────────────────────
if "last_fetched" not in st.session_state:
    st.session_state.last_fetched = None
if "posts" not in st.session_state:
    st.session_state.posts = []
if "error" not in st.session_state:
    st.session_state.error = None
if "page" not in st.session_state:
    st.session_state.page = 0


def do_refresh() -> None:
    posts, error = fetch_feed()
    st.session_state.posts = posts
    st.session_state.error = error
    st.session_state.last_fetched = datetime.now(UTC)
    st.session_state.page = 0


# Auto-load on first visit
if st.session_state.last_fetched is None:
    do_refresh()

# ── Header ────────────────────────────────────────────────────────────────────
col_title, col_btn = st.columns([6, 1])

with col_title:
    st.title("🧠 Cortex AI")
    st.caption("Curated AI news — filtered and summarised by GPT-4o mini")

with col_btn:
    st.write("")
    st.write("")
    if st.button("↺ Refresh", use_container_width=True):
        do_refresh()
        st.rerun()

# ── Status bar ────────────────────────────────────────────────────────────────
if st.session_state.last_fetched:
    age = format_age(st.session_state.last_fetched.isoformat())
    count = len(st.session_state.posts)
    label = f"{count} post{'s' if count != 1 else ''}"
    st.caption(f"{label} · updated {age}")

# ── Error banner ──────────────────────────────────────────────────────────────
if st.session_state.error:
    st.error(st.session_state.error)

# ── Filters ───────────────────────────────────────────────────────────────────
posts: list[dict] = st.session_state.posts

sources = sorted({p.get("source", "unknown").lower() for p in posts})

if len(sources) > 1:
    filter_options = ["All"] + [s.capitalize() for s in sources]
    selected = st.radio(
        "Source",
        filter_options,
        horizontal=True,
        label_visibility="collapsed",
    )
    if selected != "All":
        posts = [p for p in posts if p.get("source", "").lower() == selected.lower()]
else:
    selected = "All"

# ── Search ────────────────────────────────────────────────────────────────────
if posts:
    search = st.text_input(
        "Search",
        placeholder="🔍  Search by title, summary, or author…",
        label_visibility="collapsed",
    )
    if search:
        q = search.lower()
        posts = [
            p
            for p in posts
            if q in p.get("title", "").lower()
            or q in p.get("summary", "").lower()
            or q in p.get("author", "").lower()
        ]

st.write("")

# ── Pagination ────────────────────────────────────────────────────────────────
PAGE_SIZE = 10
total = len(posts)
total_pages = max(1, -(-total // PAGE_SIZE))  # ceil division

# Reset to page 0 if filters/search pushed us out of range
if st.session_state.page >= total_pages:
    st.session_state.page = 0

page_start = st.session_state.page * PAGE_SIZE
page_posts = posts[page_start : page_start + PAGE_SIZE]

# ── Feed ──────────────────────────────────────────────────────────────────────
if not posts and not st.session_state.error:
    st.info(
        "No posts found. Try adjusting your filters or refreshing the feed.", icon="📭"
    )
else:
    for post in page_posts:
        title = post.get("title", "Untitled")
        url = post.get("url", "#")
        summary = post.get("summary", "")
        author = post.get("author", "Unknown")
        source = post.get("source", "unknown")
        created_at = post.get("created_at", "")

        age_str = format_age(created_at) if created_at else ""
        source_label = {"reddit": "◈ Reddit", "x": "𝕏 X / Twitter"}.get(
            source.lower(), source.capitalize()
        )

        with st.container(border=True):
            safe_title = (
                title.replace("[", "\\[").replace("]", "\\]").replace("\n", " ").strip()
            )
            st.markdown(f"**[{safe_title}]({url})**")

            st.write(summary)

            col_meta, col_link = st.columns([5, 1])
            with col_meta:
                parts = [f"**{source_label}**", f"👤 {author}"]
                if age_str:
                    parts.append(f"🕐 {age_str}")
                st.caption("  ·  ".join(parts))
            with col_link:
                st.link_button("Read →", url, use_container_width=True)

    # ── Pagination controls ───────────────────────────────────────────────────
    if total_pages > 1:
        st.write("")
        col_prev, col_info, col_next = st.columns([1, 3, 1])
        with col_prev:
            if st.button(
                "← Prev", disabled=st.session_state.page == 0, use_container_width=True
            ):
                st.session_state.page -= 1
                st.rerun()
        with col_info:
            st.caption(
                f"Page {st.session_state.page + 1} of {total_pages}  ·  {total} posts"
            )
        with col_next:
            if st.button(
                "Next →",
                disabled=st.session_state.page >= total_pages - 1,
                use_container_width=True,
            ):
                st.session_state.page += 1
                st.rerun()
