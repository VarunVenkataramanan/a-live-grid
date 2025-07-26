#!/usr/bin/env python3
"""
Quick test to verify the app starts without errors
"""

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from app.main import app
        print("✅ Main app imported successfully")
    except Exception as e:
        print(f"❌ Main app import failed: {e}")
        return False
    
    try:
        from app.services.data_service import data_service
        print("✅ Data service imported successfully")
    except Exception as e:
        print(f"❌ Data service import failed: {e}")
        return False
    
    try:
        from app.services.ranking import RerankingService
        print("✅ Ranking service imported successfully")
    except Exception as e:
        print(f"❌ Ranking service import failed: {e}")
        return False
    
    return True

def test_data_loading():
    """Test if data loads correctly"""
    print("\n🧪 Testing data loading...")
    
    try:
        from app.services.data_service import data_service
        
        posts = data_service.get_all_posts()
        print(f"✅ Loaded {len(posts)} posts from JSON")
        
        if len(posts) > 0:
            print(f"✅ Sample post: {posts[0]['title']}")
            return True
        else:
            print("❌ No posts loaded")
            return False
            
    except Exception as e:
        print(f"❌ Data loading failed: {e}")
        return False

def main():
    print("🚀 Quick Test - A-Live-Grid Backend (JSON Version)")
    
    if not test_imports():
        print("\n❌ Import test failed!")
        return False
    
    if not test_data_loading():
        print("\n❌ Data loading test failed!")
        return False
    
    print("\n🎉 All tests passed! Ready to run.")
    print("\n📋 Next step: python run.py")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1) 