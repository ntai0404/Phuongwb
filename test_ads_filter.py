#!/usr/bin/env python3
"""Test the new aggressive ads filter"""

import sys
from pathlib import Path

# Support both container path (/app/src) and local repo path
repo_root = Path(__file__).resolve().parent
local_src = repo_root / 'crawler-service' / 'src'
sys.path.insert(0, '/app/src')
sys.path.insert(0, str(local_src))

from web_crawler import ArticleCrawler

# Test cases from the problem, including the exact noisy ad snippet
test_cases = [
    # Case 1: Full mutex/taboola injection code that must be blocked
    """//Chèn ads giữa bài (runinit = window.runinit || []).push(function () { //Nếu k chạy ads thì return if (typeof _chkPrLink != 'undefined' && _chkPrLink) return; var mutexAds = ''; var content = $('[data-role="content"]'); if (content.length > 0) { var childNodes = content[0].childNodes; for (i = 0; i < childNodes.length; i++) { var childNode = childNodes[i]; var isPhotoOrVideo = false; if (childNode.nodeName.toLowerCase() == 'div') { // kiem tra xem co la anh khong? var type = $(childNode).attr('class') + ''; if (type.indexOf('VCSortableInPreviewMode') >= 0) { isPhotoOrVideo = true; } } try { if ((i >= childNodes.length / 2 - 1) && (i < childNodes.length / 2) && !isPhotoOrVideo) { if (i <= childNodes.length - 3) { childNode.after(htmlToElement(mutexAds)); arfAsync.push("l2srqb41"); } break; } } catch (e) { } } } }); function htmlToElement(html) { var template = document.createElement('template'); template.innerHTML = html; return template.content.firstChild; }""",

    # Case 2: Condensed allow3rd tracking snippet
    "pageSettings.allow3rd _mgq.load laNuocNgoai _isAdsHidden",

    # Case 3: Generic taboola mid-article label
    "Taboola mid article widget placement",

    # Case 4: Timestamp noise that should be treated as non-content
    "Sat Jan 10 2026 12:08:00 GMT+0700 (Giờ Đông Dương)",

    # Case 5: Normal text mentioning container/placement should NOT be filtered
    "Bài viết mô tả container vận chuyển và việc bố trí placement hàng hóa an toàn.",

    # Case 6: Normal article text with multiple sentences
    "Thị trường chứng khoán hôm nay tăng 2.5% do tin tức tích cực về nền kinh tế. Nhà đầu tư đang mong chờ báo cáo kết quả kinh doanh quý 4.",
]

expected_results = [
    True,   # Case 1: Should be blocked (full ads code)
    True,   # Case 2: Should be blocked (tracking markers)
    True,   # Case 3: Should be blocked (taboola markers)
    True,   # Case 4: Should be blocked (timestamp noise)
    False,  # Case 5: Should NOT be filtered (normal text about container/placement)
    False,  # Case 6: Should NOT be filtered (normal article)
]

crawler = ArticleCrawler()

print("=" * 80)
print("TESTING AGGRESSIVE ADS FILTER")
print("=" * 80)

passed = 0
failed = 0

for i, (test, expected) in enumerate(zip(test_cases, expected_results)):
    result = crawler._is_javascript_content(test)
    status = "✓ PASS" if result == expected else "✗ FAIL"
    
    if result == expected:
        passed += 1
    else:
        failed += 1
    
    print(f"\nTest {i+1}: {status}")
    print(f"Expected: {expected}, Got: {result}")
    if len(test) > 100:
        print(f"Content: {test[:100]}...")
    else:
        print(f"Content: {test}")

print("\n" + "=" * 80)
print(f"RESULTS: {passed} passed, {failed} failed")
print("=" * 80)

if failed == 0:
    print("\n✓ ALL TESTS PASSED! The aggressive filter is working correctly!")
    sys.exit(0)
else:
    print(f"\n✗ {failed} tests failed!")
    sys.exit(1)
