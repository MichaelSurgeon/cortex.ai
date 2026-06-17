from datetime import UTC, datetime


def format_age(created_at: str) -> str:
    """Convert ISO timestamp to a human-readable relative time string."""
    try:
        dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        now = datetime.now(UTC)
        seconds = int((now - dt).total_seconds())
        if seconds < 60:
            return f"{seconds}s ago"
        if seconds < 3600:
            return f"{seconds // 60}m ago"
        if seconds < 86400:
            return f"{seconds // 3600}h ago"
        days = seconds // 86400
        return f"{days}d ago"
    except Exception:
        return created_at[:10]
