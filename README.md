# phuong-web

## Microservice Smart News Reader

Ứng dụng đọc tin tức thông minh sử dụng RSS với kiến trúc microservices, Docker, và AI summarization.

### 🚀 Quick Start

```bash
git clone <repository-url>
cd phuong-web
make build && make up
# Visit http://localhost:3000
```

See [QUICKSTART.md](QUICKSTART.md) for detailed instructions.

### 📋 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get started in 5 minutes
- **[ARCHITECTURE.md](ARCHITECTURE.md)** - System architecture and design
- **[DEVELOPMENT.md](DEVELOPMENT.md)** - Development guide
- **[e2e-tests/README.md](e2e-tests/README.md)** - E2E API testing with HTTP files

### Kiến trúc

```
┌─────────────────────────────────────────────────────────────┐
│                      Frontend (Next.js)                     │
│                        Port 3000                            │
└─────────────────────┬───────────────────────────────────────┘
                      │ HTTP
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Core API Service (FastAPI)                     │
│         Port 8080 + Auth + RabbitMQ Consumer                │
└────┬────────────┬───────────────┬───────────────┬──────────┘
     │            │               │               │
     ▼            ▼               ▼               ▼
┌─────────┐  ┌─────────┐  ┌──────────────┐  ┌───────────┐
│ Crawler │  │Recommend│  │   Summary    │  │PostgreSQL │
│ Service │  │ Service │  │   Service    │  │(Port 5432)│
│         │  │(Port 8001)│ │  (Port 8002) │  └───────────┘
└────┬────┘  └─────┬───┘  └──────────────┘
     │            │
     │      ┌─────┴─────┐
     │      │  Qdrant   │
     │      │(Port 6333)│
     │      └───────────┘
     │
┌────┴────────────┐
│   RabbitMQ      │
│(5672/15672)     │
└─────────────────┘
```

Ứng dụng bao gồm các services sau:

1. **Core API Service** (Port 8080): Backend chính với Auth, quản lý RSS sources, articles, và crawler orchestration
2. **Crawler Service**: Worker thu thập tin tức từ RSS feeds qua RabbitMQ
3. **Recommendation Service** (Port 8001): AI recommendations với vector search (Qdrant)
4. **Summary Service** (Port 8002): Tóm tắt nội dung bài viết sử dụng AI/LLM
5. **Frontend** (Port 3000): Giao diện Next.js
6. **PostgreSQL** (Port 5432): Cơ sở dữ liệu chính
7. **Qdrant** (Port 6333): Vector database cho recommendations
8. **RabbitMQ** (Ports 5672/15672): Message broker cho giao tiếp async
9. **Redis** (Port 6379): Cache layer (optional)

### Yêu cầu

- Docker
- Docker Compose

### Cài đặt và chạy

1. Clone repository:
```bash
git clone <repository-url>
cd phuong-web
```

2. Copy file cấu hình môi trường (tùy chọn):
```bash
cp .env.example .env
```

3. Build và chạy tất cả services:

**Sử dụng Makefile (khuyến nghị):**
```bash
make build    # Build all images
make up       # Start all services
make logs     # View logs
```

**Hoặc sử dụng docker compose trực tiếp:**
```bash
docker compose up --build
```

Hoặc chạy ở chế độ background:
```bash
docker compose up -d --build
```

Lần đầu tiên build có thể mất 5-10 phút để tải các dependencies và AI model.

4. Truy cập các services:
- Frontend: http://localhost:3000
- Core API: http://localhost:8080
- Recommendation Service: http://localhost:8001
- Summary Service: http://localhost:8002
- RabbitMQ Management: http://localhost:15672 (guest/guest)
- Qdrant Dashboard: http://localhost:6333/dashboard
- PostgreSQL: localhost:5432
- Redis: localhost:6379

### Quản lý Services

**Sử dụng Makefile:**
```bash
make help       # Show all available commands
make ps         # Show status of all services
make logs       # View logs from all services
make restart    # Restart all services
make down       # Stop all services
make clean      # Stop and remove all containers, volumes
```

### Dừng services

