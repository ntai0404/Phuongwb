#!/usr/bin/env python3
"""Quick test of the crawler fix"""
import sys
import os
sys.path.insert(0, os.path.join(os.getcwd(), 'crawler-service', 'src'))

from web_crawler import ArticleCrawler
from bs4 import BeautifulSoup

# Test HTML similar to the reported issue
html = """
<article class="content_detail">
    <h1>HLV Thawatchai và những tuyên bố đanh thép</h1>
    <div class="article-text">
        <p>HLV Thawatchai đã dành nhiều lời khen cho các cầu thủ U.23 Thái Lan sau trận gặp U.23 Iraq.</p>
        <div class="text-inner">
            <p>Nội dung chi tiết đoạn 1 - Tình hình trận đấu và hiệu suất của các cầu thủ.</p>
            <p>Nội dung chi tiết đoạn 2 - Những điểm sáng trong hiệp một.</p>
            <div class="deep-text">
                <p>Nội dung chi tiết đoạn 3 - Phân tích hiệp hai của trận đấu.</p>
                <p>Nội dung chi tiết đoạn 4 - Tổng kết về kỹ thuật của các cầu thủ.</p>
            </div>
        </div>
    </div>
</article>
"""

soup = BeautifulSoup(html, 'html.parser')
article = soup.find('article')

# Run crawler
crawler = ArticleCrawler()
result = crawler._collect_paragraphs_with_images(article, 'https://example.com')

p_count = result.count('<p>')
print('='*90)
print('CRAWLER FIX - QUICK VERIFICATION')
print('='*90)
print()
print(f'✅ RESULT:')
print(f'   Paragraphs extracted: {p_count}')
print(f'   Total characters: {len(result):,}')
print()
print('Content extracted:')
print('-'*90)
print(result)
print('-'*90)
print()
if p_count >= 4:
    print('✅ SUCCESS: All nested paragraphs captured!')
else:
    print(f'❌ ISSUE: Expected 4+ paragraphs, got {p_count}')
