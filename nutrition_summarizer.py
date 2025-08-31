import feedparser
import yaml
import os
from datetime import datetime, timedelta

def load_config():
    with open("config.yaml", "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def fetch_articles(feed_url, lookback_hours):
    feed = feedparser.parse(feed_url)
    cutoff = datetime.utcnow() - timedelta(hours=lookback_hours)
    links = []
    for entry in feed.entries[:5]:
        published = None
        if hasattr(entry, "published_parsed"):
            published = datetime(*entry.published_parsed[:6])
        if published and published < cutoff:
            continue
        links.append(entry.link)
    return links

def main():
    config = load_config()
    os.makedirs("output", exist_ok=True)
    fname = f"output/rassegna_{datetime.now().strftime('%Y%m%d_%H%M')}.txt"
    all_links = []

    for cat in config["categories"]:
        for feed in cat["feeds"]:
            try:
                articles = fetch_articles(feed, config.get("lookback_hours", 72))
                all_links.extend(articles[:config.get("max_per_category", 2)])
            except Exception as e:
                print(f"Errore con {feed}: {e}")

    with open(fname, "w", encoding="utf-8") as f:
        for link in all_links:
            f.write(f"{link}\n")

    print("File salvato:", fname)

if __name__ == "__main__":
    main()
