import os
import sys
import json
import time

# Add directories to path
sys.path.append('data_ingestor')
sys.path.append('extraction_worker')

def test_full_pipeline():
    print("🧪 Testing Full Pipeline: Google CSE → Pub/Sub → LLM Extraction")
    print("=" * 60)
    
    try:
        # Step 1: Test Google CSE
        print("1️⃣ Testing Google CSE...")
        from sources.google_cse import fetch_and_publish_google_cse_results
        
        # Test with a limited number of queries first
        import requests
        api_key = os.getenv("GOOGLE_CSE_API_KEY")
        search_engine_id = os.getenv("GOOGLE_CSE_ID")
        
        test_query = "Bangalore traffic"
        url = f"https://www.googleapis.com/customsearch/v1?q={test_query}&cx={search_engine_id}&key={api_key}"
        response = requests.get(url)
        
        if response.status_code == 200:
            results = response.json()
            print(f"✅ Google CSE working! Found {len(results.get('items', []))} results")
            
            # Step 2: Test Pub/Sub (if configured)
            print("\n2️⃣ Testing Pub/Sub publishing...")
            try:
                from pubsub_publisher import publish_event
                
                # Test with a sample event
                test_event = {
                    "text": "Heavy traffic on Old Airport Road in Bangalore due to ongoing construction work",
                    "source": "test",
                    "timestamp": time.time()
                }
                
                publish_event(test_event)
                print("✅ Pub/Sub publishing working!")
                
            except Exception as e:
                print(f"⚠️ Pub/Sub not configured or failed: {str(e)}")
                print("   (This is okay for testing without GCP setup)")
            
            # Step 3: Test LLM Extraction
            print("\n3️⃣ Testing LLM Extraction...")
            try:
                from extraction_worker.main import extract_civic_signal, process_event
                
                # Test with sample text
                test_text = "Heavy traffic jam on Old Airport Road in Bangalore. Avoid this route if possible."
                print(f"Testing extraction with: '{test_text}'")
                
                structured = extract_civic_signal(test_text)
                print(f"✅ Extraction result: {json.dumps(structured, indent=2)}")
                
                # Test full event processing
                print("\n4️⃣ Testing full event processing...")
                test_event = {
                    "text": test_text,
                    "source": "test",
                    "timestamp": time.time()
                }
                
                processed_result = process_event(test_event)
                print(f"✅ Full processing result: {json.dumps(processed_result, indent=2)}")
                
            except Exception as e:
                print(f"❌ LLM extraction failed: {str(e)}")
                import traceback
                traceback.print_exc()
            
            # Step 4: Test with real Google CSE resultsaa
            print("\n5️⃣ Testing with real Google CSE results...")
            if results.get('items'):
                first_result = results['items'][0]
                test_text = f"{first_result.get('title', '')} {first_result.get('snippet', '')}"
                print(f"Testing with real result: '{test_text[:100]}...'")
                
                try:
                    structured = extract_civic_signal(test_text)
                    print(f"✅ Real data extraction: {json.dumps(structured, indent=2)}")
                    
                    # Test full processing with real data
                    real_event = {
                        "text": test_text,
                        "source": "google_cse",
                        "link": first_result.get('link', ''),
                        "timestamp": time.time()
                    }
                    
                    processed_real = process_event(real_event)
                    print(f"✅ Real data full processing: {json.dumps(processed_real, indent=2)}")
                    
                except Exception as e:
                    print(f"❌ Real data extraction failed: {str(e)}")
            
        else:
            print(f"❌ Google CSE failed: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Pipeline test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_full_pipeline() 
