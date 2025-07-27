from typing import Any

import firebase_admin
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from firebase_admin import auth, credentials

from app.core.config import settings

# Initialize Firebase Admin SDK
try:
	if not firebase_admin._apps:
		# Use service account credentials if provided
		if settings.GOOGLE_APPLICATION_CREDENTIALS:
			cred = credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
			firebase_admin.initialize_app(cred)
		else:
			# Use default credentials (for local development)
			firebase_admin.initialize_app()
	print("✅ Firebase Admin SDK initialized successfully")
except Exception as e:
	print(f"❌ Error initializing Firebase Admin SDK: {e}")

# Security scheme for JWT tokens
security = HTTPBearer()


class FirebaseAuth:
	"""Firebase Authentication Service"""

	@staticmethod
	async def verify_token(token: str) -> dict[str, Any] | None:
		"""
		Verify Firebase ID token and return user info
		"""
		try:
			# Verify the Firebase ID token
			decoded_token = auth.verify_id_token(token)

			# Extract user information
			user_info = {
				"uid": decoded_token["uid"],
				"email": decoded_token.get("email"),
				"email_verified": decoded_token.get("email_verified", False),
				"name": decoded_token.get("name"),
				"picture": decoded_token.get("picture"),
				"provider_id": decoded_token.get("firebase", {}).get("sign_in_provider", "google"),
			}

			return user_info

		except auth.ExpiredIdTokenError:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token has expired",
			)
		except auth.RevokedIdTokenError:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Token has been revoked",
			)
		except auth.InvalidIdTokenError:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail="Invalid token",
			)
		except Exception as e:
			raise HTTPException(
				status_code=status.HTTP_401_UNAUTHORIZED,
				detail=f"Token verification failed: {e!s}",
			)

	@staticmethod
	async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, Any]:
		"""
		Get current user from Firebase token
		"""
		token = credentials.credentials
		user_info = await FirebaseAuth.verify_token(token)
		return user_info

	@staticmethod
	async def get_user_by_uid(uid: str) -> dict[str, Any] | None:
		"""
		Get user information from Firebase by UID
		"""
		try:
			user_record = auth.get_user(uid)
			return {
				"uid": user_record.uid,
				"email": user_record.email,
				"email_verified": user_record.email_verified,
				"display_name": user_record.display_name,
				"photo_url": user_record.photo_url,
				"disabled": user_record.disabled,
				"created_at": user_record.user_metadata.creation_timestamp,
				"last_sign_in": user_record.user_metadata.last_sign_in_timestamp,
			}
		except auth.UserNotFoundError:
			return None
		except Exception as e:
			print(f"Error getting user by UID: {e}")
			return None

	@staticmethod
	async def create_custom_token(uid: str, additional_claims: dict | None = None) -> str:
		"""
		Create a custom token for a user
		"""
		try:
			custom_token = auth.create_custom_token(uid, additional_claims)
			return custom_token.decode("utf-8")
		except Exception as e:
			print(f"Error creating custom token: {e}")
			return None


# Dependency for getting current user
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict[str, Any]:
	"""
	FastAPI dependency to get current authenticated user
	"""
	return await FirebaseAuth.get_current_user(credentials)


async def get_current_user_uid(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
	"""
	FastAPI dependency to get current user UID
	"""
	user_info = await FirebaseAuth.get_current_user(credentials)
	return user_info["uid"]
