"""
Real Web Crawler using BeautifulSoup
Collects full article content (text + images) from Vietnamese news sites.
"""

import logging
import re
from typing import Dict, List, Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


class ArticleCrawler:
    def __init__(self, timeout: int = 15):
        self.timeout = timeout
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121 Safari/537.36'
        }

    # ------------------------------------------------------------------
    # Helpers
    def _abs_url(self, src: Optional[str], page_url: str) -> Optional[str]:
        if not src:
            return None
        return urljoin(page_url, src)

    def _is_javascript_content(self, text: str) -> bool:
        if not text or len(text) < 5:
            return False

        text_lower = text.lower()

        absolute_blocklist = [
            'taboola', 'outbrain', 'arfasync', 'mutexads', '_taboola', 'runinit', '_mgq',
            'window.runinit', 'window.pagesettings', 'window._isadshidden',
            'document.queryselector', 'document.createelement',
            'addeventlistener', '.push(', '.call(', 'htmltoelement',
        ]
        if any(k in text_lower for k in absolute_blocklist):
            return True

        js_patterns = [
            'function(', 'function ()', 'document.createelement', 'document.queryselector',
            '.appendchild', '.insertbefore', 'var ', 'const ', 'let ',
            '.getattribute', '.setattribute', 'typeof ', 'typeof window',
        ]
        if sum(1 for p in js_patterns if p in text_lower) >= 2:
            return True

        if text_lower.startswith(('//', '/*', '(function')):
            return True
        if text.count('{') >= 2 and text.count('}') >= 2:
            return True
        return False

    # ------------------------------------------------------------------
    # Content collection
    def _collect_paragraphs_with_images(self, container, page_url: str, p_selector: Optional[Dict] = None) -> str:
        """Traverse DOM depth-first to preserve text+image order (VNExpress, ThanhNien)."""

        # Remove unwanted elements globally (keep iframes for potential video)
        for unwanted in container.find_all(['script', 'style', 'noscript']):
            unwanted.decompose()

        # Remove header/footer/navigation/metadata for ThanhNien
        for unwanted_class in container.find_all(class_=re.compile(r'breadcrumb|header|footer|nav|author|time|date|share|social|comment|relate|sidebar|widget|tool|tag|category-label|detail-tab', re.I)):
            unwanted_class.decompose()
        
        # Remove by ID
        for unwanted_id in container.find_all(id=re.compile(r'header|footer|nav|sidebar|comment|relate', re.I)):
            unwanted_id.decompose()

        # Remove related-topic/tag blocks by text (e.g., "Khám phá thêm chủ đề")
        topic_text_patterns = [
            'khám phá thêm', 'chủ đề', 'từ khóa', 'tin liên quan',
            'cùng chuyên mục', 'đọc thêm', 'có thể bạn quan tâm',
            'dòng sự kiện', 'detail info=', 'siteid185', 'threadid',
            'tin đọc nhiều', 'for inquiries'
        ]
        for section in container.find_all(['div', 'section', 'aside', 'ul', 'ol', 'p']):
            text = section.get_text(separator=' ', strip=True).lower()
            if text and any(pat in text for pat in topic_text_patterns):
                section.decompose()

        # Remove ThanhNien tag/highlight blocks (only when they are tag/related sections)
        for block in container.find_all(class_=re.compile(r'detail__cmain-flex|detail-tab|tag-title|highlight', re.I)):
            text = block.get_text(separator=' ', strip=True).lower()
            if any(pat in text for pat in topic_text_patterns):
                block.decompose()

        # Remove obvious ad blocks
        ads_selectors = [
            {'class': re.compile(r'(\b(ad|ads|advertisement|sponsor|taboola|outbrain|banner)\b)', re.I)},
            {'id': re.compile(r'(\b(ad|ads|advertisement|sponsor|taboola|outbrain|banner)\b)', re.I)},
        ]
        for selector in ads_selectors:
            for ad in container.find_all(['div', 'section'], selector):
                ad.decompose()

        # Remove by attributes (e.g., data-role="tags")
        for section in container.find_all(True):
            for attr_name, attr_val in section.attrs.items():
                if isinstance(attr_val, list):
                    attr_val_join = ' '.join(map(str, attr_val)).lower()
                else:
                    attr_val_join = str(attr_val).lower()
                if attr_name in ['data-role', 'role', 'data-component', 'data-widget'] and 'tags' in attr_val_join:
                    section.decompose()
                    break

        # Inline scripts with ad keywords
        for script in container.find_all('script'):
            script_text = script.get_text(strip=True).lower()
            if any(k in script_text for k in ['taboola', 'outbrain', 'mutexads', 'runinit', '_mgq', '_taboola']):
                script.decompose()

        content_parts: List[str] = []
        video_providers = ['youtube.com', 'youtu.be', 'vimeo.com', 'player.vcdn.vn', 'video.thanhnien.vn', 'vnecdn']

        category_stopwords = {
            'thể thao', 'bóng đá việt nam', 'kinh tế', 'bất động sản',
            'tín dụng', 'ngân hàng', 'chính phủ', 'highlight'
        }

        def walk(node):
            # Text node
            if isinstance(node, str):
                text = node.strip()
                if text and len(text) > 0 and not self._is_javascript_content(text):
                    text_lower = text.lower().replace('\xa0', ' ').strip()
                    if text_lower in category_stopwords:
                        return
                    if not text.startswith('(function') and not text.startswith('//'):
                        content_parts.append(f'<p>{text}</p>')
                return

            if not hasattr(node, 'name') or not node.name:
                return

            tag = node.name.lower()
            if tag in ['script', 'style', 'noscript', 'button', 'input', 'form', 'nav', 'header', 'footer', 'aside']:
                return
            
            # Skip elements with metadata/navigation classes
            elem_class = ' '.join(node.get('class', [])).lower()
            if any(x in elem_class for x in ['breadcrumb', 'author', 'time-', 'date-', 'share', 'social', 'comment', 'relate', 'tag', 'category-label', 'discover', 'thread', 'topic', 'keyword', 'detail-tab']):
                return

            # Video tag
            if tag == 'video':
                src = node.get('src') or node.get('data-src') or node.get('data-original')
                if not src:
                    source_tag = node.find('source')
                    if source_tag:
                        src = source_tag.get('src') or source_tag.get('data-src')
                abs_src = self._abs_url(src, page_url)
                if abs_src:
                    poster = node.get('poster') or ''
                    poster_attr = f' poster="{self._abs_url(poster, page_url)}"' if poster else ''
                    content_parts.append(f'<video controls src="{abs_src}"{poster_attr}></video>')
                return

            # Iframe video embeds (allowlisted providers or src hint)
            if tag == 'iframe':
                src = node.get('src') or node.get('data-src') or ''
                src_lower = src.lower()
                if any(provider in src_lower for provider in video_providers) or re.search(r'(video|embed|player)', src_lower):
                    abs_src = self._abs_url(src, page_url)
                    if abs_src:
                        content_parts.append(f'<iframe src="{abs_src}" allowfullscreen loading="lazy"></iframe>')
                return

            # Paragraphs
            if tag == 'p':
                text = node.get_text(strip=True)
                # Skip short metadata paragraphs
                if text and len(text) > 5 and not self._is_javascript_content(text):
                    # Skip common metadata patterns
                    text_lower = text.lower().replace('\xa0', ' ').strip()
                    if text_lower in category_stopwords:
                        return
                    if not any(pattern in text_lower for pattern in ['chia sẻ', 'khám phá thêm', '@gmail.com', 'gmt+7', 'gmt+0700', 'giờ đông dương']):
                        content_parts.append(f'<p>{text}</p>')
                return

            # Headings - only h2 and below (h1 is usually title)
            if tag in ['h2', 'h3', 'h4', 'h5', 'h6']:
                text = node.get_text(strip=True)
                if text:
                    content_parts.append(f'<{tag}>{text}</{tag}>')
                return

            # Blockquote
            if tag == 'blockquote':
                text = node.get_text(strip=True)
                if text:
                    content_parts.append(f'<blockquote>{text}</blockquote>')
                return


            # Tables
            if tag == 'table':
                table_html = str(node)
                content_parts.append(table_html)
                return

            # Lists
            if tag in ['ul', 'ol']:
                items = []
                for li in node.find_all('li', recursive=False):
                    li_text = li.get_text(strip=True)
                    if li_text:
                        items.append(f'<li>{li_text}</li>')
                if items:
                    content_parts.append(f'<{tag}>{"".join(items)}</{tag}>')
                return

            # Figure: may contain image or video/iframe + caption
            if tag == 'figure':
                processed_media = False
                iframe = node.find('iframe')
                if iframe:
                    i_src = iframe.get('src') or iframe.get('data-src') or ''
                    i_src_lower = i_src.lower()
                    if any(p in i_src_lower for p in video_providers) or re.search(r'(video|embed|player)', i_src_lower):
                        abs_src = self._abs_url(i_src, page_url)
                        if abs_src:
                            content_parts.append(f'<iframe src="{abs_src}" allowfullscreen loading="lazy"></iframe>')
                            processed_media = True
                video = node.find('video')
                if video and not processed_media:
                    src = video.get('src') or video.get('data-src') or video.get('data-original')
                    if not src:
                        source_tag = video.find('source')
                        if source_tag:
                            src = source_tag.get('src') or source_tag.get('data-src')
                    abs_src = self._abs_url(src, page_url)
                    if abs_src:
                        poster = video.get('poster') or ''
                        poster_attr = f' poster="{self._abs_url(poster, page_url)}"' if poster else ''
                        content_parts.append(f'<video controls src="{abs_src}"{poster_attr}></video>')
                        processed_media = True
                if not processed_media:
                    img = node.find('img')
                    if img:
                        src = img.get('data-src') or img.get('src') or img.get('data-original')
                        abs_src = self._abs_url(src, page_url)
                        if abs_src:
                            alt = img.get('alt') or ''
                            content_parts.append(f'<img src="{abs_src}" alt="{alt}" />')
                caption = node.find('figcaption')
                if caption:
                    cap_text = caption.get_text(strip=True)
                    if cap_text:
                        content_parts.append(f'<p><em>{cap_text}</em></p>')
                return

            if tag == 'img':
                src = node.get('data-src') or node.get('src') or node.get('data-original')
                abs_src = self._abs_url(src, page_url)
                if abs_src:
                    alt = node.get('alt') or ''
                    content_parts.append(f'<img src="{abs_src}" alt="{alt}" />')
                return

            # Generic container: recurse children to preserve order
            for child in node.children:
                walk(child)

        walk(container)

        # If still empty, fallback to all text
        if not content_parts:
            text_content = container.get_text(separator='\n', strip=True)
            if text_content:
                lines = text_content.split('\n')
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 10 and not self._is_javascript_content(line):
                        content_parts.append(f'<p>{line}</p>')

        return '\n'.join(content_parts)
    def crawl_generic(self, url: str) -> Optional[Dict]:
        """Generic crawler for unknown sites"""
        try:
            response = requests.get(url, headers=self.headers, timeout=self.timeout)
            response.encoding = 'utf-8'
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Try common article selectors (broad but ordered)
            article_body = (
                soup.find('article') or
                # ThanhNien specific classes
                soup.find('div', class_=re.compile(r'detail-content|detail__main|detail__cmain-main|detail__cmain|afcbc-body', re.I)) or
                # VNExpress selectors (broadened)
                soup.find('div', class_=re.compile(r'fck_detail|content_detail|detail__content|read__content|main-detail|container_detail|content-detail|section-content|article-content|section-content', re.I)) or
                soup.find('section', class_=re.compile(r'section-content|article-content', re.I)) or
                soup.find('div', class_=re.compile(r'article-body|article__body|story-body|post-content|entry-content|main-content|post', re.I)) or
                soup.find('div', id=re.compile(r'article|content|detail|body', re.I)) or
                soup.find('main') or
                soup.find('div', class_=re.compile(r'article|content|detail|body|main-content|post', re.I))
            )

            # Fallback: choose the div with the most text
            if not article_body:
                divs = soup.find_all('div')
                if divs:
                    article_body = max(divs, key=lambda d: len(d.get_text(strip=True)))
            
            if not article_body:

                logger.warning(f"Could not find article body for {url}")
                return None
            
            content_html = self._collect_paragraphs_with_images(article_body, url)
            
            # Accept content as long as it's non-empty. Some sources have short bodies.
            if content_html and len(content_html.strip()) > 0:
                return {
                    'content': content_html,
                    'success': True
                }
            
            return None
        except Exception as e:
            logger.error(f"Error crawling generic {url}: {e}")
            return None
    
    def crawl_article(self, url: str) -> Optional[Dict]:
        """Universal entry point - currently all domains use the generic crawler"""
        logger.info(f"Crawling article: {url}")
        return self.crawl_generic(url)
