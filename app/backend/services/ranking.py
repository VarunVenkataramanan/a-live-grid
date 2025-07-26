import math
from datetime import datetime

from geopy.distance import geodesic


class RerankingService:
	"""
	Reranking algorithm based on:
	1. Number of upvotes
	2. User uploaded reports based on location
	3. Proximity/accuracy of uploaded post location
	"""

	def __init__(self):
		self.location_weight = 0.4
		self.upvote_weight = 0.4
		self.recency_weight = 0.2

	def rerank_posts_json(self, posts: list[dict], user_lat: float, user_lng: float) -> list[dict]:
		"""
		Rerank posts based on user location and other factors (JSON version)
		"""
		if not posts:
			return posts

		# Calculate scores for each post
		scored_posts = []
		for post in posts:
			score = self._calculate_post_score_json(post, user_lat, user_lng)
			scored_posts.append((post, score))

		# Sort by score (descending)
		scored_posts.sort(key=lambda x: x[1], reverse=True)

		# Return sorted posts
		return [post for post, score in scored_posts]

	def _calculate_post_score_json(self, post: dict, user_lat: float, user_lng: float) -> float:
		"""
		Calculate a score for a post based on multiple factors (JSON version)
		"""
		# Location proximity score (0-1, higher is closer)
		location_score = self._calculate_location_score_json(post, user_lat, user_lng)

		# Upvote score (0-1, higher is more upvotes)
		upvote_score = self._calculate_upvote_score_json(post)

		# Recency score (0-1, higher is more recent)
		recency_score = self._calculate_recency_score_json(post)

		# Weighted combination
		total_score = self.location_weight * location_score + self.upvote_weight * upvote_score + self.recency_weight * recency_score

		return total_score

	def _calculate_location_score_json(self, post: dict, user_lat: float, user_lng: float) -> float:
		"""
		Calculate location proximity score (JSON version)
		"""
		geolocation = post.get("Geolocation", [])
		if not geolocation or len(geolocation) < 2:
			return 0.5  # Default score for posts without coordinates

		# Calculate distance in kilometers
		post_location = (geolocation[0], geolocation[1])
		user_location = (user_lat, user_lng)
		distance = geodesic(user_location, post_location).kilometers

		# Convert distance to score (closer = higher score)
		# Exponential decay: score = e^(-distance/10)
		score = math.exp(-distance / 10)

		return min(1.0, max(0.0, score))

	def _calculate_upvote_score_json(self, post: dict) -> float:
		"""
		Calculate upvote-based score (JSON version)
		"""
		total_votes = post.get("upvote_count", 0) + post.get("downvote_count", 0)
		if total_votes == 0:
			return 0.5  # Default score for posts with no votes

		upvote_count = post.get("upvote_count", 0)

		# Apply logarithmic scaling to prevent extremely popular posts from dominating
		score = math.log(1 + upvote_count) / math.log(100)  # Normalize to 0-1

		return min(1.0, max(0.0, score))

	def _calculate_recency_score_json(self, post: dict) -> float:
		"""
		Calculate recency score (JSON version)
		"""
		try:
			created_at = datetime.fromisoformat(post["created_at"].replace("Z", "+00:00"))
			now = datetime.utcnow()
			age_hours = (now - created_at).total_seconds() / 3600

			# Exponential decay: newer posts get higher scores
			score = math.exp(-age_hours / 24)  # 24-hour half-life

			return min(1.0, max(0.0, score))
		except:
			return 0.5  # Default score if date parsing fails
