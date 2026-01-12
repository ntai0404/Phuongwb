#!/usr/bin/env python3
"""Check database status"""
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'core-api-service', 'src'))

from models.database import SessionLocal
from models import Article, RSSSource

db = SessionLocal()
try:
    article_count = db.query(Article).count()
    source_count = db.query(RSSSource).count()
    
    print('='*60)
    print('DATABASE STATUS')
    print('='*60)
    print(f'✅ Database connected')
    print(f'   Articles: {article_count}')
    print(f'   RSS Sources: {source_count}')
    
    if source_count == 0:
        print('\n❌ No RSS sources! Add some sources first.')
    
    if article_count > 0:
        print(f'\n📰 Latest article:')
        latest = db.query(Article).order_by(Article.fetched_at.desc()).first()
        print(f'   Title: {latest.title[:60]}...')
        print(f'   Content: {len(latest.content or "")} chars')
        print(f'   Summary: {len(latest.summary or "")} chars')
        print(f'   Fetched: {latest.fetched_at}')
    else:
        print('\n❌ No articles! Crawler needs to run.')
        
finally:
    db.close()
