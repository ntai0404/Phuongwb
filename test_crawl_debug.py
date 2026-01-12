#!/usr/bin/env python3
"""Test crawler with a specific article to debug content extraction"""

import sys
from pathlib import Path

# Support both container path (/app/src) and local repo path
repo_root = Path(__file__).resolve().parent
local_src = repo_root / 'crawler-service' / 'src'
sys.path.insert(0, '/app/src')
sys.path.insert(0, str(local_src))

from web_crawler import ArticleCrawler

# Test with a VNExpress health article
test_url = "https://vnexpress.net/loi-ich-khi-uong-mot-coc-nuoc-sau-thuc-day-4846164.html"

print("=" * 80)
print(f"Testing crawler with: {test_url}")
print("=" * 80)

crawler = ArticleCrawler()
result = crawler.crawl_article(test_url)

if result and result.get('success'):
    content = result.get('content', '')
    print(f"\nContent length: {len(content)} characters")
    print(f"\nFirst 500 characters of content:")
    print("-" * 80)
    print(content[:500])
    print("-" * 80)
    print(f"\nLast 500 characters of content:")
    print("-" * 80)
    print(content[-500:])
    print("-" * 80)
    
    # Count elements
    p_count = content.count('<p>')
    img_count = content.count('<img')
    video_count = content.count('<video')
    iframe_count = content.count('<iframe')
    
    print(f"\nContent analysis:")
    print(f"- Paragraphs: {p_count}")
    print(f"- Images: {img_count}")
    print(f"- Videos: {video_count}")
    print(f"- Iframes: {iframe_count}")
    
    if p_count < 5:
        print("\n⚠️ WARNING: Very few paragraphs detected! Content may be incomplete.")
    else:
        print(f"\n✓ Content looks good with {p_count} paragraphs")
else:
    print("\n✗ FAILED to crawl article")
    print(f"Result: {result}")
