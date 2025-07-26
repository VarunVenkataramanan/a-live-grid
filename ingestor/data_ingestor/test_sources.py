from sources.twitter import fetch_twitter
from sources.newsapi import fetch_news
from sources.reddit import fetch_reddit
from sources.serpapi import fetch_serp

def test_twitter():
    print("Testing Twitter...")
    results = fetch_twitter()
    print(f"Fetched {len(results)} results from Twitter.")
    for r in results[:3]:
        print(r)
    print("-" * 40)

def test_newsapi():
    print("Testing NewsAPI...")
    results = fetch_news()
    print(f"Fetched {len(results)} results from NewsAPI.")
    for r in results[:3]:
        print(r)
    print("-" * 40)

def test_reddit():
    print("Testing Reddit...")
    results = fetch_reddit()
    print(f"Fetched {len(results)} results from Reddit.")
    for r in results[:3]:
        print(r)
    print("-" * 40)

def test_serpapi():
    print("Testing SerpAPI...")
    results = fetch_serp()
    print(f"Fetched {len(results)} results from SerpAPI.")
    for r in results[:3]:
        print(r)
    print("-" * 40)

if __name__ == "__main__":
    test_twitter()
    test_newsapi()
    test_reddit()
    test_serpapi() 