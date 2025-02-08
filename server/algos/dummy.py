from typing import Optional
from server.types import FeedPost, FeedResponse

posts = [
    "at://did:plc:6w6c3aaefvfx5h4oye37wdjc/app.bsky.feed.post/3lho5h7owsk2h",
    "at://did:plc:ulgja7eud73o4bvz4zgietqd/app.bsky.feed.post/3lho5h6jhlk2o",
    "at://did:plc:6ck6mjjqtfbwjviep3guifxr/app.bsky.feed.post/3lho5h36iqc2q",
    "at://did:plc:sr4wuggvstlv55uqapafa4oc/app.bsky.feed.post/3lho5h2k7d22d",
    "at://did:plc:e76ty7fuvz73us327ce4yx6s/app.bsky.feed.post/3lho5h26dqg2n",
    "at://did:plc:pzcbboorkxh3ko2fmdrmu346/app.bsky.feed.post/3lho5gzl3a22o",
    "at://did:plc:q7hjfjt3tffg5bpbwgrlntq6/app.bsky.feed.post/3lho5gy3cvs2h",
    "at://did:plc:6tzj6dh3qxuaeagtw2k7a52e/app.bsky.feed.post/3lho5gysvs22n",
    "at://did:plc:on7k77y322ged7maeh2x4dx5/app.bsky.feed.post/3lho5gt3vds2q",
    "at://did:plc:bihpfcu47hc64v3y6m2v55oz/app.bsky.feed.post/3lho5gr732k2t",
    "at://did:plc:lh4cafnee4nki6rnjud2b42z/app.bsky.feed.post/3lho5gjzoac2d",
]


def handler(cursor: Optional[str], limit: int) -> FeedResponse:
    return FeedResponse(cursor="none", feed=[FeedPost(post=post) for post in posts])
