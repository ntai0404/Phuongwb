import pika
import json
import os
import threading
import httpx
from sqlalchemy.orm import Session

from .models import SessionLocal, Article, RSSSource
from .classifier import classify_article

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')
RECOMMENDATION_URL = os.getenv('RECOMMENDATION_URL', 'http://recommendation-service:8001')

def save_article_to_db(article_data: dict, db: Session):
    """Save or update article in database"""
    try:
        # Check if article already exists
        existing = db.query(Article).filter(Article.link == article_data.get('link')).first()
        
        # Auto-classify article
        category = classify_article(
            title=article_data.get('title', ''),
            summary=article_data.get('summary'),
            content=article_data.get('content')
        )
        
        if existing:
            # Update existing article
            existing.title = article_data.get('title')
            # IMPORTANT: Only update content if new content is provided and not empty
            new_content = article_data.get('content')
            if new_content and len(str(new_content).strip()) > 0:
                existing.content = new_content
            # If new_content is empty/None, keep existing content (don't overwrite with summary)
            existing.published = article_data.get('published')
            existing.summary = article_data.get('summary')
            existing.image_url = article_data.get('image_url')
            existing.category = category
            if article_data.get('source_id'):
                existing.source_id = article_data.get('source_id')
            
            db.commit()
            db.refresh(existing)
            
            print(f"Updated article: {existing.title} (Category: {category})")
            return existing
        
        # Create new article
        new_content = article_data.get('content')
        # If no detailed content, fall back to summary
        if not new_content or len(str(new_content).strip()) == 0:
            new_content = article_data.get('summary')
        
        new_article = Article(
            title=article_data.get('title'),
            link=article_data.get('link'),
            content=new_content,
            published=article_data.get('published'),
            summary=article_data.get('summary'),
            image_url=article_data.get('image_url'),
            category=category,
            source_id=article_data.get('source_id')
        )
        
        db.add(new_article)
        db.commit()
        db.refresh(new_article)
        
        print(f"Saved new article: {new_article.title} (Category: {category})")
        return new_article
    except Exception as e:
        db.rollback()
        print(f"Error saving article: {e}")
        return None

def index_article_in_recommendation_service(article):
    """Send article to recommendation service for vector indexing"""
    try:
        data = {
            "id": article.id,
            "title": article.title,
            "content": article.content or article.summary or article.title
        }
        
        response = httpx.post(
            f"{RECOMMENDATION_URL}/api/v1/vectors/upsert",
            json=data,
            timeout=10.0
        )
        
        if response.status_code == 200:
            print(f"Indexed article in recommendation service: {article.title}")
        else:
            print(f"Failed to index article: {response.status_code}")
    except Exception as e:
        print(f"Error indexing article in recommendation service: {e}")

def process_crawled_article(ch, method, properties, body):
    """Process crawled articles from RabbitMQ"""
    db = SessionLocal()
    try:
        article_data = json.loads(body)
        print(f"Processing crawled article: {article_data.get('title', 'Unknown')}")
        
        # Save to database
        article = save_article_to_db(article_data, db)
        
        # If saved successfully, index in recommendation service
        if article:
            index_article_in_recommendation_service(article)
        
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing crawled article: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)
    finally:
        db.close()

def start_consumer():
    """Start RabbitMQ consumer for crawled data"""
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
        channel.queue_declare(queue='crawled_data', durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(
            queue='crawled_data',
            on_message_callback=process_crawled_article
        )
        
        print("Started RabbitMQ consumer for crawled articles...")
        channel.start_consuming()
    except Exception as e:
        print(f"RabbitMQ consumer error: {e}")
        # Retry connection after delay
        import time
        time.sleep(5)
        start_consumer()

def start_background_worker():
    """Start background worker thread"""
    consumer_thread = threading.Thread(target=start_consumer, daemon=True)
    consumer_thread.start()
    print("Background worker started")