```bash
make down
# hoặc
docker compose down
```

Để xóa cả volumes (dữ liệu):
```bash
make clean
# hoặc
docker compose down -v
```

### Development

#### Chạy chỉ infrastructure services (Database, Redis, RabbitMQ)

Để phát triển backend services riêng, bạn có thể chạy chỉ infrastructure:

```bash
make dev-up
# hoặc
docker compose -f docker-compose.dev.yml up -d
```

Sau đó chạy các services riêng lẻ như bên dưới.

Để dừng infrastructure services:
```bash
make dev-down
# hoặc
docker compose -f docker-compose.dev.yml down
```

#### Chạy từng service riêng lẻ

**API Gateway:**
```bash
cd core-api-service
pip install -r requirements.txt
# Set environment variables
export DB_HOST=localhost
export DB_NAME=newsdb
export DB_USER=postgres
export DB_PASSWORD=postgres
export RABBITMQ_HOST=localhost
export RECOMMENDATION_URL=http://localhost:8001
uvicorn src.main:app --reload --port 8080
```

**Storage Service:**
```bash
cd recommendation-service
pip install -r requirements.txt
# Set environment variables
export QDRANT_HOST=localhost
uvicorn main:app --reload --port 8001
```

**Crawler Service:**
```bash
cd crawler-service
pip install -r requirements.txt
# Set environment variables
export DB_HOST=localhost
export DB_NAME=newsdb
export DB_USER=postgres
export DB_PASSWORD=postgres
export RABBITMQ_HOST=localhost
# Run the service
python src/main_new.py
```

**AI Summarizer:**
```bash
cd summary-service
pip install -r requirements.txt
uvicorn main:app --reload --port 8002
```

**Frontend:**
```bash
cd frontend
npm install
# Set environment variable
export NEXT_PUBLIC_API_URL=http://localhost:8080
npm run dev
```

### Cấu trúc thư mục

```
phuong-web/
├── core-api-service/     # Central backend with Auth & orchestration
├── crawler-service/      # RSS crawler worker service
├── recommendation-service/ # AI recommendations with vector search
├── summary-service/      # AI text summarization service
├── frontend/             # Next.js frontend
├── docker-compose.yml    # Docker orchestration
└── .env.example          # Environment variables template
```

### Giao tiếp giữa các services

- **HTTP REST API**: Frontend ↔ Core API, Core API ↔ Recommendation/Summary services
- **RabbitMQ**: 
  - Core API → Crawler (crawl_tasks queue)
  - Crawler → Core API (crawled_data queue)
- **Vector Search**: Qdrant database cho AI recommendations

### Features

- ✅ Thu thập tin tức tự động từ RSS feeds
- ✅ Xác thực và phân quyền với JWT (RBAC)
- ✅ Quản lý RSS sources và articles
- ✅ Tóm tắt nội dung sử dụng AI (BART model)
- ✅ AI-powered semantic search với Qdrant vector database
- ✅ Gợi ý bài viết tương đồng (recommendations)
- ✅ Giao diện người dùng hiện đại với Next.js
- ✅ Kiến trúc microservices với Docker
- ✅ Message queue với RabbitMQ cho async processing
- ✅ Database PostgreSQL

### Testing

#### E2E API Testing with HTTP Files

Comprehensive end-to-end API testing using HTTP files following RFC 2616 specification:

```bash
# Install VS Code REST Client extension
# Open any .http file in e2e-tests/ directory
# Click "Send Request" to execute API calls
```

Test files available:
- `e2e-tests/health-check.http` - Health checks for all services
- `e2e-tests/auth.http` - Authentication endpoints
- `e2e-tests/articles.http` - Article management
- `e2e-tests/sources.http` - RSS source management
- `e2e-tests/crawler.http` - Crawler orchestration
- `e2e-tests/recommendation.http` - Recommendation service
- `e2e-tests/summary.http` - Summary service
- `e2e-tests/complete-workflow.http` - Complete E2E workflow

See [e2e-tests/README.md](e2e-tests/README.md) for detailed testing guide.

### License

MIT

