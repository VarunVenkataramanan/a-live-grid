from datetime import timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.backend.core.config import settings
from app.backend.core.firestore import firestore_service
from app.backend.core.security import create_access_token, get_password_hash, verify_password
from app.backend.schemas.user import UserCreate, UserLogin, UserResponse, UserToken, UserUpdate

router = APIRouter()


# Helper functions (you'll need to implement these)
async def get_current_user_id():
	"""Get current user ID from token"""
	# This would be implemented with JWT token validation
	# For now, return a placeholder
	return "current_user_id"


async def get_user_by_email(email: str):
	"""Get user by email"""
	# This would be implemented in the FirestoreService
	# For now, return None
	return


@router.post("/register", response_model=UserResponse)
async def register_user(user: UserCreate):
	"""
	Register a new user
	"""
	try:
		# Check if user already exists
		# Note: In a real app, you'd check by email
		existing_user = await firestore_service.get_user_by_email(user.email)
		if existing_user:
			raise HTTPException(
				status_code=status.HTTP_400_BAD_REQUEST,
				detail="User with this email already exists",
			)

		# Hash password
		hashed_password = get_password_hash(user.password)

		# Create user data
		user_data = user.dict()
		user_data["password"] = hashed_password
		user_data["karma"] = 0.0
		user_data["post_count"] = 0

		# Create user in Firestore
		user_id = await firestore_service.create_user(user_data)

		if not user_id:
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail="Failed to create user",
			)

		# Get created user
		created_user = await firestore_service.get_user(user_id)
		return UserResponse(**created_user)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Error creating user: {e!s}",
		)


@router.post("/login", response_model=UserToken)
async def login_user(user_credentials: UserLogin):
	"""
	Login user and return access token
	"""
	try:
		# Get user by email
		user = await firestore_service.get_user_by_email(user_credentials.email)
		if not user:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Invalid email or password",
			)

		# Verify password
		if not verify_password(user_credentials.password, user["password"]):
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Invalid email or password",
			)

		# Create access token
		access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
		access_token = create_access_token(
			data={"sub": user["id"]},
			expires_delta=access_token_expires,
		)

		return UserToken(
			access_token=access_token,
			user=UserResponse(**user),
		)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Error during login: {e!s}",
		)


@router.get("/me", response_model=UserResponse)
async def get_current_user(current_user_id: str = Depends(get_current_user_id)):
	"""
	Get current user profile
	"""
	try:
		user = await firestore_service.get_user(current_user_id)
		if not user:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="User not found",
			)

		return UserResponse(**user)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Error getting user: {e!s}",
		)


@router.put("/me", response_model=UserResponse)
async def update_current_user(
	user_update: UserUpdate,
	current_user_id: str = Depends(get_current_user_id),
):
	"""
	Update current user profile
	"""
	try:
		# Get current user
		user = await firestore_service.get_user(current_user_id)
		if not user:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="User not found",
			)

		# Update user data
		update_data = user_update.dict(exclude_unset=True)
		success = await firestore_service.update_user(current_user_id, update_data)

		if not success:
			raise HTTPException(
				status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
				detail="Failed to update user",
			)

		# Get updated user
		updated_user = await firestore_service.get_user(current_user_id)
		return UserResponse(**updated_user)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Error updating user: {e!s}",
		)


@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
	"""
	Get user by ID
	"""
	try:
		user = await firestore_service.get_user(user_id)
		if not user:
			raise HTTPException(
				status_code=status.HTTP_404_NOT_FOUND,
				detail="User not found",
			)

		return UserResponse(**user)

	except Exception as e:
		raise HTTPException(
			status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
			detail=f"Error getting user: {e!s}",
		)
