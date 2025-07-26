import requests
import json
import yaml
import os

def get_config():
    with open(os.path.join(os.path.dirname(__file__), '../../config.yaml'), 'r') as f:
        return yaml.safe_load(f)

def get_keywords():
    # General traffic/civic keywords (broad)
    keywords = [
        'traffic jam', 'heavy traffic', 'slow traffic', 'bumper to bumper', 'stuck in traffic',
        'pothole', 'road work', 'road closed', 'diversion', 'road digging', 'repair underway',
        'tree fallen', 'flooded road', 'waterlogging', 'rain traffic', 'monsoon jam',
        'underpass flooded', 'lake overflow', 'slippery road', 'accident', 'car crash',
        'bike skid', 'hit and run', 'road mishap', 'bmtc delay', 'metro packed', 'bus stuck',
        'no cab', 'ola surge', 'uber delay', 'auto not coming', 'no public transport',
        'commute nightmare', 'signal not working', 'power cut', 'no electricity', 'load shedding',
        'garbage', 'sewage', 'water supply', 'protest', 'rally', 'strike', 'public gathering',
        'civic issue', 'municipal', 'bbmp', 'bescom', 'bwssb', 'ward', 'corporator', 'mayor',
        'commissioner', 'bengaluru', 'bangalore'
    ]
    return keywords

def fetch_serp():
    print("🔍 Starting SerpAPI fetch...")
    try:
        config = get_config()
        api_key = config['serpapi']['api_key']
        if not api_key:
            print('❌ SerpAPI key not set.')
            return []
        keywords = get_keywords()
        query = ' OR '.join(keywords[:10]) # Limit to first 10 keywords for query length
        print(f"🔍 Using query: {query[:100]}... (truncated)")
        all_results = []
        page = 1
        while True:
            params = {
                'engine': 'google_news',
                'q': query,
                'api_key': api_key,
                'hl': 'en',
                'num': 100,  # SerpAPI max per page
                'start': (page - 1) * 100
            }
            response = requests.get('https://serpapi.com/search', params=params)
            if response.status_code != 200:
                print('❌ SerpAPI request failed:', response.text)
                break
            data = response.json()
            results = []
            for article in data.get('news_results', []):
                full_text = article.get('title', '') + '\n' + article.get('snippet', '')
                # Filter for Bangalore/Bengaluru
                if 'bangalore' in full_text.lower() or 'bengaluru' in full_text.lower():
                    results.append({
                        'source': 'serpapi',
                        'text_short': full_text[:100],
                        'text_long': full_text,
                        'url': article.get('link', ''),
                        'published': article.get('date', '')
                    })
            all_results.extend(results)
            if not data.get('news_results') or len(data.get('news_results', [])) < 100:
                break  # No more pages
            page += 1
        print(f"🎉 SerpAPI fetch complete! Found {len(all_results)} relevant articles for Bangalore/Bengaluru")
        return all_results
    except Exception as e:
        print(f"❌ Error in fetch_serp: {str(e)}")
        import traceback
        traceback.print_exc()
        return [] 