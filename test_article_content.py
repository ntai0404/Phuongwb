#!/usr/bin/env python3
"""Test API endpoint"""
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'core-api-service', 'src'))

from models.database import SessionLocal
from models import Article

db = SessionLocal()
article = db.query(Article).order_by(Article.fetched_at.desc()).first()
db.close()

print('='*80)
print('ARTICLE API RESPONSE TEST')
print('='*80)
print(f'\nTitle: {article.title}')
print(f'\nSummary ({len(article.summary or "")} chars):')
print(f'{article.summary}\n')
print(f'Content ({len(article.content or "")} chars):')
print(f'{article.content}\n')

if len(article.content or "") <= len(article.summary or ""):
    print('❌ PROBLEM: Content is same as or shorter than summary!')
    print('   Crawler is NOT extracting full content.')
else:
    print('✅ OK: Content is longer than summary')
