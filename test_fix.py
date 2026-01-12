#!/usr/bin/env python3
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'crawler-service', 'src'))

# Import lại để tránh cache
import importlib
if 'web_crawler' in sys.modules:
    del sys.modules['web_crawler']

from web_crawler import ArticleCrawler
from bs4 import BeautifulSoup

html = """<article><h1>Test</h1><p>A</p><p>B</p><p>C</p></article>"""
soup = BeautifulSoup(html, 'html.parser')
crawler = ArticleCrawler()
result = crawler._collect_paragraphs_with_images(soup.find('article'), "https://example.com")

print(f"Length: {len(result)}")
print(f"Content:\n{result}")
print(f"\nStatus: {'✅ OK (>= 50)' if len(result) >= 50 else '❌ TOO SHORT (< 50)'}")
