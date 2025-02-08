import os
from typing import Optional

from pydantic import BaseModel, Field, validator
from dotenv import load_dotenv


def _get_bool_env_var(value: Optional[str]) -> bool:
    if value is None:
        return False

    normalized_value = value.strip().lower()
    if normalized_value in {"1", "true", "t", "yes", "y"}:
        return True

    return False


class Config(BaseModel):
    # Set this to the hostname that you intend to run the service at
    hostname: str

    # You can obtain it by publishing of feed (run publish_feed.py)
    feed_uri: str

    # (Optional). Ignore posts with a created_at timestamp older than 1 day
    # to avoid including archived posts from X/Twitter
    ignore_archived_posts: bool = Field(default=False)

    # (Optional). Ignore reply posts
    ignore_reply_posts: bool = Field(default=False)
    # (Optional). Only use this if you want a service did different from did:web
    service_did: str = Field(default="")

    @validator("service_did", pre=True, always=True)
    def set_service_did(cls, v: str, values: dict) -> str:
        if not v:
            hostname = values.get("hostname")
            if hostname:
                return f"did:web:{hostname}"
        return v


def setup_config() -> Config:
    load_dotenv(override=True)

    hostname = os.environ.get("HOSTNAME")
    if not hostname:
        raise RuntimeError('You should set "HOSTNAME" environment variable first.')

    feed_uri = os.environ.get("FEED_URI")
    if not feed_uri:
        raise RuntimeError(
            "Publish your feed first (run publish_feed.py) to obtain Feed URI. "
            'Set this URI to "FEED_URI" environment variable.'
        )

    return Config(
        service_did=os.environ.get("SERVICE_DID", ""),
        hostname=hostname,
        feed_uri=feed_uri,
        ignore_archived_posts=_get_bool_env_var(
            os.environ.get("IGNORE_ARCHIVED_POSTS")
        ),
        ignore_reply_posts=_get_bool_env_var(os.environ.get("IGNORE_REPLY_POSTS")),
        flask_run_from_cli=os.environ.get("FLASK_RUN_FROM_CLI"),
    )
