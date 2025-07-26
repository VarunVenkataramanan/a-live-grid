import uuid
from datetime import datetime
from typing import Any

import firebase_admin
from firebase_admin import credentials, firestore
from google.cloud import firestore as google_firestore

from app.backend.core.config import settings


class FirestoreService:
	def __init__(self):
		self.db = None
		self._initialize_firestore()

	def _initialize_firestore(self):
		"""Initialize Firestore connection"""
		try:
			# Check if Firebase Admin is already initialized
			if not firebase_admin._apps:
				# Use service account credentials if provided
				if settings.GOOGLE_APPLICATION_CREDENTIALS:
					cred = credentials.Certificate(settings.GOOGLE_APPLICATION_CREDENTIALS)
					firebase_admin.initialize_app(cred)
				else:
					# Use default credentials (for local development)
					firebase_admin.initialize_app()

			self.db = firestore.client()
			print("✅ Firestore initialized successfully")

		except Exception as e:
			print(f"❌ Error initializing Firestore: {e}")
			# Fallback to local JSON for development
			self.db = None

	def is_connected(self) -> bool:
		"""Check if Firestore is connected"""
		return self.db is not None

	# User Operations
	async def create_user(self, user_data: dict[str, Any]) -> str:
		"""Create a new user"""
		if not self.is_connected():
			return None

		try:
			user_id = str(uuid.uuid4())
			user_data["id"] = user_id
			user_data["created_at"] = datetime.utcnow()
			user_data["updated_at"] = datetime.utcnow()

			doc_ref = self.db.collection(settings.USERS_COLLECTION).document(user_id)
			doc_ref.set(user_data)

			return user_id
		except Exception as e:
			print(f"Error creating user: {e}")
			return None

	async def get_user(self, user_id: str) -> dict[str, Any] | None:
		"""Get user by ID"""
		if not self.is_connected():
			return None

		try:
			doc_ref = self.db.collection(settings.USERS_COLLECTION).document(user_id)
			doc = doc_ref.get()

			if doc.exists:
				return doc.to_dict()
			return None
		except Exception as e:
			print(f"Error getting user: {e}")
			return None

	async def update_user(self, user_id: str, user_data: dict[str, Any]) -> bool:
		"""Update user data"""
		if not self.is_connected():
			return False

		try:
			user_data["updated_at"] = datetime.utcnow()
			doc_ref = self.db.collection(settings.USERS_COLLECTION).document(user_id)
			doc_ref.update(user_data)
			return True
		except Exception as e:
			print(f"Error updating user: {e}")
			return False

	async def delete_user(self, user_id: str) -> bool:
		"""Delete user"""
		if not self.is_connected():
			return False

		try:
			doc_ref = self.db.collection(settings.USERS_COLLECTION).document(user_id)
			doc_ref.delete()
			return True
		except Exception as e:
			print(f"Error deleting user: {e}")
			return False

	# Post Operations
	async def create_post(self, post_data: dict[str, Any]) -> str:
		"""Create a new post"""
		if not self.is_connected():
			return None

		try:
			post_id = str(uuid.uuid4())
			post_data["id"] = post_id
			post_data["created_at"] = datetime.utcnow()
			post_data["updated_at"] = datetime.utcnow()
			post_data["upvote_count"] = 0
			post_data["downvote_count"] = 0
			post_data["karma"] = 0.0

			doc_ref = self.db.collection(settings.POSTS_COLLECTION).document(post_id)
			doc_ref.set(post_data)

			return post_id
		except Exception as e:
			print(f"Error creating post: {e}")
			return None

	async def get_post(self, post_id: str) -> dict[str, Any] | None:
		"""Get post by ID"""
		if not self.is_connected():
			return None

		try:
			doc_ref = self.db.collection(settings.POSTS_COLLECTION).document(post_id)
			doc = doc_ref.get()

			if doc.exists:
				return doc.to_dict()
			return None
		except Exception as e:
			print(f"Error getting post: {e}")
			return None

	async def get_posts(self, limit: int = 50, offset: int = 0) -> list[dict[str, Any]]:
		"""Get posts with pagination"""
		if not self.is_connected():
			return []

		try:
			posts_ref = self.db.collection(settings.POSTS_COLLECTION)
			posts_ref = posts_ref.order_by("created_at", direction=firestore.Query.DESCENDING)
			posts_ref = posts_ref.limit(limit).offset(offset)

			docs = posts_ref.stream()
			posts = []

			for doc in docs:
				post_data = doc.to_dict()
				posts.append(post_data)

			return posts
		except Exception as e:
			print(f"Error getting posts: {e}")
			return []

	async def update_post(self, post_id: str, post_data: dict[str, Any]) -> bool:
		"""Update post data"""
		if not self.is_connected():
			return False

		try:
			post_data["updated_at"] = datetime.utcnow()
			doc_ref = self.db.collection(settings.POSTS_COLLECTION).document(post_id)
			doc_ref.update(post_data)
			return True
		except Exception as e:
			print(f"Error updating post: {e}")
			return False

	async def delete_post(self, post_id: str) -> bool:
		"""Delete post"""
		if not self.is_connected():
			return False

		try:
			doc_ref = self.db.collection(settings.POSTS_COLLECTION).document(post_id)
			doc_ref.delete()
			return True
		except Exception as e:
			print(f"Error deleting post: {e}")
			return False

	# Vote Operations
	async def vote_post(self, post_id: str, user_id: str, vote_type: str) -> bool:
		"""Vote on a post (upvote/downvote)"""
		if not self.is_connected():
			return False

		try:
			# Get current post
			post = await self.get_post(post_id)
			if not post:
				return False

			# Update vote counts
			if vote_type == "upvote":
				post["upvote_count"] += 1
			elif vote_type == "downvote":
				post["downvote_count"] += 1

			# Recalculate karma
			post["karma"] = self._calculate_karma(post["upvote_count"])

			# Update post
			await self.update_post(post_id, post)

			# Store vote record
			vote_data = {
				"post_id": post_id,
				"user_id": user_id,
				"vote_type": vote_type,
				"created_at": datetime.utcnow(),
			}

			vote_id = f"{post_id}_{user_id}"
			doc_ref = self.db.collection(settings.VOTES_COLLECTION).document(vote_id)
			doc_ref.set(vote_data)

			return True
		except Exception as e:
			print(f"Error voting on post: {e}")
			return False

	def _calculate_karma(self, upvotes: int) -> float:
		"""Calculate karma based on upvotes"""
		if upvotes <= 0:
			return 0.0
		return round(upvotes * 0.5, 2)

	# Search Operations
	async def search_posts_by_location(self, lat: float, lng: float, radius_km: float = 10) -> list[dict[str, Any]]:
		"""Search posts by location"""
		if not self.is_connected():
			return []

		try:
			# Note: Firestore doesn't support native geospatial queries
			# This is a simplified implementation
			# For production, consider using GeoFirestore or similar
			posts = await self.get_posts(limit=100)

			# Filter by distance
			filtered_posts = []
			for post in posts:
				if "Geolocation" in post and len(post["Geolocation"]) >= 2:
					post_lat, post_lng = post["Geolocation"][0], post["Geolocation"][1]
					distance = self._calculate_distance(lat, lng, post_lat, post_lng)

					if distance <= radius_km:
						filtered_posts.append(post)

			return filtered_posts
		except Exception as e:
			print(f"Error searching posts by location: {e}")
			return []

	def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
		"""Calculate distance between two points in kilometers"""
		from geopy.distance import geodesic

		return geodesic((lat1, lng1), (lat2, lng2)).kilometers


# Global Firestore service instance
firestore_service = FirestoreService()
