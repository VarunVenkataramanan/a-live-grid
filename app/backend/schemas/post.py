from pydantic import BaseModel


class PostBase(BaseModel):
	title: str
	description: str


class PostCreate(PostBase):
	image_bitmap: str | None = None
	username: str | None = None
	Geolocation: list[float] | None = None
	user_id: str | None = None
	category: list[str] | None = None


class PostShortResponse(BaseModel):
	id: int
	username: str
	title: str
	image_bitmap: str | None
	upvote_count: int
	downvote_count: int
	karma: float
	created_at: str
	Geolocation: list[float]
	user_id: str


class PostResponse(PostBase):
	id: int
	username: str
	image_bitmap: str | None
	upvote_count: int
	downvote_count: int
	karma: float
	created_at: str
	Geolocation: list[float]
	user_id: str
	category: list[str] | None = None


class VoteRequest(BaseModel):
	vote_type: str  # "upvote" or "downvote"
	user_id: str
