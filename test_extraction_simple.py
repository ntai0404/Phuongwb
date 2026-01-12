#!/usr/bin/env python3
"""Test extraction function directly"""
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'crawler-service', 'src'))

from web_crawler import ArticleCrawler
from bs4 import BeautifulSoup

# Simplified test with real article structure
test_html = """
<article class="fck_detail">
    <h1>Tiêu đề bài viết</h1>
    <div class="article-wrapper">
        <div class="content">
            <p>Đoạn 1 của bài viết này là nội dung chi tiết.</p>
            <p>Đoạn 2: Thêm thông tin về chủ đề.</p>
            <p>Đoạn 3: Chi tiết thứ ba.</p>
            <p>Đoạn 4: Kết luận.</p>
        </div>
    </div>
</article>
"""

soup = BeautifulSoup(test_html, 'html.parser')
article = soup.find('article')

crawler = ArticleCrawler()
content = crawler._collect_paragraphs_with_images(article, "https://example.com")

print("="*80)
print("EXTRACTION TEST")
print("="*80)
print(f"\nExtracted content ({len(content)} chars):")
print(content)
print(f"\n✅ Content extracted: {len(content) > 0}")
