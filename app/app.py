import sys
import signal
import threading

from flask import Flask, jsonify, request
from app import config

app = Flask(__name__)


@app.route("/")
def index():
    active_routes = [
        ".well-known/did.json",
        "/xrpc/app.bsky.feed.describeFeedGenerator",
        "/xrpc/app.bsky.feed.getFeedSkeleton",
    ]
    txt = f"ATProto Feed Generator.<br>Active routes:<br>"
    for route in active_routes:
        txt += f"<a href='{route}'>{route}</a><br>"
    return txt


@app.route("/.well-known/did.json", methods=["GET"])
def did_json():
    if not config.SERVICE_DID.endswith(config.HOSTNAME):
        return "", 404

    return jsonify(
        {
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
    )


@app.route("/xrpc/app.bsky.feed.describeFeedGenerator", methods=["GET"])
def describe_feed_generator():
    feeds = [{"uri": config.FEED_URI}]
    response = {
        "encoding": "application/json",
        "body": {"did": config.SERVICE_DID, "feeds": feeds},
    }
    return jsonify(response)


def algo(cursor, limit):
    feed = [
        {
            "post": "at://did:plc:stdc72pu4wbmpdkfw5qqcw3b/app.bsky.feed.post/3lhj7sjr75o2s"
        },
        {
            "post": "at://did:plc:e2ndzn2nunpgqh2r2b43ijk5/app.bsky.feed.post/3lhj7q4nuaz2e"
        },
        {
            "post": "at://did:plc:stdc72pu4wbmpdkfw5qqcw3b/app.bsky.feed.post/3lhj7pgfg7w2s"
        },
        {
            "post": "at://did:plc:lnamjzanglynqbri6gxyyvcm/app.bsky.feed.post/3lhj7iboets2i"
        },
        {
            "post": "at://did:plc:s2z5pod6c232oj3f4yqjhxw6/app.bsky.feed.post/3lhj7hycfac2u"
        },
        {
            "post": "at://did:plc:y3gfb3pd2c3be7asz5c622nn/app.bsky.feed.post/3lhj7cqeu4c2l"
        },
        {
            "post": "at://did:plc:2dieft65rlnwrzjcg3nzcjye/app.bsky.feed.post/3lhj77vnktk2i"
        },
        {
            "post": "at://did:plc:czzwr7go6wsjhqfsf7dutcqh/app.bsky.feed.post/3lhj73h4xf22q"
        },
    ]
    return {"cursor": cursor, "feed": feed}


@app.route("/xrpc/app.bsky.feed.getFeedSkeleton", methods=["GET"])
def get_feed_skeleton():
    # Example of how to check auth if giving user-specific results:
    """
    from server.auth import AuthorizationError, validate_auth
    try:
        requester_did = validate_auth(request)
    except AuthorizationError:
        return 'Unauthorized', 401
    """

    try:
        cursor = request.args.get("cursor", default=None, type=str)
        limit = request.args.get("limit", default=20, type=int)
        print(f"cursor: {cursor}, limit: {limit}")
        body = algo(cursor, limit)
    except ValueError:
        return "Malformed cursor", 400

    return jsonify(body)
