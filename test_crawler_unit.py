#!/usr/bin/env python3
"""
Unit test for the crawler fix using sample HTML
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'crawler-service', 'src'))

from web_crawler import ArticleCrawler
from bs4 import BeautifulSoup

# Sample HTML that mimics typical news site structure
SAMPLE_ARTICLE_HTML = """
<!DOCTYPE html>
<html>
<head><title>Test Article</title></head>
<body>
<article class="fck_detail">
    <h1>HLV Thawatchai dành khen cho các cầu thủ U.23 Thái Lan</h1>
    
    <p>HLV Thawatchai đã dành nhiều lời khen cho các cầu thủ U.23 Thái Lan sau trận gặp U.23 Iraq.</p>
    
    <p>Đây là một đoạn nội dung chi tiết về hiệu suất của các cầu thủ trẻ trong trận đấu này. HLV rất hài lòng với cách các em thi đấu.</p>
    
    <img src="/images/hlv-thawatchai.jpg" alt="HLV Thawatchai" />
    
    <p>Kỹ năng chuyền bóng của các cầu thủ được cải thiện rõ rệt so với trận trước. Họ đã chỉ ra những yêu cầu cao trong từng pha bóng.</p>
    
    <h2>Tuyên bố về trận gặp U.23 Trung Quốc</h2>
    
    <p>Khi được hỏi về trận gặp U.23 Trung Quốc, HLV có những tuyên bố đầy đanh thép. Ông tin rằng đội tuyển sẽ có cơ hội tốt để chiến thắng.</p>
    
    <p>Đây sẽ là một trận đấu quan trọng quyết định vị trí của các cầu thủ. HLV sẵn sàng với một kế hoạch chiến thuật cụ thể cho trận này.</p>
    
    <blockquote>
        <p>"Tôi tin vào khả năng của các cầu thủ này. Họ sẽ chứng minh được giá trị của mình trước đội Trung Quốc," HLV Thawatchai nói.</p>
    </blockquote>
    
    <p>Nhóm phòng ngự của Thái Lan sẽ cần phải chủ động hơn trong việc bám sát các cầu thủ tấn công của đội bạn.</p>
    
    <figure>
        <img src="/images/stadium.jpg" alt="Sân vận động" />
        <figcaption>Sân vận động nơi diễn ra trận đấu</figcaption>
    </figure>
    
    <p>Với kinh nghiệm từ những trận đấu trước, HLV đã chuẩn bị một chiến lược riêng để đối phó với đối thủ mạnh này.</p>
    
    <h3>Chuẩn bị cho trận đấu</h3>
    
    <p>Các cầu thủ sẽ tiếp tục tập luyện với cường độ cao để chuẩn bị cho trận đấu sắp tới. HLV chỉ ra những điểm còn yếu cần cải thiện.</p>
    
    <p>Chiến thắng trong trận này sẽ là bước đệm quan trọng cho các mục tiêu lớn hơn của đội tuyển.</p>
</article>
</body>
</html>
"""

def test_crawler_with_html():
    """Test the crawler with sample HTML"""
    print("="*90)
    print("CRAWLER FIX VALIDATION TEST")
    print("="*90)
    print("\nTesting with sample HTML containing multiple paragraphs, images, and figures...")
    
    crawler = ArticleCrawler()
    soup = BeautifulSoup(SAMPLE_ARTICLE_HTML, 'html.parser')
    article = soup.find('article')
    
    # Count paragraphs in source
    source_paragraphs = article.find_all('p')
    print(f"\nSource HTML contains:")
    print(f"  - {len(source_paragraphs)} <p> tags")
    print(f"  - {len(article.find_all('img'))} <img> tags")
    print(f"  - {len(article.find_all('figure'))} <figure> tags")
    print(f"  - {len(article.find_all('h1,h2,h3,h4,h5,h6'))} headings")
    print(f"  - {len(article.find_all('blockquote'))} blockquotes")
    
    # Run crawler
    print("\n" + "-"*90)
    print("Running crawler...")
    print("-"*90)
    
    extracted_content = crawler._collect_paragraphs_with_images(article, "https://example.com")
    
    # Analyze extracted content
    print(f"\n✓ Extraction completed!")
    print(f"  Total extracted: {len(extracted_content):,} characters")
    print(f"  Paragraphs extracted: {extracted_content.count('<p>')}")
    print(f"  Images extracted: {extracted_content.count('<img')}")
    print(f"  Figures extracted: {extracted_content.count('<figure')}")
    print(f"  Headings extracted: {extracted_content.count('<h')}")
    print(f"  Blockquotes extracted: {extracted_content.count('<blockquote')}")
    
    # Coverage analysis
    p_extracted = extracted_content.count('<p>')
    p_source = len(source_paragraphs)
    coverage = (p_extracted / p_source * 100) if p_source > 0 else 0
    
    print(f"\n  Coverage: {p_extracted}/{p_source} paragraphs ({coverage:.1f}%)")
    
    if coverage >= 90:
        print("\n✓ TEST PASSED: Excellent coverage of content!")
        return True
    elif coverage >= 75:
        print("\n⚠ TEST WARNING: Good coverage but some content may be missing")
        return True
    else:
        print(f"\n✗ TEST FAILED: Low coverage ({coverage:.1f}%)")
        return False
    
    print("\n" + "="*90)
    print("EXTRACTED CONTENT:")
    print("="*90)
    print(extracted_content)

if __name__ == '__main__':
    success = test_crawler_with_html()
    sys.exit(0 if success else 1)
