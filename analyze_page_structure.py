#!/usr/bin/env python3
"""
Debug script to analyze page structure and identify why content isn't being extracted
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawler-service', 'src'))

from web_crawler import ArticleCrawler
import requests
from bs4 import BeautifulSoup
import re

def analyze_page(url):
    """Detailed analysis of page structure"""
    print(f"\n{'='*90}")
    print(f"Analyzing: {url}")
    print(f"{'='*90}\n")
    
    try:
        crawler = ArticleCrawler()
        response = requests.get(url, headers=crawler.headers, timeout=15)
        response.encoding = 'utf-8'
        
        print(f"✓ Fetched: {len(response.content):,} bytes\n")
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Find various article containers
        containers = {
            '<article>': soup.find('article'),
            'article.fck_detail': soup.find('article', class_=re.compile(r'fck_detail', re.I)),
            'article.content_detail': soup.find('article', class_=re.compile(r'content_detail', re.I)),
            'div.ArticleContent': soup.find('div', class_=re.compile(r'ArticleContent', re.I)),
            'div.fck_detail': soup.find('div', class_=re.compile(r'fck_detail', re.I)),
            'div.content_detail': soup.find('div', class_=re.compile(r'content_detail', re.I)),
            'div#main-detail': soup.find('div', id=re.compile(r'main-detail', re.I)),
            'div.article-body': soup.find('div', class_=re.compile(r'article-body', re.I)),
            'div.article-content': soup.find('div', class_=re.compile(r'article-content', re.I)),
            'div.story-body': soup.find('div', class_=re.compile(r'story-body', re.I)),
            '<main>': soup.find('main'),
            'div[role=main]': soup.find('div', attrs={'role': 'main'}),
        }
        
        found_containers = []
        for selector, elem in containers.items():
            if elem:
                found_containers.append(selector)
                text_len = len(elem.get_text(strip=True))
                p_count = len(elem.find_all('p'))
                print(f"✓ Found: {selector}")
                print(f"  - Text length: {text_len:,} characters")
                print(f"  - Paragraphs: {p_count}")
        
        if not found_containers:
            print("✗ No article containers found!")
            print("\nSearching for largest text container...")
            all_divs = soup.find_all('div')
            if all_divs:
                largest = max(all_divs, key=lambda d: len(d.get_text(strip=True)))
                text_len = len(largest.get_text(strip=True))
                p_count = len(largest.find_all('p'))
                print(f"  Largest div: {text_len:,} characters, {p_count} paragraphs")
        
        print(f"\nAll paragraphs in page: {len(soup.find_all('p'))}")
        
        # Show first few paragraphs
        print("\nFirst 5 paragraphs on page:")
        for i, p in enumerate(soup.find_all('p')[:5], 1):
            text = p.get_text(strip=True)[:80]
            classes = ' '.join(p.get('class', []))
            print(f"  {i}. {text}..." if len(text) > 80 else f"  {i}. {text}")
            if classes:
                print(f"     class: {classes}")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    urls = [
        "https://vnexpress.net/",
        "https://vnexpress.net/thao-luan/hlv-thawatchai-va-nhung-phat-bieu-danh-the-tren-u23-trung-quoc-4755849.html",
    ]
    
    if len(sys.argv) > 1:
        urls = sys.argv[1:]
    
    for url in urls:
        analyze_page(url)
