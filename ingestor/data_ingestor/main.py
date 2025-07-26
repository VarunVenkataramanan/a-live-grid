import json
import time
import yaml
import google.generativeai as genai
import os
from sources.twitter import fetch_twitter
from sources.reddit import fetch_reddit
from sources.serpapi import fetch_serp
from sources.newsapi import fetch_news

# Load config
def load_config():
    try:
        with open('config.yaml', 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

# Configure Gemini API
config = load_config()
if config and config.get('gemini', {}).get('api_key'):
    GOOGLE_API_KEY = config['gemini']['api_key']
    genai.configure(api_key=GOOGLE_API_KEY)
else:
    print("⚠️ No Gemini API key found in config.yaml")

def extract_civic_signal(text):
    prompt = f"""
Given the following news article or social media post, extract ONLY IF it is related to traffic issues, road problems, or civic infrastructure issues specifically in Bangalore/Bengaluru, India.

Focus ONLY on these Bangalore-specific traffic and civic issues:

BANGALORE TRAFFIC ISSUES: traffic jam, heavy traffic, slow traffic, bumper to bumper, stuck in traffic, choked road, clogged roads, standstill traffic, silk board jam, marathahalli blocked, hebbal choke, bellandur jam

BANGALORE ROAD PROBLEMS: pothole, road work, civic work, construction blockage, road closed, diversion, road digging, utility work, manhole open, repair underway, tree fallen, road condition

BANGALORE WEATHER TRAFFIC: flooded road, waterlogging, rain traffic, monsoon jam, underpass flooded, lake overflow, puddle, slippery road

BANGALORE TRANSPORT ISSUES: bmtc delay, metro packed, bus stuck, no cab, ola surge, uber delay, auto not coming, no public transport, commute nightmare

BANGALORE TRAFFIC ACCIDENTS: accident, car crash, bike skid, hit and run, vehicle flipped, road mishap

BANGALORE EVENTS CAUSING TRAFFIC: vip movement, political rally, procession, wedding traffic, strike rally, bbmp protest, public gathering

BANGALORE TRAFFIC COMPLAINTS: traffic complaint, traffic issue, traffic problem, signal not working, traffic police, traffic light, road repair

IMPORTANT: 
- ONLY extract if the post is specifically about Bangalore/Bengaluru, India
- IGNORE posts about concerts, sports events, or traffic in other cities/countries
- IGNORE posts that don't mention Bangalore/Bengaluru or specific Bangalore locations
- IGNORE general news not related to Bangalore traffic or civic issues

If the post is not related to Bangalore traffic or civic issues, return null for all fields.

Extract:
1. Type of event (e.g., traffic jam, pothole, accident, etc.)
2. Location (specific area in Bangalore or landmark)
3. Severity level (low, moderate, high)
4. Actionable advice (if any)

Text:
{text}

Return your answer as a JSON object with keys: type, location, severity, advice.
If any field is missing or not found, use null.
"""
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        response = model.generate_content(prompt)
        result_text = response.text
        try:
            start_idx = result_text.find('{')
            end_idx = result_text.rfind('}') + 1
            if start_idx != -1 and end_idx != 0:
                json_str = result_text[start_idx:end_idx]
                structured = json.loads(json_str)
            else:
                structured = {"type": None, "location": None, "severity": None, "advice": None}
        except json.JSONDecodeError:
            structured = {"type": None, "location": None, "severity": None, "advice": None}
    except Exception as e:
        print(f"Gemini API error: {str(e)}")
        structured = {"type": None, "location": None, "severity": None, "advice": None}
    return structured

def process_post(post):
    """Process a post through Gemini LLM and print if relevant"""
    # Handle both old 'text' field and new 'text_short'/'text_long' fields
    text = post.get('text_long', post.get('text', ''))
    if not text:
        return

    # Extract civic signals using Gemini
    structured_data = extract_civic_signal(text)

    # Only print if it's a civic event
    if structured_data.get('type'):
        # Combine original post with extracted data
        enriched_post = {
            "original_post": post,
            "extracted_data": structured_data,
            "timestamp": time.time(),
            "processed": True
        }
        print(f"✅ Civic event detected: {structured_data['type']} in {structured_data.get('location', 'Unknown')}")
        print(json.dumps(enriched_post, indent=2)) # Print instead of publish_event
    else:
        print(f"ℹ️ No civic event detected in post")

def main():
    print("🚀 Starting LiveGrid-Om Data Ingestion with Gemini LLM Processing")
    print("=" * 60)
    
    # Fetch data from all sources
    all_data = []
    source_counts = {}
    
    try:
        # print("📱 Fetching from Twitter...")
        # twitter_data = fetch_twitter()[:10] # Enforced limit
        # all_data.extend(twitter_data)
        # source_counts['twitter'] = len(twitter_data)
        # print(f"   Found {len(twitter_data)} Twitter posts (max 10)")

        print("📱 Fetching from Reddit...")
        reddit_data = fetch_reddit()  # No limit, fetch all available
        all_data.extend(reddit_data)
        source_counts['reddit'] = len(reddit_data)
        print(f"   Found {len(reddit_data)} Reddit posts")

        print("📰 Fetching from News API...")
        news_data = fetch_news()  # No limit, fetch all available
        all_data.extend(news_data)
        source_counts['newsapi'] = len(news_data)
        print(f"   Found {len(news_data)} news articles")

        print("🔍 Fetching from SerpAPI...")
        serp_data = fetch_serp()  # No limit, fetch all available
        all_data.extend(serp_data)
        source_counts['serpapi'] = len(serp_data)
        print(f"   Found {len(serp_data)} search results")
        
    except Exception as e:
        print(f"❌ Error fetching data: {e}")
        return
    
    print("\n📊 Source summary:")
    for source, count in source_counts.items():
        print(f"- {source}: {count}")
    print(f"Total sources: {len(source_counts)}")
    print(f"Total posts fetched: {len(all_data)}")
    print("🧠 Processing posts through Gemini LLM...")
    
    # Process each post through Gemini
    civic_events_count = 0
    for i, item in enumerate(all_data, 1):
        print(f"\nProcessing {i}/{len(all_data)}: {item.get('text', '')[:50]}...")
        process_post(item)
        
        # Count civic events
        if item.get('processed'):
            civic_events_count += 1
    
    print(f"\n🎉 Processing complete!")
    print(f"📈 Total posts processed: {len(all_data)}")
    print(f"🏙️ Civic events detected: {civic_events_count}")

if __name__ == "__main__":
    main() 