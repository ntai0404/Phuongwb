#!/usr/bin/env python3
"""
Test script to validate the crawler fix
Tests with multiple Vietnamese news sources
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawler-service', 'src'))

from web_crawler import ArticleCrawler
import requests
from bs4 import BeautifulSoup

def test_specific_url(url):
    """Test crawler with a specific URL"""
    print(f"\n{'='*80}")
    print(f"Testing: {url}")
    print(f"{'='*80}\n")
    
    crawler = ArticleCrawler()
    
    try:
        response = requests.get(url, headers=crawler.headers, timeout=15)
        response.encoding = 'utf-8'
        
        print(f"✓ Page fetched (Status: {response.status_code}, Size: {len(response.content)} bytes)")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Count paragraphs on source page
        all_p_tags = soup.find_all('p')
        print(f"✓ Total <p> tags on source page: {len(all_p_tags)}")
        if all_p_tags:
            print(f"  Sample paragraphs from source:")
            for i, p in enumerate(all_p_tags[:3]):
                text = p.get_text(strip=True)[:100]
                print(f"    {i+1}. {text}...")
        
        # Test the crawler
        result = crawler.crawl_article(url)
        
        if result and result.get('success'):
            content = result.get('content', '')
            print(f"\n✓ Crawler extracted: {len(content)} characters")
            
            # Count how many paragraphs were extracted
            extracted_p_count = content.count('<p>')
            print(f"✓ Extracted {extracted_p_count} paragraphs")
            
            # Show first 1000 chars
            print(f"\nFirst 1000 characters of extracted content:")
            print(f"{content[:1000]}")
            
            # Calculate percentage of paragraphs extracted
            if len(all_p_tags) > 0:
                percentage = (extracted_p_count / len(all_p_tags)) * 100
                print(f"\n✓ Coverage: {extracted_p_count}/{len(all_p_tags)} paragraphs ({percentage:.1f}%)")
            
            return True
        else:
            print(f"\n✗ Crawler failed")
            return False
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    # Test with some Vietnamese news sites
    test_urls = [
        "https://vnexpress.net/",
        "https://thanhnien.vn/",
    ]
    
    if len(sys.argv) > 1:
        # Use custom URLs from command line
        test_urls = sys.argv[1:]
    
    success_count = 0
    for url in test_urls:
        if test_specific_url(url):
            success_count += 1
    
    print(f"\n{'='*80}")
    print(f"Results: {success_count}/{len(test_urls)} tests passed")
    print(f"{'='*80}\n")

if __name__ == '__main__':
    main()
