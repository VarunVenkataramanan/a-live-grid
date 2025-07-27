import json
import os
from datetime import datetime


class DataService:
	def __init__(self):
		self.data_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_data.json")
		self.posts = self._load_data()
		self.votes = {}  # Store votes in memory: {post_id: {user_id: vote_type}}

	def _load_data(self) -> list[dict]:
		"""Load data from JSON file"""
		try:
			if os.path.exists(self.data_file):
				with open(self.data_file, encoding="utf-8") as f:
					data = json.load(f)
					# Handle both direct array and {"posts": [...]} structure
					if isinstance(data, dict) and "posts" in data:
						return data["posts"]
					elif isinstance(data, list):
						return data
					else:
						print(f"Unexpected data format in {self.data_file}")
						return []
			else:
				# Create sample data if file doesn't exist
				sample_data = self._create_sample_data()
				self._save_data(sample_data)
				return sample_data
		except Exception as e:
			print(f"Error loading data: {e}")
			return []

	def _save_data(self, data: list[dict] = None):
		"""Save data to JSON file"""
		try:
			os.makedirs(os.path.dirname(self.data_file), exist_ok=True)
			# Save in the format {"posts": [...]} to match existing structure
			save_data = {"posts": data or self.posts}
			with open(self.data_file, "w", encoding="utf-8") as f:
				json.dump(save_data, f, indent=2, ensure_ascii=False)
		except Exception as e:
			print(f"Error saving data: {e}")

	def _create_sample_data(self) -> list[dict]:
		"""Create sample data with category field"""
		return [
			{
				"id": 1,
				"username": "traffic_reporter",
				"title": "Heavy Traffic on MG Road",
				"description": "There is heavy traffic on MG Road near Brigade Road junction. Avoid this route if possible.",
				"image_bitmap": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
				"upvote_count": 15,
				"downvote_count": 2,
				"karma": 7.5,
				"created_at": "2024-01-15T10:30:00Z",
				"Geolocation": [12.9716, 77.5946],
				"user_id": "user_123",
				"category": ["traffic", "road"],
			},
			{
				"id": 2,
				"username": "weather_watcher",
				"title": "Rain Alert - Bangalore",
				"description": "Heavy rainfall is expected in Bangalore today. Carry umbrellas and expect delays.",
				"image_bitmap": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
				"upvote_count": 23,
				"downvote_count": 1,
				"karma": 11.5,
				"created_at": "2024-01-15T11:00:00Z",
				"Geolocation": [12.9716, 77.5946],
				"user_id": "user_456",
				"category": ["weather", "rain"],
			},
			{
				"id": 3,
				"username": "event_planner",
				"title": "Food Festival at UB City",
				"description": "Don't miss the amazing food festival at UB City this weekend. Great variety of cuisines available.",
				"image_bitmap": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
				"upvote_count": 45,
				"downvote_count": 3,
				"karma": 22.5,
				"created_at": "2024-01-15T12:00:00Z",
				"Geolocation": [12.9716, 77.5946],
				"user_id": "user_789",
				"category": ["event", "food"],
			},
			{
				"id": 4,
				"username": "sports_fan",
				"title": "Cricket Match at Chinnaswamy",
				"description": "Don't miss the exciting cricket match at Chinnaswamy Stadium today. India vs Australia!",
				"image_bitmap": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
				"upvote_count": 67,
				"downvote_count": 5,
				"karma": 33.5,
				"created_at": "2024-01-15T13:00:00Z",
				"Geolocation": [12.9716, 77.5946],
				"user_id": "user_101",
				"category": ["sports", "cricket"],
			},
			{
				"id": 5,
				"username": "tech_news",
				"title": "New Tech Startup in Koramangala",
				"description": "A new AI startup has launched in Koramangala. They're working on innovative machine learning solutions.",
				"image_bitmap": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
				"upvote_count": 34,
				"downvote_count": 2,
				"karma": 17.0,
				"created_at": "2024-01-15T14:00:00Z",
				"Geolocation": [12.9716, 77.5946],
				"user_id": "user_202",
				"category": ["technology", "startup"],
			},
			{
				"id": 6,
				"username": "health_advisor",
				"title": "Yoga Classes at Lalbagh",
				"description": "Join free yoga classes at Lalbagh Botanical Garden every morning at 6 AM. Great for health and wellness.",
				"image_bitmap": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
				"upvote_count": 28,
				"downvote_count": 1,
				"karma": 14.0,
				"created_at": "2024-01-15T15:00:00Z",
				"Geolocation": [12.9716, 77.5946],
				"user_id": "user_303",
				"category": ["health", "yoga"],
			},
			{
				"id": 7,
				"username": "music_lover",
				"title": "Live Music at Hard Rock Cafe",
				"description": "Don't miss the amazing live band performance at Hard Rock Cafe tonight. Great music and atmosphere!",
				"image_bitmap": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
				"upvote_count": 39,
				"downvote_count": 4,
				"karma": 19.5,
				"created_at": "2024-01-15T16:00:00Z",
				"Geolocation": [12.9716, 77.5946],
				"user_id": "user_404",
				"category": ["music", "entertainment"],
			},
			{
				"id": 8,
				"username": "art_enthusiast",
				"title": "Art Exhibition at NGMA",
				"description": "Visit the contemporary art exhibition at National Gallery of Modern Art. Amazing works by local artists.",
				"image_bitmap": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
				"upvote_count": 19,
				"downvote_count": 2,
				"karma": 9.5,
				"created_at": "2024-01-15T17:00:00Z",
				"Geolocation": [12.9716, 77.5946],
				"user_id": "user_505",
				"category": ["art", "culture"],
			},
			{
				"id": 9,
				"username": "shopping_guide",
				"title": "Sale at Phoenix MarketCity",
				"description": "Massive sale at Phoenix MarketCity with up to 70% off on electronics and gadgets. Don't miss out!",
				"image_bitmap": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
				"upvote_count": 52,
				"downvote_count": 6,
				"karma": 26.0,
				"created_at": "2024-01-15T18:00:00Z",
				"Geolocation": [12.9716, 77.5946],
				"user_id": "user_606",
				"category": ["shopping", "sale"],
			},
			{
				"id": 10,
				"username": "fitness_trainer",
				"title": "New Gym Opening in Indiranagar",
				"description": "A new state-of-the-art fitness center is opening in Indiranagar. Modern equipment and expert trainers available.",
				"image_bitmap": "data:image/jpeg;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNkYPhfDwAChwGA60e6kgAAAABJRU5ErkJggg==",
				"upvote_count": 31,
				"downvote_count": 3,
				"karma": 15.5,
				"created_at": "2024-01-15T19:00:00Z",
				"Geolocation": [12.9716, 77.5946],
				"user_id": "user_707",
				"category": ["fitness", "health"],
			},
		]

	def get_all_posts(self) -> list[dict]:
		"""Get all posts"""
		return self.posts

	def get_post_by_id(self, post_id: int) -> dict | None:
		"""Get post by ID"""
		for post in self.posts:
			if post.get("id") == post_id:
				return post
		return None

	def create_post(self, post_data: dict) -> dict:
		"""Create a new post"""
		# Generate new ID
		new_id = max([post.get("id", 0) for post in self.posts]) + 1

		# Create post with default values
		new_post = {
			"id": new_id,
			"username": post_data.get("username", "Anonymous"),
			"title": post_data.get("title", ""),
			"description": post_data.get("description", ""),
			"image_bitmap": post_data.get("image_bitmap"),
			"upvote_count": 0,
			"downvote_count": 0,
			"karma": 0.0,
			"created_at": datetime.utcnow().isoformat() + "Z",
			"Geolocation": post_data.get("Geolocation", [0.0, 0.0]),
			"user_id": post_data.get("user_id", "unknown"),
			"category": post_data.get("category", []),
		}

		# Add to posts list
		self.posts.append(new_post)

		# Save to file
		self._save_data()

		return new_post

	def vote_post(self, post_id: int, user_id: str, vote_type: str) -> bool:
		"""Vote on a post"""
		post = self.get_post_by_id(post_id)
		if not post:
			return False

		# Check if user already voted
		if post_id not in self.votes:
			self.votes[post_id] = {}

		if user_id in self.votes[post_id]:
			# User already voted, remove previous vote
			previous_vote = self.votes[post_id][user_id]
			if previous_vote == "upvote":
				post["upvote_count"] -= 1
			elif previous_vote == "downvote":
				post["downvote_count"] -= 1

		# Add new vote
		self.votes[post_id][user_id] = vote_type

		if vote_type == "upvote":
			post["upvote_count"] += 1
		elif vote_type == "downvote":
			post["downvote_count"] += 1

		# Recalculate karma
		post["karma"] = self._calculate_karma(post["upvote_count"])

		# Save to file
		self._save_data()

		return True

	def _calculate_karma(self, upvotes: int) -> float:
		"""Calculate karma based on upvotes"""
		if upvotes <= 0:
			return 0.0
		return round(upvotes * 0.5, 2)

	def get_posts_short(self) -> list[dict]:
		"""Get posts in short format"""
		return [
			{
				"id": post["id"],
				"username": post["username"],
				"title": post["title"],
				"image_bitmap": post.get("image_bitmap"),
				"upvote_count": post["upvote_count"],
				"downvote_count": post["downvote_count"],
				"karma": post["karma"],
				"created_at": post["created_at"],
				"Geolocation": post["Geolocation"],
				"user_id": post["user_id"],
			}
			for post in self.posts
		]

	def get_posts_long(self) -> list[dict]:
		"""Get posts in full format"""
		return [
			{
				"id": post["id"],
				"username": post["username"],
				"title": post["title"],
				"description": post.get("description") or post.get("long_description") or post.get("short_description", ""),
				"image_bitmap": post.get("image_bitmap"),
				"upvote_count": post["upvote_count"],
				"downvote_count": post["downvote_count"],
				"karma": post["karma"],
				"created_at": post["created_at"],
				"Geolocation": post["Geolocation"],
				"user_id": post["user_id"],
				"category": post.get("category", []),
			}
			for post in self.posts
		]

	def delete_post(self, post_id: int) -> bool:
		"""Delete a post"""
		for i, post in enumerate(self.posts):
			if post.get("id") == post_id:
				del self.posts[i]
				self._save_data()
				return True
		return False


# Global data service instance
data_service = DataService()
