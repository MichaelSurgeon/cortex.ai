from backend.models.feed_schemas import FeedPost


class RedditPost(FeedPost):
    subreddit: str
