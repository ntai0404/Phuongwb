#!/usr/bin/env python3
"""Check recent article content in database"""

import sys
import psycopg2
from datetime import datetime

# Database connection
conn = psycopg2.connect(
    host="localhost",
    port=5432,
    database="newsdb",
    user="postgres",
    password="postgres"
)

cursor = conn.cursor()

# Get most recent article with full content
cursor.execute("""
    SELECT id, title, LEFT(content, 500) as content_preview, 
           LENGTH(content) as content_length, source, created_at
    FROM articles 
    WHERE content IS NOT NULL AND content != ''
    ORDER BY created_at DESC 
    LIMIT 5
""")

print("=" * 100)
print("RECENT ARTICLES IN DATABASE")
print("=" * 100)

for row in cursor.fetchall():
    article_id, title, preview, length, source, created_at = row
    print(f"\nID: {article_id}")
    print(f"Title: {title}")
    print(f"Source: {source}")
    print(f"Content length: {length} chars")
    print(f"Created: {created_at}")
    print(f"Preview:\n{preview}...")
    print("-" * 100)

# Get one full article to analyze
cursor.execute("""
    SELECT id, title, content
    FROM articles 
    WHERE content IS NOT NULL AND content != ''
    ORDER BY created_at DESC 
    LIMIT 1
""")

row = cursor.fetchone()
if row:
    article_id, title, content = row
    print("\n" + "=" * 100)
    print(f"FULL CONTENT ANALYSIS FOR: {title}")
    print("=" * 100)
    
    # Count HTML elements
    p_count = content.count('<p>')
    img_count = content.count('<img')
    video_count = content.count('<video')
    iframe_count = content.count('<iframe')
    
    print(f"\nHTML Elements:")
    print(f"- Paragraphs (<p>): {p_count}")
    print(f"- Images (<img>): {img_count}")
    print(f"- Videos (<video>): {video_count}")
    print(f"- Iframes: {iframe_count}")
    
    print(f"\nFirst 1000 characters:")
    print(content[:1000])
    
    if p_count < 5:
        print("\n⚠️ WARNING: Very few paragraphs! Content seems incomplete.")
    else:
        print(f"\n✓ Content has {p_count} paragraphs - looks good")

cursor.close()
conn.close()
