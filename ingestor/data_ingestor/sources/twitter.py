import yaml
import os
import tweepy
import requests
import time

def get_config():
    with open('config.yaml', 'r') as f:
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

def fetch_twitter():
    print("🐦 Starting Twitter fetch using Twitter API...")
    try:
        config = get_config()
        twitter_cfg = config['twitter']
        bearer_token = twitter_cfg['bearer_token']

        if not bearer_token:
            print('❌ Twitter Bearer Token not set.')
            return []

        print("✅ Twitter credentials found, initializing client...")
        client = tweepy.Client(bearer_token=bearer_token)

        keywords = get_keywords()
        query = ' OR '.join(keywords[:10]) + ' bangalore lang:en -is:retweet'
        print(f"🔍 Using query: {query[:100]}... (truncated)")
        try:
            response = client.search_recent_tweets(query=query, max_results=10, tweet_fields=['created_at', 'author_id', 'text'])
            tweets = response.data if response.data else []
            print(f"📱 Found {len(tweets)} tweets")
        except Exception as e:
            if "429" in str(e):
                print(f"⚠️ Twitter rate limited. Waiting 60 seconds...")
                time.sleep(60)
                query = ' OR '.join(keywords[:5]) + ' bangalore lang:en -is:retweet'
                response = client.search_recent_tweets(query=query, max_results=3, tweet_fields=['created_at', 'author_id', 'text'])
                tweets = response.data if response.data else []
                print(f"📱 Found {len(tweets)} tweets after retry")
            else:
                print(f"❌ Error fetching tweets: {e}")
                return []

        results = []
        for tweet in tweets:
            text = tweet.text
            # Only include tweets that mention 'bangalore' or 'bengaluru'
            if 'bangalore' in text.lower() or 'bengaluru' in text.lower():
                print(f"[DEBUG] Tweet: {text}")
                results.append({
                    'source': 'twitter',
                    'text_short': text[:100],
                    'text_long': text,
                    'user': tweet.author_id,
                    'created_at': str(tweet.created_at) if hasattr(tweet, 'created_at') else None
                })
        print(f"🎉 Twitter fetch complete! Found {len(results)} Bangalore-related tweets")
        return results
    except Exception as e:
        print(f"❌ Error in fetch_twitter: {str(e)}")
        import traceback
        traceback.print_exc()
        return []