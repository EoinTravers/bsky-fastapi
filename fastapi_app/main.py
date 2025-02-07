from fastapi import FastAPI
from pydantic import BaseModel, validator
from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

MY_POST = "at://did:plc:stdc72pu4wbmpdkfw5qqcw3b/app.bsky.feed.post/3lhj7sjr75o2s"


app = FastAPI()


class Config(BaseModel):
    SERVICE_DID: str = os.getenv("SERVICE_DID", "")
    HOSTNAME: str = os.getenv("HOSTNAME", "")
    FEED_URI: str = os.getenv("FEED_URI", "")

    @validator("SERVICE_DID")
    def validate_service_did(cls, v: str, values: Dict[str, Any]) -> str:
        hostname: str = values["HOSTNAME"]
        if not v.endswith(hostname):
            raise ValueError(f"SERVICE_DID must end with HOSTNAME ({hostname})")
        return v


config = Config()


@app.get("/")
def index():
    return "ATProto Feed Generator powered by The AT Protocol SDK for Python (https://github.com/MarshalX/atproto)."


@app.get("/.well-known/did.json")
def did_json():
    return {
        "@context": ["https://www.w3.org/ns/did/v1"],
        "id": config.SERVICE_DID,
        "service": [
            {
                "id": "#bsky_fg",
                "type": "BskyFeedGenerator",
                "serviceEndpoint": f"https://{config.HOSTNAME}",
            }
        ],
    }


@app.get("/xrpc/app.bsky.feed.describeFeedGenerator")
def describe_feed_generator():
    feeds = [{"uri": config.FEED_URI}]
    response = {
        "encoding": "application/json",
        "body": {"did": config.SERVICE_DID, "feeds": feeds},
    }
    return response


# The main route
class FeedPost(BaseModel):
    post: str  # Must be an at://did: identifier


class FeedSkeleton(BaseModel):
    feed: list[FeedPost]
    cursor: int | None = None


@app.get("/xrpc/app.bsky.feed.getFeedSkeleton")
def get_feed_skeleton(
    feed: str | None = None,
    cursor: int | None = None,
    limit: int = 20,
) -> FeedSkeleton:
    # Example of how to check auth if giving user-specific results:
    """
    from server.auth import AuthorizationError, validate_auth
    try:
        requester_did = validate_auth(request)
    except AuthorizationError:
        return 'Unauthorized', 401
    """

    response = FeedSkeleton(feed=[FeedPost(post=MY_POST) for _ in range(5)])
    return response
