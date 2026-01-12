# 📚 KIẾN TRÚC HỆ THỐNG PHUONG WEB

## 📋 Mục Lục
1. [Tổng Quan Kiến Trúc](#tổng-quan-kiến-trúc)
2. [Các Microservices](#các-microservices)
3. [Luồng Dữ Liệu](#luồng-dữ-liệu)
4. [Cấu Trúc Thư Mục](#cấu-trúc-thư-mục)
5. [Giải Thích Chi Tiết Từng File](#giải-thích-chi-tiết-từng-file)
6. [Quy Trình Hoạt Động](#quy-trình-hoạt-động)

---

## 🎯 Tổng Quan Kiến Trúc

**Phuong Web** là một hệ thống **tin tức thông minh** có 3 cách lấy dữ liệu:

### 1. **RSS Feeds** (Cách 1)
- Lấy từ RSS feed của các website tin tức
- **Nhanh**, dữ liệu **có sẵn định dạng**
- Được sử dụng: VNExpress, DanTri, ThanhNien, TuoiTre

### 2. **Web Crawling** (Cách 2 - MỚI)
- Tải **HTML trực tiếp** từ website
- **Parse HTML** để trích xuất **toàn bộ nội dung**
- Là **real crawling** thực sự (giáo viên sẽ hài lòng!)

### 3. **AI Classification** (Tự động phân loại)
- Phân loại bài viết vào **8 danh mục**
- Sử dụng **Semantic embeddings** + **keyword matching**

---

## 🔧 Các Microservices

### 1. **Frontend Service** (`frontend/`)
**Công Nghệ**: Next.js 14, React, TypeScript, Tailwind CSS

**Chức Năng**:
- Giao diện người dùng (web app)
- Hiển thị danh sách bài viết
- Xem chi tiết bài viết
- Lưu bài viết yêu thích
- Xem lịch sử đọc bài

**Port**: 3000

---

### 2. **Core API Service** (`core-api-service/`)
**Công Nghệ**: FastAPI, Python 3.11

**Chức Năng**:
- API chính của hệ thống
- Quản lý users, articles, sources
- Xác thực (authentication)
- Lưu bài viết yêu thích
- Phân loại bài viết tự động

**Port**: 8080

**Các Module**:
- `auth/`: Xử lý đăng nhập, đăng ký
- `articles/`: Quản lý bài viết
- `sources/`: Quản lý RSS sources
- `crawler/`: Kích hoạt crawling
- `classifier.py`: AI phân loại bài viết

---

### 3. **Crawler Service** (`crawler-service/`)
**Công Nghệ**: Python 3.11, BeautifulSoup, Requests

**Chức Năng**:
- Crawl từ RSS feeds
- Crawl từ HTML website (real crawling)
- Gửi dữ liệu qua RabbitMQ message queue

**Port**: 8003

**Các Module**:
- `main.py`: Khởi động service, RSS crawling
- `web_crawler.py`: **Web crawler chính** - crawl HTML từ website

---

### 4. **Summary Service** (`summary-service/`)
**Công Nghệ**: Python 3.11, Hugging Face Transformers

**Chức Năng**:
- Tóm tắt AI bài viết dài
- Sử dụng mô hình BART

**Port**: 8004

---

### 5. **Recommendation Service** (`recommendation-service/`)
**Công Nghệ**: Python 3.11

**Chức Năng**:
- Gợi ý bài viết dựa trên lịch sử đọc
- Collaborative filtering

**Port**: 8005

---

## 📊 Luồng Dữ Liệu

```
┌─────────────────────────────────────────────────────────┐
│                    Người Dùng Web                       │
│              (Browser / Frontend)                       │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓ HTTP Request
┌──────────────────────────────────────────────────────────┐
│                  Frontend (Next.js)                      │
│    - Hiển thị tin tức                                    │
│    - Xử lý login/register                                │
│    - Lưu bài yêu thích                                  │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ↓ API Call (REST)
┌──────────────────────────────────────────────────────────┐
│              Core API Service (FastAPI)                  │
│    - /api/v1/articles (GET articles)                     │
│    - /api/v1/auth/login (Đăng nhập)                     │
│    - /api/v1/articles/save (Lưu bài)                    │
│    - /api/v1/crawler/trigger (Kích hoạt)               │
└──────────┬────────────────────────────────────────┬──────┘
           │                                        │
           ↓ (Trigger)                              ↓ (Query)
    ┌─────────────────┐                      ┌──────────────┐
    │ Crawler Service │                      │   Database   │
    │ - RSS Crawling  │                      │  (PostgreSQL)│
    │ - Web Crawling  │                      └──────────────┘
    └────────┬────────┘
             │
             ↓ (Message Queue)
    ┌─────────────────────┐
    │  RabbitMQ Queue     │
    │ (crawled_data)      │
    └────────┬────────────┘
             │
             ↓ (Consume)
    ┌─────────────────────┐
    │  Core API Worker    │
    │ - Lưu articles      │
    │ - Phân loại (AI)    │
    │ - Tóm tắt (AI)      │
    └─────────────────────┘
```

---

## 📁 Cấu Trúc Thư Mục

```
phuong-web/
├── frontend/                          # 🎨 Next.js Frontend
│   ├── app/
│   │   ├── page.tsx                   # Trang chính
│   │   ├── layout.tsx                 # Layout chung
│   │   ├── admin/page.tsx             # Admin panel
│   │   ├── articles/page.tsx          # Trang bài viết
│   │   ├── saved/page.tsx             # Bài viết lưu
│   │   └── history/page.tsx           # Lịch sử đọc
│   ├── components/
│   │   ├── news-card.tsx              # Card hiển thị bài viết
│   │   ├── news-grid.tsx              # Grid danh sách bài
│   │   ├── news-detail-modal.tsx      # 🔑 Modal chi tiết bài viết
│   │   ├── sidebar.tsx                # Sidebar danh mục
│   │   ├── topbar.tsx                 # Top bar search
│   │   └── providers/
│   │       ├── auth-provider.tsx      # Auth context
│   │       └── query-provider.tsx     # React Query
│   ├── hooks/
│   │   └── use-articles.ts            # Hook fetch articles
│   ├── lib/
│   │   ├── api.ts                     # API client
│   │   └── api-client.ts              # Axios client
│   └── package.json
│
├── core-api-service/                  # 🔌 FastAPI Backend
│   ├── src/
│   │   ├── main.py                    # Khởi động API
│   │   ├── classifier.py              # 🤖 AI phân loại bài
│   │   ├── models/
│   │   │   └── db.py                  # SQLAlchemy models
│   │   ├── auth/
│   │   │   ├── routes.py              # Login/Register API
│   │   │   └── utils.py               # JWT, Password
│   │   ├── articles/
│   │   │   ├── routes.py              # GET/POST articles API
│   │   │   └── db.py                  # Article DB queries
│   │   ├── sources/
│   │   │   ├── routes.py              # RSS sources API
│   │   │   └── db.py                  # Source DB queries
│   │   ├── crawler/
│   │   │   └── routes.py              # Trigger crawler API
│   │   └── worker.py                  # 🔄 Worker xử lý messages
│   └── pyproject.toml
│
├── crawler-service/                   # 🕷️ Web Crawler
│   ├── src/
│   │   ├── main.py                    # 🔑 RSS crawling + RabbitMQ
│   │   └── web_crawler.py             # 🔑 Web crawling từ HTML
│   ├── tests/
│   │   └── test_integration.py        # Integration tests
│   └── pyproject.toml
│
├── summary-service/                   # 📝 AI Summary
│   └── main.py                        # Tóm tắt bài viết
│
├── recommendation-service/            # 💡 Recommendations
│   └── main.py                        # Gợi ý bài viết
│
├── docker-compose.yml                 # 🐳 Docker Compose
├── pyproject.toml                     # Python dependencies
└── README.md
```

---

## 🔍 Giải Thích Chi Tiết Từng File

### **Frontend Files**

#### `frontend/components/news-detail-modal.tsx` 🔑 **QUAN TRỌNG**
```typescript
// File này hiển thị chi tiết bài viết khi user click vào một bài

export default function NewsDetailModal({ article, isOpen, onClose }) {
  // 1. Lấy dữ liệu user từ Auth context
  const { user } = useAuth();
  
  // 2. Lấy bài viết liên quan
  const { data: relatedArticles } = useRelatedArticles(article?.id);
  
  // 3. Xử lý lưu bài viết
  const saveArticleMutation = useMutation({
    mutationFn: async (articleId) => {
      // Gọi API POST /api/v1/articles/save/{articleId}
      const response = await fetch(
        `${API_URL}/api/v1/articles/save/${articleId}?user_id=${user.id}`,
        { method: isSaved ? 'DELETE' : 'POST' }
      );
      return response.json();
    }
  });
  
  // 4. Đánh dấu bài đã đọc
  useEffect(() => {
    if (isOpen && article?.id) {
      // Gọi API POST /api/v1/articles/read/{articleId}
      fetch(`${API_URL}/api/v1/articles/read/${article.id}?user_id=${user.id}`, {
        method: 'POST'
      });
    }
  }, [isOpen]);
  
  // 5. Hiển thị HTML content từ crawler
  return (
    <div className="prose prose-lg">
      <h1>{article.title}</h1>
      <img src={article.image_url} />
      {/* 🔑 Đây là phần quan trọng: render full HTML content */}
      <div dangerouslySetInnerHTML={{ __html: article.content }} />
    </div>
  );
}
```

**Dòng chảy**:
1. User click vào bài viết → Modal mở
2. Gọi API mark as read → Lưu vào DB
3. Hiển thị: Title → Summary → Image → Full Content (từ crawler)
4. User click "Lưu" → API POST /save → DB lưu

---

#### `frontend/app/page.tsx` (Trang chính)
```typescript
// Hiển thị danh sách bài viết chính

function HomeContent() {
  // 1. Lấy danh mục được chọn từ URL
  const selectedCategory = useSearchParams().get('category') || 'all';
  
  // 2. Fetch bài viết từ API
  const { data: articles } = useArticles(); // GET /api/v1/articles
  
  // 3. Normalize category names từ API (business → Kinh doanh)
  const normalizeCategoryName = (cat) => {
    const categoryMap = {
      'business': 'Kinh doanh',
      'technology': 'Công nghệ',
      'sports': 'Thể thao',
      'entertainment': 'Giải trí',
    };
    return categoryMap[cat] || cat;
  };
  
  // 4. Filter bài theo danh mục được chọn
  const filtered = articles.filter(item => {
    const category = normalizeCategoryName(item.category);
    return selectedCategory === 'all' || category === selectedCategory;
  });
  
  return (
    <div>
      <Sidebar selectedCategory={selectedCategory} /> {/* Chọn danh mục */}
      <NewsGrid articles={filtered} /> {/* Hiển thị danh sách */}
    </div>
  );
}
```

---

### **Backend Files**

#### `core-api-service/src/main.py` (Khởi động API)
```python
# FastAPI server chính

from fastapi import FastAPI
from fastapi_cors import CORSMiddleware
from .models import init_db  # Khởi tạo database
from .worker import start_background_worker  # Khởi động consumer RabbitMQ

app = FastAPI()

# Thêm CORS middleware để frontend gọi được
app.add_middleware(CORSMiddleware, allow_origins=["*"])

# Khởi tạo database
@app.on_event("startup")
def startup():
    init_db()  # Tạo tables nếu chưa tồn tại
    start_background_worker()  # Khởi động RabbitMQ consumer

# Gồm các routes
app.include_router(auth_router)      # /api/v1/auth (login, register)
app.include_router(articles_router)  # /api/v1/articles (GET, POST, save)
app.include_router(sources_router)   # /api/v1/sources (RSS sources)
app.include_router(crawler_router)   # /api/v1/crawler (trigger)
```

---

#### `core-api-service/src/articles/routes.py` (API bài viết)
```python
# API endpoints cho bài viết

@router.get("/api/v1/articles")
def get_articles(skip: int = 0, limit: int = 20):
    """
    Lấy danh sách bài viết
    - GET: /api/v1/articles?skip=0&limit=20
    - Response: [{ id, title, summary, content, image_url, category, ... }]
    """
    articles = db.query(Article).offset(skip).limit(limit).all()
    return articles

@router.get("/api/v1/articles/{article_id}")
def get_article(article_id: int):
    """
    Lấy chi tiết 1 bài viết
    - GET: /api/v1/articles/123
    - Response: { id: 123, title: "...", content: "...", ... }
    """
    article = db.query(Article).filter(Article.id == article_id).first()
    return article

@router.post("/api/v1/articles/save/{article_id}")
def save_article(article_id: int, user_id: int):
    """
    Lưu bài viết yêu thích
    - POST: /api/v1/articles/save/123?user_id=5
    - Xử lý: Tạo UserSavedArticle(user_id=5, article_id=123)
    """
    saved = db.query(UserSavedArticle).filter(
        UserSavedArticle.user_id == user_id,
        UserSavedArticle.article_id == article_id
    ).first()
    
    if not saved:
        db.add(UserSavedArticle(user_id=user_id, article_id=article_id))
        db.commit()
    
    return {"saved": True}

@router.post("/api/v1/articles/read/{article_id}")
def mark_as_read(article_id: int, user_id: int):
    """
    Đánh dấu bài đã đọc (lưu lịch sử)
    - POST: /api/v1/articles/read/123?user_id=5
    - Xử lý: Tạo UserReadingHistory
    """
    db.add(UserReadingHistory(
        user_id=user_id,
        article_id=article_id,
        read_at=datetime.now()
    ))
    db.commit()
    return {"read": True}
```

---

#### `core-api-service/src/worker.py` (Worker xử lý messages)
```python
# Worker nhận messages từ RabbitMQ queue

import pika
import json
from .classifier import classify_article
from .models import Article, db

def start_background_worker():
    """
    Khởi động worker xử lý messages
    
    Luồng:
    1. Connect tới RabbitMQ
    2. Subscribe vào queue 'crawled_data'
    3. Mỗi khi có message mới:
       - Parse JSON
       - Phân loại bài (AI)
       - Tóm tắt bài (optional)
       - Lưu vào database
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    
    # Tạo queue nếu chưa tồn tại
    channel.queue_declare(queue='crawled_data', durable=True)
    
    def callback(ch, method, properties, body):
        # Nhận message từ crawler
        article_data = json.loads(body)
        
        # 1. Phân loại
        category = classify_article(
            title=article_data['title'],
            summary=article_data['summary'],
            content=article_data['content']
        )
        
        # 2. Tạo Article object
        article = Article(
            title=article_data['title'],
            summary=article_data['summary'],
            content=article_data['content'],  # Full content từ crawler
            image_url=article_data.get('image_url'),
            link=article_data['link'],
            category=category,
            source_id=article_data['source_id']
        )
        
        # 3. Lưu vào database
        db.add(article)
        db.commit()
        
        # 4. Xác nhận message đã xử lý
        ch.basic_ack(delivery_tag=method.delivery_tag)
    
    # Subscribe vào queue
    channel.basic_consume(queue='crawled_data', on_message_callback=callback)
    channel.start_consuming()
```

---

#### `core-api-service/src/classifier.py` (AI phân loại)
```python
# 🤖 AI phân loại bài viết tự động

from sentence_transformers import SentenceTransformer
import numpy as np

# Load mô hình multilingual embeddings một lần
MODEL = SentenceTransformer("paraphrase-multilingual-MiniLM-L12-v2")

# Mô tả các danh mục (tiếng Việt)
CATEGORY_DESCRIPTIONS = {
    "Kinh doanh": "Kinh tế, tài chính, doanh nghiệp, chứng khoán",
    "Công nghệ": "Công nghệ, AI, phần mềm, internet, điện thoại",
    "Thể thao": "Thể thao, bóng đá, giải đấu, vận động viên",
    "Giải trí": "Giải trí, phim ảnh, âm nhạc, nghệ sĩ",
    "Chính trị": "Chính trị, chính phủ, quốc hội, chính sách",
    "Sức khỏe": "Sức khỏe, bệnh tật, y tế, thuốc",
    "Giáo dục": "Giáo dục, trường học, đại học, học sinh",
    "Pháp luật": "Pháp luật, luật lệ, tòa án, quyền lợi",
}

def classify_article(title: str, summary: str, content: str) -> str:
    """
    Phân loại bài viết vào 1 trong 8 danh mục
    
    Cách hoạt động:
    1. Kết hợp title + summary + content
    2. Tính embedding (vector 384 chiều)
    3. Tính similarity với embedding của mỗi danh mục
    4. Return danh mục có similarity cao nhất
    """
    # 1. Kết hợp text
    full_text = f"{title} {summary} {content}"[:512]  # Max 512 chars
    
    # 2. Tính embedding của bài viết
    article_embedding = MODEL.encode(full_text, convert_to_tensor=True)
    
    # 3. Tính similarity với từng danh mục
    max_similarity = -1
    best_category = "Khác"
    
    for category, description in CATEGORY_DESCRIPTIONS.items():
        category_embedding = MODEL.encode(description, convert_to_tensor=True)
        similarity = MODEL.util.pytorch_cos_sim(article_embedding, category_embedding)
        
        if similarity > max_similarity:
            max_similarity = similarity
            best_category = category
    
    return best_category
```

---

### **Crawler Files** 🕷️

#### `crawler-service/src/main.py` (RSS Crawling)
```python
# Khởi động crawler service
# Có 2 chức năng: RSS crawling + Web crawling

import feedparser
from web_crawler import ArticleCrawler

def fetch_feed(url: str, max_items: int = 50) -> list:
    """
    Crawl RSS feed từ website
    
    Quá trình:
    1. Parse RSS feed bằng feedparser
    2. Với mỗi article trong feed:
       a. Lấy title, summary từ RSS
       b. Crawl FULL content từ website (real crawling) ← 🔑 Mới!
       c. Lấy image URL
       d. Return dict: {title, summary, content, image_url, link, ...}
    
    Ví dụ:
    """
    parsed = feedparser.parse(url)
    articles = []
    
    web_crawler = ArticleCrawler()  # ← Khởi động web crawler
    
    for entry in parsed.entries[:max_items]:
        # Lấy từ RSS
        title = entry.title
        summary = entry.summary
        link = entry.link
        
        # 🔑 Crawl full content từ website HTML
        crawled_data = web_crawler.crawl_article(link)
        if crawled_data and crawled_data.get('success'):
            full_content = crawled_data.get('content', summary)
        else:
            full_content = summary  # Fallback to RSS summary
        
        # Lấy image
        image_url = extract_image_from_feed(entry)
        
        articles.append({
            'title': title,
            'summary': summary,
            'content': full_content,  # ← FULL content, not just summary!
            'link': link,
            'image_url': image_url,
        })
    
    return articles

def process_crawl_task(ch, method, properties, body):
    """
    RabbitMQ Consumer: Nhận task từ queue, crawl, gửi data về API
    
    Luồng:
    1. Nhận message: {source_id, url}
    2. Gọi fetch_feed(url) → Crawl RSS + HTML
    3. Gửi từng article vào queue 'crawled_data'
    4. Core API worker nhận → Phân loại → Lưu DB
    """
    task = json.loads(body)
    url = task.get('url')
    source_id = task.get('source_id')
    
    # Crawl RSS (+ web crawling bên trong)
    articles = fetch_feed(url, max_items=50)
    
    for article in articles:
        article['source_id'] = source_id
        
        # Gửi vào queue crawled_data
        publish_crawled_data(article)
    
    ch.basic_ack(delivery_tag=method.delivery_tag)
```

---

#### `crawler-service/src/web_crawler.py` (Web Crawling) 🔑 **QUAN TRỌNG**
```python
# 🕷️ Web Crawler: Crawl full HTML content từ website
# Đây là "real crawling" thực sự!

from bs4 import BeautifulSoup
import requests
import re

class ArticleCrawler:
    def crawl_article(self, url: str) -> dict:
        """
        Crawl toàn bộ content từ website HTML
        
        Quá trình:
        1. Download HTML từ URL
        2. Parse HTML bằng BeautifulSoup
        3. Tìm container chứa article (VNExpress: <article class="fck_detail">)
        4. Trích xuất: paragraphs + images theo thứ tự gốc
        5. Filter bỏ: scripts, ads, JavaScript code, timestamps
        6. Return HTML clean
        """
        
        # 1. Xác định website và route tới crawler phù hợp
        if 'vnexpress.net' in url:
            return self.crawl_vnexpress(url)
        elif 'dantri.com.vn' in url:
            return self.crawl_dantri(url)
        else:
            return self.crawl_generic(url)
    
    def crawl_vnexpress(self, url: str) -> dict:
        """
        Crawl VNExpress article
        
        HTML structure:
        <article class="fck_detail">
          <p class="Normal">Paragraph 1</p>
          <p class="Normal">Paragraph 2</p>
          <img src="..." alt="..." />
          <p class="Normal">Paragraph 3</p>
        </article>
        """
        # 1. Download HTML
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # 2. Tìm article container
        article_body = soup.find('article', class_='fck_detail')
        if not article_body:
            return None
        
        # 3. Trích xuất content (xem hàm dưới)
        content_html = self._collect_paragraphs_with_images(
            article_body, 
            url, 
            p_selector={'class_': 'Normal'}
        )
        
        return {'content': content_html, 'success': True}
    
    def _collect_paragraphs_with_images(self, container, page_url, p_selector=None):
        """
        Trích xuất paragraphs + images theo thứ tự gốc
        
        🔑 Quan trọng: Filter bỏ tất cả bad content:
        - JavaScript code
        - Ads (taboola, outbrain)
        - Timestamps (GMT, UTC)
        
        Quá trình:
        1. Xóa <script>, <style>, <iframe> tags
        2. Xóa div có class chứa 'ad', 'taboola', v.v.
        3. Duyệt qua các child elements theo thứ tự
        4. Với mỗi element:
           - Nếu <p>: trích text, filter JS code, add vào content
           - Nếu <img>: get URL, add vào content
           - Nếu <figure>: get image + caption, add vào content
        5. Return '\n'.join(content_parts)
        """
        
        # Remove unwanted elements first
        for unwanted in container.find_all(['script', 'style', 'iframe', 'noscript']):
            unwanted.decompose()
        
        # Remove ads
        for ad in container.find_all('div', class_=re.compile(r'ad|taboola|outbrain', re.I)):
            ad.decompose()
        
        content_parts = []
        
        # Process each child in order
        for elem in container.children:
            if isinstance(elem, str):
                text = str(elem).strip()
                if text and not self._is_javascript_content(text):
                    content_parts.append(f'<p>{text}</p>')
                continue
            
            if elem.name == 'p':
                text = elem.get_text(strip=True)
                if text and not self._is_javascript_content(text):
                    content_parts.append(f'<p>{text}</p>')
            
            elif elem.name == 'img':
                img_src = elem.get('data-src') or elem.get('src')
                abs_src = self._abs_url(img_src, page_url)
                if abs_src:
                    content_parts.append(f'<img src="{abs_src}" alt="" />')
            
            elif elem.name == 'figure':
                img = elem.find('img')
                if img:
                    img_src = img.get('src')
                    abs_src = self._abs_url(img_src, page_url)
                    if abs_src:
                        content_parts.append(f'<img src="{abs_src}" />')
                
                # Add caption if exists
                figcaption = elem.find('figcaption')
                if figcaption:
                    caption_text = figcaption.get_text(strip=True)
                    if caption_text:
                        content_parts.append(f'<p><em>{caption_text}</em></p>')
        
        return '\n'.join(content_parts)
    
    def _is_javascript_content(self, text: str) -> bool:
        """
        Filter JavaScript code, ads, timestamps
        
        Detect:
        - Keywords: 'taboola', 'window.', 'function(', etc.
        - Timestamps: '2024-01-10 12:30:00 GMT'
        """
        text_lower = text.lower()
        
        # Hard filter for ads
        ads_keywords = [
            'taboola', 'outbrain', 'arfasync', 'mutexads',
            'window.runinit', 'pageSettings', 'querySelector'
        ]
        
        for keyword in ads_keywords:
            if keyword in text_lower:
                return True
        
        # Detect timestamps
        if re.search(r'\d{4}-\d{2}-\d{2}.*GMT', text):
            return True
        
        # Count JS patterns
        js_patterns = ['var ', 'const ', 'function(', 'if (', 'for (']
        if sum(1 for p in js_patterns if p in text_lower) >= 3:
            return True
        
        return False
```

---

## 🔄 Quy Trình Hoạt Động (End-to-End)

### **Scenario 1: User Xem Bài Viết**

```
1. User mở web → frontend/app/page.tsx
   ├─ Fetch articles: GET /api/v1/articles
   └─ Display danh sách bài viết

2. User click vào 1 bài → news-detail-modal.tsx
   ├─ Modal mở
   ├─ Gọi API POST /api/v1/articles/read/{id}?user_id=X
   │  └─ Worker lưu vào UserReadingHistory
   └─ Hiển thị:
      ├─ Title + Summary
      ├─ Image
      └─ Full Content (từ crawler) ← 🔑 Web Crawling result!

3. User click "Lưu" → news-detail-modal.tsx
   ├─ Gọi API POST /api/v1/articles/save/{id}?user_id=X
   └─ Worker lưu vào UserSavedArticle
```

### **Scenario 2: Admin Kích Hoạt Crawl**

```
1. Admin vào /admin → admin/page.tsx
   └─ Click "Kích hoạt thu thập"

2. Frontend gửi → POST /api/v1/crawler/trigger
   └─ Core API nhận

3. Core API → gửi message vào RabbitMQ queue: 'crawl_tasks'
   └─ {source_id: 1, url: "https://vnexpress.net/rss/..."}

4. Crawler Service consumer nhận message
   ├─ Gọi fetch_feed(url)
   │  ├─ Parse RSS feed
   │  └─ Với mỗi article:
   │     ├─ Lấy title, summary từ RSS
   │     ├─ 🕷️ Crawl full content từ website (web_crawler.py)
   │     ├─ Lấy image
   │     └─ Gửi vào queue 'crawled_data'

5. Core API worker nhận từ 'crawled_data'
   ├─ Phân loại bài (AI) → classifier.py
   ├─ Tóm tắt bài (optional) → summary service
   └─ Lưu vào database

6. Frontend fetch lại → GET /api/v1/articles
   └─ Hiển thị bài viết mới cùng full content
```

---

## 📊 Database Schema

```
Users
├─ id (Primary Key)
├─ username (Unique)
├─ password_hash
├─ email
└─ role (user, admin)

Articles
├─ id (Primary Key)
├─ title
├─ summary
├─ content (🔑 Full HTML content từ crawler)
├─ link
├─ image_url
├─ category (Kinh doanh, Công nghệ, ...)
├─ source_id (Foreign Key → RSSSource)
├─ published_at
└─ fetched_at

RSSSource
├─ id (Primary Key)
├─ name (VNExpress, DanTri, ...)
├─ url (RSS feed URL)
├─ category
└─ is_active

UserSavedArticle
├─ user_id (Foreign Key)
├─ article_id (Foreign Key)
└─ saved_at

UserReadingHistory
├─ user_id (Foreign Key)
├─ article_id (Foreign Key)
└─ read_at
```

---

## 🚀 Deployment

```bash
# 1. Build all services
docker-compose build

# 2. Start all services
docker-compose up -d

# 3. Services running
- Frontend: http://localhost:3000
- API: http://localhost:8080
- Crawler: http://localhost:8003
- Summary: http://localhost:8004
- Recommendation: http://localhost:8005
- Database: localhost:5432
- Redis: localhost:6379
- RabbitMQ: localhost:5672
```

---

## 💡 Key Technologies

| Service | Tech | Version |
|---------|------|---------|
| Frontend | Next.js + React + TypeScript | 14.0 |
| API | FastAPI + SQLAlchemy | 0.104 |
| Crawler | BeautifulSoup4 + Requests | 4.12 |
| Database | PostgreSQL | 15 |
| Queue | RabbitMQ | 3.12 |
| Cache | Redis | 7.0 |
| ML | Sentence Transformers | 2.2 |
| Summary | Hugging Face BART | - |

---

## 🎯 Tóm Tắt

**Phuong Web** = Hệ thống tin tức thông minh với:
- ✅ **RSS Crawling** (nhanh, dữ liệu định sẵn)
- ✅ **Web Crawling** (real crawling từ HTML)
- ✅ **AI Classification** (phân loại tự động)
- ✅ **Microservices** (scalable, modular)
- ✅ **Full-featured** (save, history, recommendation)

**Kiến trúc**:
```
Frontend (Next.js) 
  ↔ 
Core API (FastAPI)
  ↕
Crawler Service (Python) → RabbitMQ → Worker → AI Classification
  ↕
PostgreSQL Database
```

---

**Tác giả**: AI Assistant  
**Ngày cập nhật**: 11/01/2026  
**Phiên bản**: 1.0
