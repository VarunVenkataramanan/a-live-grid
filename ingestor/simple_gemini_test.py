import os
import json
import yaml

def load_config():
    """Load configuration from config.yaml"""
    try:
        with open('config.yaml', 'r') as file:
            config = yaml.safe_load(file)
        return config
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def simple_gemini_test():
    print("🧪 Simple Gemini Test")
    print("=" * 30)
    
    # Load config and set API key
    config = load_config()
    if config and config.get('gemini', {}).get('api_key'):
        os.environ["GOOGLE_API_KEY"] = config['gemini']['api_key']
        print("✅ API key loaded from config.yaml")
    else:
        print("⚠️ No API key found in config.yaml")
        return
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        
        # Simple test with one request
        model = genai.GenerativeModel('gemini-1.0-pro')
        
        test_text = "Heavy traffic jam on Old Airport Road in Bangalore due to ongoing construction work."
        
        prompt = f"""
Extract civic event information from this text. Return as JSON with keys: type, location, severity, advice.

Text: {test_text}
"""
        
        print(f"Testing with: '{test_text}'")
        response = model.generate_content(prompt)
        
        print(f"✅ Gemini Response: {response.text}")
        
        # Try to parse JSON
        try:
            start_idx = response.text.find('{')
            end_idx = response.text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = response.text[start_idx:end_idx]
                result = json.loads(json_str)
                print(f"✅ Parsed JSON: {json.dumps(result, indent=2)}")
            else:
                print("⚠️ No JSON found in response")
        except json.JSONDecodeError as e:
            print(f"⚠️ JSON parsing failed: {e}")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simple_gemini_test() 