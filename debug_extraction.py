#!/usr/bin/env python3
"""
Debug script - kiểm tra xem hàm _collect_paragraphs_with_images có lấy content không
"""
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'crawler-service', 'src'))

from web_crawler import ArticleCrawler
from bs4 import BeautifulSoup

html = """
<article class="fck_detail">
    <h1>Tiêu đề bài viết</h1>
    <div class="article-text">
        <p>Đoạn 1</p>
        <p>Đoạn 2</p>
        <p>Đoạn 3</p>
    </div>
</article>
"""

soup = BeautifulSoup(html, 'html.parser')
article = soup.find('article')

crawler = ArticleCrawler()

# Kiểm tra hàm extraction
print("Testing _collect_paragraphs_with_images...")
result = crawler._collect_paragraphs_with_images(article, "https://example.com")

print(f"Result type: {type(result)}")
print(f"Result length: {len(result)}")
print(f"Result content:\n{result}")
print()

if len(result) < 100:
    print(f"❌ PROBLEM: Content too short ({len(result)} < 100)")
else:
    print(f"✅ OK: Content long enough ({len(result)} >= 100)")
