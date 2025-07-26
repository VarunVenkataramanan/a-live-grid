from newsapi import NewsApiClient
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

def fetch_news():
    print("📰 Starting NewsAPI fetch...")
    try:
        config = get_config()
        api_key = config['newsapi']['api_key']
        if not api_key:
            print('❌ NewsAPI key not set.')
            return []
        newsapi = NewsApiClient(api_key=api_key)
        keywords = get_keywords()
        query = ' OR '.join(keywords[:10]) # Limit to first 10 keywords for query length
        print(f"🔍 Using query: {query[:100]}... (truncated)")
        all_articles = []
        page = 1
        page_size = 100  # NewsAPI max page size
        while True:
            articles = newsapi.get_everything(q=query, language='en', page_size=page_size, page=page)
            results = []
            for article in articles.get('articles', []):
                full_text = article['title'] + '\n' + article.get('description', '')
                # Filter for Bangalore/Bengaluru
                if 'bangalore' in full_text.lower() or 'bengaluru' in full_text.lower():
                    results.append({
                        'source': 'newsapi',
                        'text_short': full_text[:100],
                        'text_long': full_text,
                        'url': article['url'],
                        'published_at': article['publishedAt']
                    })
            all_articles.extend(results)
            if len(articles.get('articles', [])) < page_size:
                break  # No more pages
            page += 1
        print(f"🎉 NewsAPI fetch complete! Found {len(all_articles)} relevant articles for Bangalore/Bengaluru")
        return all_articles
    except Exception as e:
        print(f"❌ Error in fetch_news: {str(e)}")
        import traceback
        traceback.print_exc()
        return [] 