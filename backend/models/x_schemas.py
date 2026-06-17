from backend.models.feed_schemas import FeedPost


class XPost(FeedPost):
    like_count: int
    retweet_count: int
