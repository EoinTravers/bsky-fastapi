from fastapi import FastAPI, Header, HTTPException
from dotenv import load_dotenv
import logging

from .config import Config, setup_config
from .type_definitions import DIDDocument, FeedGeneratorDescriptor, FeedSkeleton
from .feed import feed_generator

load_dotenv()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

app = FastAPI()
config: Config = setup_config()


@app.get("/")
def index():
    return "Minimal FastAPI-powered bsky feed generator."


@app.get("/.well-known/did.json")
def did_json() -> DIDDocument:
    doc = {
        "@context": ["https://www.w3.org/ns/did/v1"],
        "id": config.service_did,
        "service": [
            {
                "id": "#bsky_fg",
                "type": "BskyFeedGenerator",
                "serviceEndpoint": f"https://{config.hostname}",
            }
        ],
    }
    return DIDDocument(**doc)


@app.get("/xrpc/app.bsky.feed.describeFeedGenerator")
def describe_feed_generator() -> FeedGeneratorDescriptor:
    feeds = [{"uri": config.feed_uri}]
    response = {
        "encoding": "application/json",
        "body": {"did": config.service_did, "feeds": feeds},
    }
    return FeedGeneratorDescriptor(**response)


# The main route
@app.get("/xrpc/app.bsky.feed.getFeedSkeleton")
def get_feed_skeleton(
    feed: str | None = config.feed_uri,
    cursor: int | None = None,
    limit: int = 20,
    authorization: str | None = Header(
        None, description="Bearer token for authentication"
    ),
) -> FeedSkeleton:
    """
    The main route for bsky feeds.

    Args:
        feed: The feed to get.
        cursor: The cursor to get the next page of.
        limit: The number of posts to get.
        authorization: The authorization header. Should start with "Bearer ".
    """
    logger.info(f"Feed Request: {feed=} {cursor=} {limit=} {authorization=}")
    if feed != config.feed_uri:
        raise HTTPException(status_code=404, detail=f"Feed not found: {feed}")

    # Example of how to check auth if giving user-specific results:
    # """
    # from server.auth import AuthorizationError, validate_auth
    # try:
    #     requester_did = validate_auth(request)
    # except AuthorizationError:
    #     return 'Unauthorized', 401
    # """
    response = feed_generator(cursor, limit)
    logger.info(f"Feed Response: {response}")
    return response
    # response = FeedSkeleton(feed=[FeedPost(post=MY_POST) for _ in range(5)])
    # return response
