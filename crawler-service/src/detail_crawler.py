"""
Compatibility module to satisfy existing tests.
Provides HTML cleaning and minimal stubs used by tests.
"""
from bs4 import BeautifulSoup
import re
from typing import Tuple

# Placeholder Article class (tests will monkeypatch this)
class Article:  # pragma: no cover
    def __init__(self, url: str, **kwargs):
        self.url = url

# Minimal queue publisher stub (tests monkeypatch this too)
def add_to_queue(queue_name: str, message: str) -> bool:  # pragma: no cover
    return True


def clean_and_minify_html(html: str) -> str:
    """Remove class attributes, comments and minify HTML while preserving structure.
    - Strips HTML comments
    - Removes all class attributes
    - Preserves other attributes (href, id, src, alt, etc.)
    - Collapses excess whitespace between tags
    """
    if not html:
        return ''

    # Remove comments first
    no_comments = re.sub(r'<!--.*?-->', '', html, flags=re.S)

    soup = BeautifulSoup(no_comments, 'lxml')

    # Remove all class attributes from tags
    for tag in soup.find_all(True):
        if 'class' in tag.attrs:
            del tag.attrs['class']

    # Convert back to string and collapse excess whitespace
    result = str(soup)
    # Trim leading/trailing whitespace inside tags is okay to keep; just collapse newlines
    result = re.sub(r'>\s+<', '><', result)

    return result.strip()
