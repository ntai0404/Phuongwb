#!/usr/bin/env python3
"""
Test script to verify web crawler output
"""
import sys
sys.path.insert(0, 'crawler-service/src')

from web_crawler import ArticleCrawler

# Test URL - VNExpress article
test_urls = [
    'https://vnexpress.net/tien-luong-huu-tro-te-khong-day-du-cho-cu-gia-4677236.html',
]

crawler = ArticleCrawler()

for url in test_urls:
    print(f"\n{'='*80}")
    print(f"Testing: {url}")
    print(f"{'='*80}\n")
    
    result = crawler.crawl_article(url)
    
    if result and result.get('success'):
        content = result.get('content', '')
        print("CRAWLED CONTENT:")
        print("-" * 80)
        
        # Print first 3000 chars
        lines = content.split('\n')
        for i, line in enumerate(lines[:50]):
            if line.strip():
                print(f"{i+1:3}. {line[:100]}")
        
        print("\n" + "-" * 80)
        print(f"Total lines: {len(lines)}")
        print(f"Total chars: {len(content)}")
        
        # Check for JavaScript patterns
        js_indicators = ['(function', 'window.', 'var ', 'function(', 'document.', 'arfasync', 'taboola', 'GMT']
        found_js = []
        for line in lines:
            for indicator in js_indicators:
                if indicator.lower() in line.lower():
                    found_js.append((indicator, line[:80]))
                    break
        
        if found_js:
            print("\n⚠️  JAVASCRIPT PATTERNS FOUND:")
            for indicator, line in found_js[:5]:
                print(f"   - '{indicator}' in: {line}")
        else:
            print("\n✅ NO JAVASCRIPT PATTERNS FOUND")
            
        # Check for timestamps
        import re
        timestamps = re.findall(r'\d{4}-\d{2}-\d{2}.*?GMT', content)
        if timestamps:
            print(f"\n⚠️  TIMESTAMPS FOUND ({len(timestamps)}):")
            for ts in timestamps[:3]:
                print(f"   - {ts}")
        else:
            print("\n✅ NO TIMESTAMPS FOUND")
    else:
        print("❌ CRAWL FAILED")
