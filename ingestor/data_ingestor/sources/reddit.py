import praw
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

def fetch_reddit():
    print("🔍 Starting Reddit fetch...")
    try:
        config = get_config()
        reddit_cfg = config['reddit']

        client_id = reddit_cfg.get('client_id')
        client_secret = reddit_cfg.get('client_secret')
        user_agent = reddit_cfg.get('user_agent', 'civic-signal-ingestor')

        if not all([client_id, client_secret, user_agent]):
            print('❌ Reddit API credentials not found in config.yaml')
            return []

        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )

        subreddits = ['bangalore', 'india']
        keywords = get_keywords()
        print(f"🔍 Searching subreddits: {subreddits}")
        print(f"🔍 Using comprehensive civic keywords: {len(keywords)} total keywords")
        print(f"🔍 Sample keywords: {keywords[:10]}... (showing first 10)")

        results = []
        for sub in subreddits:
            subreddit = reddit.subreddit(sub)
            # Fetch as many as allowed (Reddit API default is 1000 for .new, but let's use 100 for safety)
            submissions = list(subreddit.new(limit=100))

            for submission in submissions:
                full_text = submission.title + '\n' + (submission.selftext or '')
                # Filter for Bangalore/Bengaluru AND any keyword
                if ('bangalore' in full_text.lower() or 'bengaluru' in full_text.lower()) and any(kw.lower() in full_text.lower() for kw in keywords):
                    results.append({
                        'source': 'reddit',
                        'text_short': full_text[:100],
                        'text_long': full_text,
                        'url': submission.url,
                        'created_utc': submission.created_utc,
                        'subreddit': sub
                    })
        print(f"🎉 Reddit fetch complete! Found {len(results)} relevant posts for Bangalore/Bengaluru")
        return results

    except Exception as e:
        print(f"❌ Error in fetch_reddit: {str(e)}")
        import traceback
        traceback.print_exc()
        return [] 