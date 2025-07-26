import os
import sys
import json

# Add the data_ingestor directory to the path
sys.path.append('data_ingestor')

from sources.google_cse import fetch_and_publish_google_cse_results

def test_google_cse():
    print("Testing Google Custom Search Engine integration...")
    
    # Set environment variables if not already set
    if not os.getenv("GOOGLE_CSE_API_KEY"):
        os.environ["GOOGLE_CSE_API_KEY"] = "AIzaSyBhCExO4gJFw4GqYouESHUa6wEd5Xyiqtk"
    
    if not os.getenv("GOOGLE_CSE_ID"):
        os.environ["GOOGLE_CSE_ID"] = "f31747c301120487a"
    
    try:
        # Test with a single query first
        import requests
        
        api_key = os.getenv("GOOGLE_CSE_API_KEY")
        search_engine_id = os.getenv("GOOGLE_CSE_ID")
        
        # Test a simple query
        test_query = "Bangalore traffic"
        url = f"https://www.googleapis.com/customsearch/v1?q={test_query}&cx={search_engine_id}&key={api_key}"
        
        print(f"Testing API call to: {url}")
        response = requests.get(url)
        
        if response.status_code == 200:
            results = response.json()
            print("✅ API call successful!")
            print(f"Found {len(results.get('items', []))} results")
            
            # Show first result
            if results.get('items'):
                first_result = results['items'][0]
                print(f"\nFirst result:")
                print(f"Title: {first_result.get('title', 'N/A')}")
                print(f"Link: {first_result.get('link', 'N/A')}")
                print(f"Snippet: {first_result.get('snippet', 'N/A')[:100]}...")
            
            # Now test the full function
            print("\nTesting full fetch_and_publish_google_cse_results function...")
            fetch_and_publish_google_cse_results()
            print("✅ Full function executed successfully!")
            
        else:
            print(f"❌ API call failed with status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error occurred: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_google_cse() 