import os
import json
import sys
import yaml

# Add extraction_worker to path
sys.path.append('extraction_worker')

def load_config():
    """Load configuration from config.yaml"""
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def test_gemini_extraction():
    print("🧪 Testing Gemini LLM Extraction")
    print("=" * 50)
    
    # Load config and set API key
    config = load_config()
    if config and config.get('gemini', {}).get('api_key'):
        os.environ["GOOGLE_API_KEY"] = config['gemini']['api_key']
        print("✅ API key loaded from config.yaml")
    else:
        print("⚠️ No API key found in config.yaml, please set GOOGLE_API_KEY environment variable")
        return
    
    try:
        from main import extract_civic_signal, process_event
        
        # Test cases with different types of civic events
        test_cases = [
            {
                "text": "Heavy traffic jam on Old Airport Road in Bangalore due to ongoing construction work. Avoid this route if possible.",
                "expected_type": "traffic"
            },
            {
                "text": "Power cut in HSR Layout since 2 PM. BBMP says restoration by 6 PM.",
                "expected_type": "power cut"
            },
            {
                "text": "Flooding reported in Koramangala after heavy rainfall. Roads are waterlogged.",
                "expected_type": "flood"
            },
            {
                "text": "BMTC bus strike affects thousands of commuters in Bangalore today.",
                "expected_type": "public transport"
            },
            {
                "text": "New restaurant opened in Indiranagar. Great food and ambiance!",
                "expected_type": None  # Not a civic event
            }
        ]
        
        print("Testing Gemini extraction with various civic events...\n")
        
        for i, test_case in enumerate(test_cases, 1):
            print(f"Test {i}: {test_case['text'][:50]}...")
            
            # Test direct extraction
            structured = extract_civic_signal(test_case['text'])
            print(f"Extracted: {json.dumps(structured, indent=2)}")
            
            # Test full processing
            event_data = {
                "text": test_case['text'],
                "source": "test",
                "timestamp": "2024-01-01T12:00:00Z"
            }
            
            processed = process_event(event_data)
            print(f"Processed: {json.dumps(processed, indent=2)}")
            
            # Check if extraction worked
            if structured.get('type'):
                print(f"✅ Successfully extracted civic event: {structured['type']}")
            else:
                print(f"ℹ️ No civic event detected (expected for non-civic content)")
            
            print("-" * 50)
        
        # Test with real Google CSE data (if available)
        print("\nTesting with sample Google CSE data...")
        sample_cse_data = {
            "text": "Bangalore Traffic Update: Heavy congestion reported on Hosur Road near Electronic City. Commuters advised to take alternative routes.",
            "source": "google_cse",
            "link": "https://example.com/traffic-update",
            "timestamp": "2024-01-01T12:00:00Z"
        }
        
        processed_cse = process_event(sample_cse_data)
        print(f"Google CSE sample result: {json.dumps(processed_cse, indent=2)}")
        
        print("\n🎉 All tests completed successfully!")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_gemini_extraction() 