#!/usr/bin/env python3
"""Test web crawler with real VNExpress article"""

import sys
sys.path.insert(0, '/app/src')

from web_crawler import ArticleCrawler

crawler = ArticleCrawler()

# Test with real VNExpress URL
url = "https://vnexpress.net/dau-tran-vong-play-off-aff-cup-4677152.html"

print("=" * 80)
print(f"CRAWLING: {url}")
print("=" * 80)

result = crawler.crawl_vnexpress(url)

if result and result.get('success'):
    content = result.get('content', '')
    lines = content.split('\n')
    
    print(f"\n✓ Crawl successful!")
    print(f"Total lines: {len(lines)}")
    print(f"Total characters: {len(content)}")
    
    print("\n" + "=" * 80)
    print("FIRST 30 LINES OF CONTENT:")
    print("=" * 80)
    
    for i, line in enumerate(lines[:30], 1):
        # Show first 100 chars of each line
        display = line[:100] if len(line) > 100 else line
        print(f"{i:2d}. {display}")
    
    print("\n" + "=" * 80)
    print("CHECKING FOR BAD PATTERNS:")
    print("=" * 80)
    
    bad_patterns = [
        'window.runinit',
        'pageSettings',
        'taboola',
        'outbrain',
        'arfasync',
        'window.pageSettings',
        'htmlToElement',
        'childnodes',
        '_taboola',
        'mutexads',
    ]
    
    found_bad = False
    for pattern in bad_patterns:
        if pattern.lower() in content.lower():
            print(f"✗ FOUND BAD PATTERN: {pattern}")
            found_bad = True
    
    if not found_bad:
        print("✓ NO BAD PATTERNS FOUND! Clean content!")
    
    print("\n" + "=" * 80)
    print(f"SUCCESS - Content is clean and has {len(lines)} lines")
    print("=" * 80)
else:
    print("\n✗ Crawl failed!")
    if result:
        print(f"Error: {result.get('error', 'Unknown error')}")
    sys.exit(1)
