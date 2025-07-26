import json
import os
from typing import List, Dict, Optional
from datetime import datetime
import uuid

class DataService:
    """Service to handle JSON data operations"""
    
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(__file__), "..", "..", "data", "sample_data.json")
        self.posts = self._load_data()
        self.votes = {}  # Store votes in memory: {post_id: {user_id: vote_type}}
    
    def _load_data(self) -> List[Dict]:
        """Load data from JSON file"""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return data.get('posts', [])
        except FileNotFoundError:
            print(f"Data file not found: {self.data_file}")
            return []
        except json.JSONDecodeError:
            print(f"Invalid JSON in data file: {self.data_file}")
            return []
    
    def _save_data(self):
        """Save data to JSON file"""
        try:
            data = {"posts": self.posts}
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def get_all_posts(self) -> List[Dict]:
        """Get all posts"""
        return self.posts
    
    def get_post_by_id(self, post_id: int) -> Optional[Dict]:
        """Get post by ID"""
        for post in self.posts:
            if post['id'] == post_id:
                return post
        return None
    
    def create_post(self, post_data: Dict) -> Dict:
        """Create a new post"""
        new_post = {
            'id': len(self.posts) + 1,
            'username': post_data.get('username', 'anonymous'),
            'title': post_data['title'],
            'short_description': post_data['short_description'],
            'long_description': post_data['long_description'],
            'image_url': post_data.get('image_url'),
            'location': post_data['location'],
            'latitude': post_data.get('latitude'),
            'longitude': post_data.get('longitude'),
            'upvote_count': 0,
            'downvote_count': 0,
            'karma': 0.0,
            'created_at': datetime.now().isoformat()
        }
        
        self.posts.append(new_post)
        self._save_data()
        return new_post
    
    def vote_post(self, post_id: int, user_id: str, vote_type: str) -> bool:
        """Vote on a post"""
        post = self.get_post_by_id(post_id)
        if not post:
            return False
        
        # Initialize votes for this post if not exists
        if post_id not in self.votes:
            self.votes[post_id] = {}
        
        # Check if user already voted
        if user_id in self.votes[post_id]:
            old_vote = self.votes[post_id][user_id]
            # Remove old vote
            if old_vote == 'upvote':
                post['upvote_count'] -= 1
            else:
                post['downvote_count'] -= 1
        
        # Add new vote
        self.votes[post_id][user_id] = vote_type
        if vote_type == 'upvote':
            post['upvote_count'] += 1
        else:
            post['downvote_count'] += 1
        
        # Recalculate karma
        post['karma'] = self._calculate_karma(post['upvote_count'])
        
        self._save_data()
        return True
    
    def _calculate_karma(self, upvotes: int) -> float:
        """Calculate karma using exponential decay"""
        if upvotes == 0:
            return 0.0
        
        karma = 0.0
        for i in range(1, upvotes + 1):
            karma += 1.0 / (i ** 0.5)  # Exponential decay
        
        return karma
    
    def get_posts_short(self) -> List[Dict]:
        """Get posts with short format (username, title, image)"""
        return [
            {
                'id': post['id'],
                'username': post['username'],
                'title': post['title'],
                'short_description': post['short_description'],
                'image_url': post.get('image_url'),
                'upvote_count': post['upvote_count'],
                'downvote_count': post['downvote_count'],
                'karma': post['karma'],
                'created_at': post['created_at']
            }
            for post in self.posts
        ]
    
    def get_posts_long(self) -> List[Dict]:
        """Get posts with full data"""
        return self.posts.copy()

# Global instance
data_service = DataService() 