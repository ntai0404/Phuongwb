from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import json
import pika
import os

from ..models import get_db, RSSSource, CrawlerConfig
from ..auth.security import get_current_admin
from ..models.models import User
from .schemas import CrawlerTriggerRequest, CrawlerScheduleUpdate, CrawlerConfigResponse

router = APIRouter(prefix="/api/v1/crawler", tags=["Crawler Orchestrator"])

# RabbitMQ configuration
RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_PORT = int(os.getenv('RABBITMQ_PORT', '5672'))
RABBITMQ_USER = os.getenv('RABBITMQ_USER', 'guest')
RABBITMQ_PASSWORD = os.getenv('RABBITMQ_PASSWORD', 'guest')

def publish_crawl_task(task_data: dict):
    """Publish crawl task to RabbitMQ"""
    try:
        credentials = pika.PlainCredentials(RABBITMQ_USER, RABBITMQ_PASSWORD)
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT, credentials=credentials)
        )
        channel = connection.channel()
        channel.queue_declare(queue='crawl_tasks', durable=True)
        
        message = json.dumps(task_data)
        channel.basic_publish(
            exchange='',
            routing_key='crawl_tasks',
            body=message,
            properties=pika.BasicProperties(delivery_mode=2)  # make message persistent
        )
        connection.close()
        return True
    except Exception as e:
        print(f"Failed to publish to RabbitMQ: {e}")
        return False

@router.post("/trigger")
def trigger_crawl(
    request: CrawlerTriggerRequest,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Trigger immediate crawl (Admin only)"""
    if request.source_id:
        # Crawl specific source
        source = db.query(RSSSource).filter(
            RSSSource.id == request.source_id,
            RSSSource.is_active == True
        ).first()
        
        if not source:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="RSS source not found or inactive"
            )
        
        task_data = {
            "source_id": source.id,
            "url": source.url,
            "name": source.name
        }
        
        success = publish_crawl_task(task_data)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to queue crawl task"
            )
        
        return {"message": f"Crawl task queued for source: {source.name}"}
    else:
        # Crawl all active sources
        sources = db.query(RSSSource).filter(RSSSource.is_active == True).all()
        
        if not sources:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No active RSS sources found"
            )
        
        queued_count = 0
        for source in sources:
            task_data = {
                "source_id": source.id,
                "url": source.url,
                "name": source.name
            }
            if publish_crawl_task(task_data):
                queued_count += 1
        
        return {
            "message": f"Queued {queued_count} crawl tasks",
            "total_sources": len(sources)
        }

@router.put("/schedule", response_model=CrawlerConfigResponse)
def update_schedule(
    schedule_data: CrawlerScheduleUpdate,
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Configure crawler schedule (Admin only)"""
    # Get or create crawler config
    config = db.query(CrawlerConfig).first()
    
    if not config:
        config = CrawlerConfig(
            cron_schedule=schedule_data.cron_schedule,
            is_enabled=schedule_data.is_enabled
        )
        db.add(config)
    else:
        config.cron_schedule = schedule_data.cron_schedule
        config.is_enabled = schedule_data.is_enabled
    
    db.commit()
    db.refresh(config)
    
    return config

@router.get("/schedule", response_model=CrawlerConfigResponse)
def get_schedule(
    current_user: User = Depends(get_current_admin),
    db: Session = Depends(get_db)
):
    """Get crawler schedule configuration (Admin only)"""
    config = db.query(CrawlerConfig).first()
    
    if not config:
        # Create default config
        config = CrawlerConfig()
        db.add(config)
        db.commit()
        db.refresh(config)
    
    return config
