#!/usr/bin/env python3
import os
import sys
import json
import logging
import threading
import time
import re
import ssl
import urllib.request
from urllib.error import URLError
from html.parser import HTMLParser

import feedparser
import psycopg2
import pika
from fastapi import FastAPI
import uvicorn

from dotenv import load_dotenv
from web_crawler import ArticleCrawler

# Load environment variables from .env file
load_dotenv()

# Configuration
DB_HOST = os.getenv('DB_HOST', 'postgres')
DB_PORT = os.getenv('DB_PORT', '5432')
DB_NAME = os.getenv('DB_NAME', 'newsdb')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')

# Logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
logger = logging.getLogger('crawler-service')

class HTMLStripper(HTMLParser):
    """Simple HTML stripper to extract text and images"""
    def __init__(self):
        super().__init__()
        self.text = []
        self.images = []
    
    def handle_data(self, data):
        self.text.append(data)
    
    def handle_starttag(self, tag, attrs):
        if tag == 'img':
            attrs_dict = dict(attrs)
            if 'src' in attrs_dict:
                self.images.append(attrs_dict['src'])

def strip_html_and_extract_images(html_text):
    """Strip HTML tags and extract image URLs"""
    if not html_text:
        return '', []
    
    stripper = HTMLStripper()
    try:
        stripper.feed(html_text)
        text = ' '.join(stripper.text).strip()
        # Clean up excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        return text, stripper.images
    except Exception as e:
        logger.warning(f'Error parsing HTML: {e}')
        # Fallback: simple regex-based HTML stripping
        text = re.sub(r'<[^>]+>', '', html_text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text, []

# Metrics
crawl_metrics = {
    "total_crawled": 0,
    "total_new": 0,
    "last_crawl": None
}

app = FastAPI(title="Crawler Service")

@app.get("/health")
def health():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "crawler-service"
    }

@app.get("/metrics")
def metrics():
    """Metrics endpoint"""
    return {
        "total_articles_crawled": crawl_metrics["total_crawled"],
        "total_new_articles": crawl_metrics["total_new"],
        "last_crawl_time": crawl_metrics["last_crawl"]
    }

def _fetch_with_ua(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    ctx = ssl._create_unverified_context()
    with urllib.request.urlopen(req, context=ctx, timeout=15) as resp:
        return resp.read()


def fetch_feed(url, max_items=None):
    """Fetch RSS feed and parse articles"""
    logger.info(f'Fetching feed: {url}')
    
    # Initialize web crawler
    web_crawler = ArticleCrawler()

    # First pass: normal parsing
    parsed = feedparser.parse(url)

    # Retry path: SSL errors or empty entries
    bozo_exc = getattr(parsed, 'bozo_exception', None)
    retry_needed = parsed.bozo or not parsed.entries

    if retry_needed:
        logger.warning(f'Feed bozo/empty, retrying with UA + relaxed SSL; reason={bozo_exc}')
        try:
            content = _fetch_with_ua(url)
            parsed = feedparser.parse(content)
        except URLError as ue:
            logger.error(f'Fallback fetch failed (URLError): {ue}')
        except ssl.SSLError as se:
            logger.error(f'Fallback fetch failed (SSLError): {se}')
        except Exception as retry_exc:
            logger.error(f'Fallback fetch failed: {retry_exc}')

    if parsed.bozo and not parsed.entries:
        logger.warning(f'Feed parse bozo: {getattr(parsed, "bozo_exception", None)}')

    entries = parsed.entries
    if max_items:
        entries = entries[:max_items]
    
    articles = []
    for e in entries:
        title = e.get('title', '').strip()
        link = e.get('link', '').strip()
        published = e.get('published', e.get('updated', ''))
        summary_raw = e.get('summary', e.get('description', ''))
        
        # Strip HTML and extract images from summary
        summary, summary_images = strip_html_and_extract_images(summary_raw)
        
        # Extract image URL from various RSS feed formats
        image_url = None
        
        # Try media:content or media:thumbnail (common in RSS 2.0)
        if hasattr(e, 'media_content') and e.media_content:
            image_url = e.media_content[0].get('url', '')
        elif hasattr(e, 'media_thumbnail') and e.media_thumbnail:
            image_url = e.media_thumbnail[0].get('url', '')
        
        # Try enclosures (podcasts/media files)
        if not image_url and hasattr(e, 'enclosures') and e.enclosures:
            for enclosure in e.enclosures:
                if enclosure.get('type', '').startswith('image/'):
                    image_url = enclosure.get('href', '')
                    break
        
        # Try image tag in entry
        if not image_url and hasattr(e, 'image'):
            if isinstance(e.image, dict):
                image_url = e.image.get('href', '')
            else:
                image_url = str(e.image)
        
        # Try links with image type
        if not image_url and hasattr(e, 'links'):
            for lnk in e.links:
                if lnk.get('type', '').startswith('image/'):
                    image_url = lnk.get('href', '')
                    break
        
        # Try images extracted from summary/description HTML
        if not image_url and summary_images:
            image_url = summary_images[0]
        
        # Crawl full content from website
        full_content = summary  # Default to RSS summary
        if link:
            logger.info(f'Crawling full content from: {link}')
            crawled_data = web_crawler.crawl_article(link)
            if crawled_data and crawled_data.get('success'):
                full_content = crawled_data.get('content', summary)
                logger.info(f'✅ Successfully crawled full content ({len(full_content)} chars)')
                logger.info(f'Content preview: {full_content[:200]}...')
            else:
                logger.warning(f'❌ Failed to crawl full content, using RSS summary')
                logger.warning(f'Crawled data: {crawled_data}')

        # If image_url is still missing, try to extract first image from full content
        if not image_url and full_content:
            _, content_images = strip_html_and_extract_images(full_content)
            if content_images:
                image_url = content_images[0]
        
        articles.append({
            'title': title,
            'link': link,
            'published': published,
            'summary': summary,
            'content': full_content,  # Full HTML content!
            'image_url': image_url
        })
    
    return articles

def publish_crawled_data(article_data):
    """Publish crawled article to crawled_data queue"""
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue='crawled_data', durable=True)
        
        message = json.dumps(article_data)
        channel.basic_publish(
            exchange='',
            routing_key='crawled_data',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)
        )
        connection.close()
        logger.info(f'Published article: {article_data.get("title")}')
        return True
    except Exception as e:
        logger.error(f'Failed to publish to RabbitMQ: {e}')
        return False

