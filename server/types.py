from typing import List, Literal
from pydantic import BaseModel, Field


class DIDService(BaseModel):
    id: str
    type: Literal["BskyFeedGenerator"]
    serviceEndpoint: str


class DIDDocument(BaseModel):
    context: List[str] = Field(["https://www.w3.org/ns/did/v1"], alias="@context")
    id: str
    service: List[DIDService]

    class Config:
        json_schema_extra = {
            "example": {
                "@context": ["https://www.w3.org/ns/did/v1"],
                "id": "did:web:example.com",
                "service": [
                    {
                        "id": "#bsky_fg",
                        "type": "BskyFeedGenerator",
                        "serviceEndpoint": "https://example.com",
                    }
                ],
            }
        }
        populate_by_name = True


class FeedDescriptor(BaseModel):
    uri: str


class DescribeFeedGeneratorResponse(BaseModel):
    encoding: Literal["application/json"]
    body: dict[str, object] = {"did": str, "feeds": List[FeedDescriptor]}


class FeedPost(BaseModel):
    post: str = Field(
        pattern=r"^at://did:plc:[a-zA-Z0-9]+/app\.bsky\.feed\.post/[a-zA-Z0-9]+$"
    )


class FeedResponse(BaseModel):
    cursor: str
    feed: List[FeedPost]
