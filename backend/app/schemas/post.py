from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PostBase(BaseModel):
    title: str
    short_description: str
    long_description: str
    location: str
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class PostCreate(PostBase):
    image_url: Optional[str] = None
    username: Optional[str] = None

class PostShortResponse(BaseModel):
    id: int
    username: str
    title: str
    short_description: str
    image_url: Optional[str]
    upvote_count: int
    downvote_count: int
    karma: float
    created_at: str

class PostResponse(PostBase):
    id: int
    username: str
    image_url: Optional[str]
    upvote_count: int
    downvote_count: int
    karma: float
    created_at: str

class VoteRequest(BaseModel):
    vote_type: str  # "upvote" or "downvote"
    user_id: str 