def process_crawl_task(ch, method, properties, body):
    """Process crawl task from RabbitMQ"""
    try:
        task = json.loads(body)
        logger.info(f'Processing crawl task for: {task.get("name", "Unknown")}')
        
        url = task.get('url')
        source_id = task.get('source_id')
        
        if not url:
            logger.error('No URL in crawl task')
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return
        
        # Fetch articles from RSS feed
        articles = fetch_feed(url, max_items=50)
        
        new_count = 0
        for article in articles:
            article['source_id'] = source_id
            
            # Publish to crawled_data queue
            if publish_crawled_data(article):
                new_count += 1
                crawl_metrics["total_new"] += 1
            
            crawl_metrics["total_crawled"] += 1
        
        crawl_metrics["last_crawl"] = time.strftime('%Y-%m-%d %H:%M:%S')
        
        logger.info(f'Crawled {len(articles)} articles, {new_count} published')
        ch.basic_ack(delivery_tag=method.delivery_tag)
        
    except Exception as e:
        logger.error(f'Error processing crawl task: {e}')
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)

def start_consumer():
    """Start RabbitMQ consumer for crawl tasks"""
    while True:
        try:
            credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
            connection = pika.BlockingConnection(
                pika.ConnectionParameters(
                    host=RABBITMQ_HOST,
                    port=RABBITMQ_PORT,
                    credentials=credentials,
                    heartbeat=600,
                    blocked_connection_timeout=300
                )
            )
            channel = connection.channel()
            channel.queue_declare(queue='crawl_tasks', durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(
                queue='crawl_tasks',
                on_message_callback=process_crawl_task
            )
            
            logger.info('Started RabbitMQ consumer for crawl tasks...')
            channel.start_consuming()
            
        except Exception as e:
            logger.error(f'RabbitMQ consumer error: {e}')
            time.sleep(5)  # Wait before reconnecting

def start_background_worker():
    """Start background worker thread"""
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()
    logger.info("Background worker started")

@app.on_event("startup")
def startup_event():
    start_background_worker()

if __name__ == '__main__':
    # Start FastAPI server
    uvicorn.run(app, host='0.0.0.0', port=8003)
