#!/usr/bin/env python3
"""
Comprehensive test to validate the crawler fix
"""
import sys
import os

# Add crawler service to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawler-service', 'src'))

from web_crawler import ArticleCrawler
import requests
from bs4 import BeautifulSoup

def test_url(url):
    """Test crawler with a URL and show detailed diagnostics"""
    print(f"\n{'='*90}")
    print(f"Testing URL: {url}")
    print(f"{'='*90}")
    
    crawler = ArticleCrawler()
    
    try:
        # Fetch the page
        print("\n[1/3] Fetching page...")
        response = requests.get(url, headers=crawler.headers, timeout=15)
        response.encoding = 'utf-8'
        print(f"✓ Status: {response.status_code}, Size: {len(response.content):,} bytes")
        
        # Analyze source page
        print("\n[2/3] Analyzing source page structure...")
        soup = BeautifulSoup(response.content, 'html.parser')
        all_p_tags = soup.find_all('p')
        print(f"✓ Total <p> tags found: {len(all_p_tags)}")
        
        # Count characters in source
        source_text_content = soup.get_text(strip=True)
        print(f"✓ Total text content: {len(source_text_content):,} characters")
        
        # Show sample paragraphs
        if all_p_tags:
            print(f"\n  Sample paragraphs from source:")
            for i, p in enumerate(all_p_tags[:3], 1):
                text = p.get_text(strip=True)[:80]
                print(f"    {i}. {text}...")
        
        # Test crawler
        print("\n[3/3] Running crawler...")
        result = crawler.crawl_article(url)
        
        if result and result.get('success'):
            content = result.get('content', '')
            extracted_p_count = content.count('<p>')
            
            print(f"✓ CRAWLER SUCCESS")
            print(f"  Total extracted: {len(content):,} characters")
            print(f"  Extracted paragraphs: {extracted_p_count}")
            
            # Calculate coverage
            if len(all_p_tags) > 0:
                percentage = (extracted_p_count / len(all_p_tags)) * 100
                print(f"  Coverage: {extracted_p_count}/{len(all_p_tags)} paragraphs ({percentage:.1f}%)")
                
                if percentage < 50:
                    print(f"  ⚠ WARNING: Low coverage detected")
            
            # Show first extracted content
            print(f"\n  First 500 characters of extracted content:")
            print(f"  {content[:500]}")
            
            return True
        else:
            print(f"✗ CRAWLER FAILED")
            return False
            
    except Exception as e:
        print(f"✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    print("CRAWLER DIAGNOSIS & TEST SUITE")
    print("="*90)
    
    # Test URLs
    test_urls = [
        "https://vnexpress.net/",
        "https://thanhnien.vn/",
    ]
    
    if len(sys.argv) > 1:
        test_urls = sys.argv[1:]
    
    # Run tests
    results = []
    for url in test_urls:
        success = test_url(url)
        results.append((url, success))
    
    # Summary
    print(f"\n{'='*90}")
    print("SUMMARY")
    print(f"{'='*90}")
    for url, success in results:
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {url}")
    
    passed = sum(1 for _, s in results if s)
    print(f"\nTotal: {passed}/{len(results)} tests passed")
    print(f"{'='*90}\n")

if __name__ == '__main__':
    main()
