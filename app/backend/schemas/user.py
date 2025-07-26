from datetime import datetime

from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
	username: str
	email: EmailStr
	full_name: str | None = None
	bio: str | None = None
	profile_image: str | None = None


class UserCreate(UserBase):
	password: str


class UserUpdate(BaseModel):
	username: str | None = None
	email: EmailStr | None = None
	full_name: str | None = None
	bio: str | None = None
	profile_image: str | None = None


class UserResponse(UserBase):
	id: str
	created_at: datetime
	updated_at: datetime
	karma: float = 0.0
	post_count: int = 0

	class Config:
		from_attributes = True


class UserLogin(BaseModel):
	email: EmailStr
	password: str


class UserToken(BaseModel):
	access_token: str
	token_type: str = "bearer"
	user: UserResponse
