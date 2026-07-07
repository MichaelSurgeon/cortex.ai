from datetime import UTC, datetime
from pathlib import Path

import streamlit as st
from utils.api import fetch_feed
from utils.helpers import format_age

st.set_page_config(
    page_title="Feed · Cortex AI",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

_css = (Path(__file__).parent.parent / "styles" / "main.css").read_text()
st.html(f"<style>{_css}</style>")

# ── Session state ─────────────────────────────────────────────────────────────
if "last_fetched" not in st.session_state:
    st.session_state.last_fetched = None
if "posts" not in st.session_state:
    st.session_state.posts = []
if "error" not in st.session_state:
    st.session_state.error = None
if "page" not in st.session_state:
    st.session_state.page = 0
if "audience" not in st.session_state:
    st.session_state.audience = "Engineer"


def do_refresh() -> None:
    with st.spinner("Fetching latest stories…"):
        posts, error = fetch_feed()
    st.session_state.posts = posts
    st.session_state.error = error
    st.session_state.last_fetched = datetime.now(UTC)
    st.session_state.page = 0


if st.session_state.last_fetched is None:
    do_refresh()

# ── Sidebar: filters, stats, refresh ─────────────────────────────────────────
with st.sidebar:
    st.subheader("Filters")

    search = st.text_input(
        "Search",
        placeholder="🔍 Search posts…",
        label_visibility="collapsed",
    )

    all_posts: list[dict] = st.session_state.posts
    sources = sorted({p.get("source", "unknown").lower() for p in all_posts})

    st.caption("Source")
    if len(sources) > 1:
        filter_options = ["All"] + [s.capitalize() for s in sources]
        selected_source = st.radio(
            "Source", filter_options, label_visibility="collapsed"
        )
    else:
        selected_source = "All"
        st.caption("Only one source available")

    st.write("")
    all_categories: list[str] = sorted(
        {p["category"] for p in all_posts if p.get("category")}
    )
    st.caption("Category")
    if all_categories:
        cat_options = ["All"] + all_categories
        selected_category = st.radio(
            "Category", cat_options, label_visibility="collapsed"
        )
    else:
        selected_category = "All"
        st.caption("No categories yet")

    st.divider()

    st.caption("Audience")
    st.session_state.audience = st.radio(
        "Audience",
        ["Engineer", "Enthusiast"],
        index=0 if st.session_state.audience == "Engineer" else 1,
        label_visibility="collapsed",
        help="Engineer: technical depth. Enthusiast: plain English.",
    )

    st.divider()

    if st.session_state.last_fetched:
        age = format_age(st.session_state.last_fetched.isoformat())
        st.metric("Stories", len(all_posts))
        st.caption(f"Updated {age}")

    st.write("")
    if st.button("↺ Refresh", width="stretch"):
        do_refresh()
        st.rerun()

# ── Apply filters ─────────────────────────────────────────────────────────────
posts: list[dict] = st.session_state.posts

if selected_source != "All":
    posts = [p for p in posts if p.get("source", "").lower() == selected_source.lower()]

if selected_category != "All":
    posts = [p for p in posts if p.get("category") == selected_category]

if search:
    q = search.lower()
    posts = [
        p
        for p in posts
        if q in p.get("title", "").lower()
        or q in p.get("summary", "").lower()
        or q in p.get("author", "").lower()
    ]

# ── Error banner ──────────────────────────────────────────────────────────────
if st.session_state.error:
    st.title("🧠 Cortex AI")
    st.error(st.session_state.error, icon="🔌")
    st.stop()

# ── Masthead ──────────────────────────────────────────────────────────────────
st.title("🧠 Cortex AI")
st.caption(datetime.now(UTC).strftime("%A, %d %B %Y") + "  ·  AI & Machine Learning")
st.divider()

# ── Pagination state ──────────────────────────────────────────────────────────
PAGE_SIZE = 10
total = len(posts)
total_pages = max(1, -(-total // PAGE_SIZE))  # ceil division

if st.session_state.page >= total_pages:
    st.session_state.page = 0

page_start = st.session_state.page * PAGE_SIZE
page_posts = posts[page_start : page_start + PAGE_SIZE]

# ── Feed ──────────────────────────────────────────────────────────────────────
SOURCE_LABELS = {"reddit": "◈ Reddit", "x": "𝕏 X / Twitter"}
CATEGORY_ICONS = {
    "Research": "🔬",
    "Engineering": "⚙️",
    "Business": "💼",
    "Policy": "⚖️",
    "General": "📰",
}

if not posts and not st.session_state.error:
    all_posts_count = len(st.session_state.posts)
    if all_posts_count == 0:
        # Backend returned nothing — still warming up or no data yet
        st.info(
            "The backend is still fetching and processing posts. "
            "This can take a few minutes on first start — hit **↺ Refresh** to check again.",
            icon="⏳",
        )
    else:
        # Posts exist but filters narrowed to zero
        st.info("No stories match your current filters. Try adjusting them.", icon="📭")
else:
    col_left, col_right = st.columns(2, gap="small")
    columns = [col_left, col_right]

    for idx, post in enumerate(page_posts):
        post_id = post.get("id", "")
        title = post.get("title", "Untitled")
        url = post.get("url", "#")
        body = post.get("clean_body_text", "")
        author = post.get("author", "Unknown")
        source = post.get("source", "unknown").lower()
        created_at = post.get("created_at", "")

        summary = (
            post.get("summary_engineer", "")
            if st.session_state.audience == "Engineer"
            else post.get("summary_enthusiast", "")
        ) or ""

        age_str = format_age(created_at) if created_at else ""
        source_label = SOURCE_LABELS.get(source, source.capitalize())
        category = post.get("category") or "General"
        category_icon = CATEGORY_ICONS.get(category, "📰")

        first_sentence = summary.split(". ")[0].rstrip(".")
        has_more = len(summary) > len(first_sentence) + 2

        headline = post.get("generated_title") or title
        safe_headline = (
            headline.replace("[", "\\[").replace("]", "\\]").replace("\n", " ").strip()
        )

        with columns[idx % 2].container(border=True):
            meta_parts = [
                f"{category_icon} **{category}**",
                f"**{source_label}**",
                f"👤 {author}",
            ]
            confidence = post.get("confidence")
            if confidence is not None:
                pct = int(confidence * 100)
                conf_icon = "🟢" if confidence >= 0.85 else "🟡" if confidence >= 0.65 else "🔴"
                meta_parts.append(f"{conf_icon} {pct}%")
            if age_str:
                meta_parts.append(f"🕐 {age_str}")
            st.caption("  ·  ".join(meta_parts))

            st.markdown(f"##### [{safe_headline}]({url})")
            st.caption(first_sentence + ("…" if has_more else ""))

            with st.expander("🧠 AI Summary  +  Original Post", key=f"exp_{post_id}"):
                st.write(summary)
                if body:
                    st.divider()
                    st.caption("Original Post")
                    st.write(body[:3000] + ("…" if len(body) > 3000 else ""))

    # ── Pagination controls ───────────────────────────────────────────────────
    if total_pages > 1:
        st.write("")
        col_prev, col_info, col_next = st.columns([1, 3, 1])
        with col_prev:
            if st.button(
                "← Prev", disabled=st.session_state.page == 0, width="stretch"
            ):
                st.session_state.page -= 1
                st.rerun()
        with col_info:
            st.caption(
                f"Page {st.session_state.page + 1} of {total_pages}  ·  {total} stories"
            )
        with col_next:
            if st.button(
                "Next →",
                disabled=st.session_state.page >= total_pages - 1,
                width="stretch",
            ):
                st.session_state.page += 1
                st.rerun()
