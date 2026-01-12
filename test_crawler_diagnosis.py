#!/usr/bin/env python3
"""
Diagnostic script to test crawler content extraction
Tests the web crawler with multiple news sources to identify content extraction issues
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawler-service', 'src'))

from web_crawler import ArticleCrawler
import json
from bs4 import BeautifulSoup
import requests

# Test URLs - various news sources
TEST_URLS = [
    # Add your problematic URL here - the one about HLV Thawatchai U.23
    # For now, using generic examples
    "https://vnexpress.net/",  # Generic - we'll fetch a real article from here
]

def test_crawler_with_url(url):
    """Test crawler with a specific URL and show diagnostic info"""
    print(f"\n{'='*80}")
    print(f"Testing URL: {url}")
    print(f"{'='*80}\n")
    
    crawler = ArticleCrawler()
    
    try:
        # Fetch the page
        response = requests.get(url, headers=crawler.headers, timeout=10)
        response.encoding = 'utf-8'
        
        print(f"✓ Successfully fetched page (Status: {response.status_code})")
        print(f"  Page size: {len(response.content)} bytes")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Run the crawl_article function
        result = crawler.crawl_article(url)
        
        if result and result.get('success'):
            content = result.get('content', '')
            print(f"\n✓ Crawler SUCCESS")
            print(f"  Content extracted: {len(content)} characters")
            print(f"  First 500 chars of content:\n{content[:500]}")
            print(f"\n  Full content HTML:\n{content}")
            return result
        else:
            print(f"\n✗ Crawler FAILED")
            # Debug: check what article body was found
            article = soup.find('article')
            if not article:
                article = soup.find('div', class_='ArticleContent')
            if not article:
                article = soup.find('div', class_='content_detail')
            if not article:
                article = soup.find('main')
            
            if article:
                text_content = article.get_text(strip=True)
                print(f"  Found article element with {len(text_content)} chars of text")
                print(f"  First 500 chars: {text_content[:500]}")
            else:
                print(f"  Could not find article element")
            return None
            
    except Exception as e:
        print(f"✗ Error: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_page_structure(url):
    """Analyze the HTML structure of the page"""
    print(f"\n{'='*80}")
    print(f"Analyzing page structure: {url}")
    print(f"{'='*80}\n")
    
    try:
        response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'}, timeout=10)
        response.encoding = 'utf-8'
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for common article containers
        containers = {
            'article': soup.find_all('article'),
            'div.ArticleContent': soup.find_all('div', class_='ArticleContent'),
            'div.content_detail': soup.find_all('div', class_='content_detail'),
            'div.fck_detail': soup.find_all('div', class_='fck_detail'),
            'main': soup.find_all('main'),
            'div[role=main]': soup.find_all('div', attrs={'role': 'main'}),
        }
        
        print("Found containers:")
        for container_type, elements in containers.items():
            if elements:
                print(f"  ✓ {container_type}: {len(elements)} element(s)")
                if elements[0]:
                    text = elements[0].get_text(strip=True)[:100]
                    print(f"    First element text preview: {text}...")
        
        # Count paragraphs on page
        paragraphs = soup.find_all('p')
        print(f"\n✓ Total <p> tags found: {len(paragraphs)}")
        if paragraphs:
            print(f"  First 5 paragraphs:")
            for i, p in enumerate(paragraphs[:5]):
                text = p.get_text(strip=True)[:100]
                print(f"    {i+1}. {text}...")
                
    except Exception as e:
        print(f"Error: {e}")

def interactive_test():
    """Interactive testing"""
    print("\n" + "="*80)
    print("CRAWLER DIAGNOSTIC TOOL")
    print("="*80)
    
    while True:
        url = input("\nEnter URL to test (or 'quit' to exit): ").strip()
        
        if url.lower() == 'quit':
            break
        
        if not url.startswith('http'):
            url = 'https://' + url
        
        # Run analysis
        analyze_page_structure(url)
        
        # Run crawler test
        result = test_crawler_with_url(url)
        
        # Show raw HTML for debugging
        if result:
            print("\nWant to see the raw extracted HTML? (y/n): ", end="")
            if input().lower() == 'y':
                print(f"\nRaw HTML:\n{result.get('content')}")

if __name__ == '__main__':
    # Test with specific URLs if provided
    if len(sys.argv) > 1:
        for url in sys.argv[1:]:
            analyze_page_structure(url)
            test_crawler_with_url(url)
    else:
        interactive_test()
