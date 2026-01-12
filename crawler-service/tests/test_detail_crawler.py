#!/usr/bin/env python3
"""
Unit tests for detail_crawler module
"""
import json
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from detail_crawler import clean_and_minify_html


def test_clean_and_minify_html():
    """Test HTML cleaning and minification"""
    print("Testing clean_and_minify_html...")
    
    # Test with HTML containing classes
    html_input = '''
    <div class="container">
        <h1 class="title">Hello World</h1>
        <p class="content">This is a test paragraph.</p>
        <!-- This is a comment -->
    </div>
    '''
    
    result = clean_and_minify_html(html_input)
    
    # Verify classes are removed
    assert 'class=' not in result, "Classes should be removed"
    
    # Verify comments are removed
    assert '<!--' not in result, "Comments should be removed"
    
    # Verify content is preserved
    assert 'Hello World' in result, "Content should be preserved"
    assert 'This is a test paragraph.' in result, "Content should be preserved"
    
    # Verify structure is preserved
    assert '<div>' in result or '<div' in result, "div tag should be present"
    assert '<h1>' in result or '<h1' in result, "h1 tag should be present"
    assert '<p>' in result or '<p' in result, "p tag should be present"
    
    print("✓ clean_and_minify_html test passed")
    return True


def test_clean_and_minify_html_with_attributes():
    """Test HTML cleaning preserves non-class attributes"""
    print("Testing clean_and_minify_html with attributes...")
    
    html_input = '''
    <a href="https://example.com" class="link" id="main-link">Click here</a>
    <img src="image.jpg" class="photo" alt="Test image">
    '''
    
    result = clean_and_minify_html(html_input)
    
    # Verify classes are removed
    assert 'class=' not in result, "Classes should be removed"
    
    # Verify other attributes are preserved
    assert 'href=' in result, "href attribute should be preserved"
    assert 'id=' in result, "id attribute should be preserved"
    assert 'src=' in result, "src attribute should be preserved"
    assert 'alt=' in result, "alt attribute should be preserved"
    
    print("✓ clean_and_minify_html with attributes test passed")
    return True


def test_empty_html():
    """Test with empty HTML"""
    print("Testing with empty HTML...")
    
    result = clean_and_minify_html('')
    assert result == '', "Empty HTML should return empty string"
    
    print("✓ Empty HTML test passed")
    return True


def run_tests():
    """Run all tests"""
    print("\n" + "="*50)
    print("Running Detail Crawler Tests")
    print("="*50 + "\n")
    
    tests = [
        test_clean_and_minify_html,
        test_clean_and_minify_html_with_attributes,
        test_empty_html
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
            failed += 1
    
    print("\n" + "="*50)
    print(f"Tests completed: {passed} passed, {failed} failed")
    print("="*50 + "\n")
    
    return failed == 0


if __name__ == '__main__':
    success = run_tests()
    sys.exit(0 if success else 1)
