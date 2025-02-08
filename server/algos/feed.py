from datetime import datetime
from typing import Optional

from server.database import Post
from server.types import FeedPost, FeedResponse

CURSOR_EOF = "eof"


def handler(cursor: Optional[str], limit: int) -> FeedResponse:
    posts = (
        Post.select()
        .order_by(Post.cid.desc())
        .order_by(Post.indexed_at.desc())
        .limit(limit)
    )

    if cursor:
        if cursor == CURSOR_EOF:
            return FeedResponse(cursor=CURSOR_EOF, feed=[])
        cursor_parts = cursor.split("::")
        if len(cursor_parts) != 2:
            raise ValueError("Malformed cursor")

        indexed_at_str, cid = cursor_parts
        indexed_at_dt = datetime.fromtimestamp(int(indexed_at_str) / 1000)
        posts = posts.where(
            ((Post.indexed_at == indexed_at_dt) & (Post.cid < cid))
            | (Post.indexed_at < indexed_at_dt)
        )

    feed = [FeedPost(post=post.uri) for post in posts]

    cursor = CURSOR_EOF
    last_post = posts[-1] if posts else None
    if last_post:
        cursor = f"{int(last_post.indexed_at.timestamp() * 1000)}::{last_post.cid}"

    return FeedResponse(cursor=cursor, feed=feed)
