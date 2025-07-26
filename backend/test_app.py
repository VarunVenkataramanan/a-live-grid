#!/usr/bin/env python3
"""
Simple test to verify the A-Live-Grid Backend works with JSON data
"""

def test_data_service():
    """Test the data service"""
    print("🧪 Testing Data Service...")
    
    try:
        from app.services.data_service import data_service
        
        # Test loading data
        posts = data_service.get_all_posts()
        print(f"✅ Loaded {len(posts)} posts from JSON")
        
        # Test getting short posts
        short_posts = data_service.get_posts_short()
        print(f"✅ Got {len(short_posts)} short posts")
        
        # Test getting long posts
        long_posts = data_service.get_posts_long()
        print(f"✅ Got {len(long_posts)} long posts")
        
        # Test getting specific post
        if posts:
            post = data_service.get_post_by_id(1)
            if post:
                print(f"✅ Retrieved post ID 1: {post['title']}")
            else:
                print("❌ Failed to retrieve post ID 1")
        
        return True
        
    except Exception as e:
        print(f"❌ Data service test failed: {e}")
        return False

def test_ranking_service():
    """Test the ranking service"""
    print("\n🧪 Testing Ranking Service...")
    
    try:
        from app.services.ranking import RerankingService
        from app.services.data_service import data_service
        
        reranking_service = RerankingService()
        posts = data_service.get_all_posts()
        
        if posts:
            # Test reranking with location
            reranked_posts = reranking_service.rerank_posts_json(posts, 12.9716, 77.5946)
            print(f"✅ Reranked {len(reranked_posts)} posts")
        
        return True
        
    except Exception as e:
        print(f"❌ Ranking service test failed: {e}")
        return False

def test_api_endpoints():
    """Test API endpoints"""
    print("\n🧪 Testing API Endpoints...")
    
    try:
        from fastapi.testclient import TestClient
        from app.main import app
        
        client = TestClient(app)
        
        # Test health endpoint
        response = client.get("/health")
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"❌ Health endpoint failed: {response.status_code}")
            return False
        
        # Test posts short endpoint
        response = client.get("/api/v1/posts/short")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Posts short endpoint working - {len(data)} posts")
        else:
            print(f"❌ Posts short endpoint failed: {response.status_code}")
            return False
        
        # Test posts long endpoint
        response = client.get("/api/v1/posts/long")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Posts long endpoint working - {len(data)} posts")
        else:
            print(f"❌ Posts long endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"❌ API endpoints test failed: {e}")
        return False

def main():
    print("🚀 Testing A-Live-Grid Backend (JSON Version)...")
    
    # Test data service
    if not test_data_service():
        return False
    
    # Test ranking service
    if not test_ranking_service():
        return False
    
    # Test API endpoints
    if not test_api_endpoints():
        return False
    
    print("\n🎉 All tests passed! The backend is working correctly.")
    print("\n📋 You can now:")
    print("1. Run: python run.py")
    print("2. Visit http://localhost:8000/docs for API documentation")
    print("3. Test the endpoints with the sample data")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 