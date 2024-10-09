# parser.py

import feedparser
from newspaper import Article
from datetime import datetime, timezone
from task import insert_article  

links_url = [
    "http://rss.cnn.com/rss/cnn_topstories.rss",
    "http://qz.com/feed",
    "http://feeds.foxnews.com/foxnews/politics",
    "http://feeds.reuters.com/reuters/businessNews",
    "http://feeds.feedburner.com/NewshourWorld",
    "https://feeds.bbci.co.uk/news/world/asia/india/rss.xml"
]


def insert_article_preprocessing(title, content, url, published_date_str):
    
    insert_article.delay(title, content, url, published_date_str)


for links in links_url:
    feed = feedparser.parse(links)
    for entry in feed.entries:
        title = entry.title
        url = entry.link

        
        if hasattr(entry, 'published'):
            published_date = entry.published
        else:
            
            published_date = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

        
        try:
            published_date_obj = datetime.strptime(published_date[:-4], '%a, %d %b %Y %H:%M:%S')
            published_date_obj = published_date_obj.replace(tzinfo=timezone.utc)  
            published_date_str = published_date_obj.strftime('%Y-%m-%d %H:%M:%S')
        except ValueError as e:
            print(f"Error parsing date: {e}")
            continue  
        
        try:
            article = Article(url)
            article.download()
            article.parse()

           
            content = article.text

            
            if content:
                insert_article_preprocessing(title, content, url, published_date_str)
            else:
                print(f"No content found for article: {title}")

        except Exception as e:
            print(f"Error processing article '{title}': {e}")
